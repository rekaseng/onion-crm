from typing import List
from domain.repositories.payment_adapter import IPaymentAdapter
from domain.models.paynow import Paynow
from pyPayNowSg import PayNowConfigFactory, PayNowSerializer



class PaynowAdapter(IPaymentAdapter):
    def generate_payment_string(self, paynow: Paynow) -> str:
        UEN = "201531357R001"
        MERCHANT_NAME = "WHOLLY GREEN PTE. LTD."
        REFERENCE = paynow.order_ref
        amount = paynow.amount

        # Build merchant account information
        merchant_info = PayNowConfigFactory.build_merchant_account_info(
            proxy_type=2,  # Type 2 for PayNow
            proxy_value=UEN,  # UEN as Merchant ID
            editable_txn=False  # Indicates that it’s a live account
        )

        # Add reference
        additional_info = PayNowConfigFactory.build_additional_data(text=REFERENCE)

        # Serialize the QR code payload with amount and additional data
        paynow_qr_str = PayNowSerializer.serialize(
            MERCHANT_NAME,
            merchant_info,
            amount,
            additional_info
        )

        return paynow_qr_str

