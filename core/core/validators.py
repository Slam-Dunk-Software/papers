from pydantic import BaseModel
from typing import Optional

class CustomerAddressCreateData(BaseModel):
    id: int
    customer_id: int # NOTE: We're going to use this as shopify_id (to link to the customer's shopify_id)
    address1: str
    address2: Optional[str]
    city: str
    province: str
    zip: str
    country: str
    phone: Optional[str]
    name: Optional[str]
    default: bool
    
    class Config:
        from_attributes = True


# This matches the Shopify customer data shape we get in the webhook
class CustomerCreateData(BaseModel):
    id: int # NOTE: We're going to use this as shopify_id
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    note: Optional[str]
    state: Optional[str]
    currency: Optional[str]
    tax_exempt: Optional[bool]
    verified_email: Optional[bool]
    created_at: str
    updated_at: str
    default_address: Optional[CustomerAddressCreateData]

    class Config:
        from_attributes = True  # This is necessary to allow pydantic models to work with ORM models if you need to use them.
