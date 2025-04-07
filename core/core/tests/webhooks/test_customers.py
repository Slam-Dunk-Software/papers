from django.test import TestCase, RequestFactory
from unittest.mock import patch
from core.models import Customer, CustomerAddress, WebhookLog
from core.views import shopify_customer_create_webhook, shopify_customer_update_webhook
import json

class CustomerCreateWebhookTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Mock payload from Shopify customers/create webhook
        self.mock_payload = {
            "id": 12345,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "555-555-5555",
            "note": "Test customer",
            "state": "enabled",
            "currency": "USD",
            "tax_exempt": False,
            "verified_email": True,
            "created_at": "2025-04-07T12:00:00Z",
            "updated_at": "2025-04-07T12:00:00Z",
            "default_address": {
                "id": 67890,
                "customer_id": 12345,
                "address1": "123 Test St",
                "address2": "",
                "city": "Testville",
                "province": "Ontario",
                "zip": "12345",
                "country": "Canada",
                "phone": "555-1234",
                "name": "John Tester",
                "default": True
            }
        }

    @patch('core.views.verify_shopify_webhook', return_value=True)  # Mock HMAC verification
    def test_shopify_customer_create_webhook(self, other):
        # Create a mock request simulating the incoming webhook
        request = self.factory.post(
            '/webhooks/customers/create',
            data=json.dumps(self.mock_payload),
            content_type='application/json',
            HTTP_X_SHOPIFY_TOPIC='customers/create',
            HTTP_X_SHOPIFY_SHOP_DOMAIN='test-shop.myshopify.com',
            HTTP_X_SHOPIFY_HMAC_SHA256='mock-hmac-value'  # Mocked HMAC value
        )
        
        # Call the view
        response = shopify_customer_create_webhook(request)

        # Assert the status code is 200 (Success)
        self.assertEqual(response.status_code, 200)

        # Assert that a customer has been created (check database)
        customer = Customer.objects.get(shopify_id=12345)
        self.assertEqual(customer.first_name, 'John')
        self.assertEqual(customer.last_name, 'Doe')

        # Assert that a WebhookLog entry has been created
        log = WebhookLog.objects.get(topic='customers/create')
        self.assertIsNotNone(log)

        # Ensure the customer address was also created
        # You can check if the CustomerAddress object exists or not
        address = CustomerAddress.objects.filter(customer_shopify_id=12345).first()
        self.assertIsNotNone(address)
        self.assertEqual(address.address1, '123 Test St')


class CustomerUpdateWebhookTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # FIXME: create a mock user first that we can test the updates against

        # Mock payload from Shopify customers/update webhook
        self.mock_payload = {
            "id": 706405506930370084,
            "note": "This customer loves ice cream",
            "email": "bob@biller.com",
            "phone": None,
            "state": "disabled",
            "currency": "USD",
            "addresses": [],
            "last_name": "Biller",
            "created_at": "2025-04-07T08:30:33-04:00",
            "first_name": "Bob",
            "tax_exempt": False,
            "updated_at": "2025-04-07T08:30:33-04:00",
            "tax_exemptions": [],
            "verified_email": True,
            "default_address": {
                "id": 12321,
                "zip": "K2P 2L8",
                "city": "Ottawa",
                "name": "Bob Biller",
                "phone": "555-555-5555",
                "company": None,
                "country": "CA",
                "default": False,
                "address1": "151 O'Connor Street",
                "address2": None,
                "province": "ON",
                "last_name": "Biller",
                "first_name": "Bob",
                "customer_id": 706405506930370084,
                "country_code": "CA",
                "country_name": "CA",
                "province_code": "ON"},
            "admin_graphql_api_id": "gid://shopify/Customer/706405506930370084",
            "multipass_identifier": None
        }

    @patch('core.views.verify_shopify_webhook', return_value=True)  # Mock HMAC verification
    def test_shopify_customer_update_webhook(self, other):
        # First--create the user with the create hook
        # Create a mock request simulating the incoming webhook
        request = self.factory.post(
            '/webhooks/customers/create',
            data=json.dumps(self.mock_payload),
            content_type='application/json',
            HTTP_X_SHOPIFY_TOPIC='customers/create',
            HTTP_X_SHOPIFY_SHOP_DOMAIN='test-shop.myshopify.com',
            HTTP_X_SHOPIFY_HMAC_SHA256='mock-hmac-value'  # Mocked HMAC value
        )
        
        # Call the create hook
        response = shopify_customer_create_webhook(request)


        # Second--update
        self.mock_payload["note"] = "This user hates ice cream!!!"
        self.mock_payload["default_address"]["city"] = "Atlantis"

        # Create a mock request simulating the incoming webhook
        request = self.factory.post(
            '/webhooks/customers/update',
            data=json.dumps(self.mock_payload),
            content_type='application/json',
            HTTP_X_SHOPIFY_TOPIC='customers/update',
            HTTP_X_SHOPIFY_SHOP_DOMAIN='test-shop.myshopify.com',
            HTTP_X_SHOPIFY_HMAC_SHA256='mock-hmac-value'  # Mocked HMAC value
        )
        
        # Call the view
        response = shopify_customer_update_webhook(request)

        # Assert the status code is 200 (Success)
        self.assertEqual(response.status_code, 200)

        # Assert that a customer has been created (check database)
        customer = Customer.objects.get(shopify_id=706405506930370084)
        self.assertEqual(customer.first_name, 'Bob')
        self.assertEqual(customer.last_name, 'Biller')
        self.assertEqual(customer.note, 'This user hates ice cream!!!')

        # Assert that a WebhookLog entry has been created
        log = WebhookLog.objects.get(topic='customers/create')
        self.assertIsNotNone(log)

        # Ensure the customer address was also created
        # You can check if the CustomerAddress object exists or not
        address = CustomerAddress.objects.filter(customer_shopify_id=706405506930370084).first()
        self.assertIsNotNone(address)
        self.assertEqual(address.address1, "151 O'Connor Street")
        self.assertEqual(address.city, 'Atlantis')
