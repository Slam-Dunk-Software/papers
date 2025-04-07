from django.test import TestCase, RequestFactory
from unittest.mock import patch
from core.models import Customer, CustomerAddress, WebhookLog
from core.views import shopify_customer_create_webhook
import json


class ShopifyWebhookTest(TestCase):
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
            HTTP_X_SHOPIFY_SHOP_DOMAIN='your-shop.myshopify.com',
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

