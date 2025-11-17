from typing import List, Optional
from pydantic import BaseModel

class TwoCTwoPRequestPaymentRequest(BaseModel):
    name: str
    invoiceNo: str
    description: str
    amount: float

class TwoCTwoPDirectPaymentRequest(BaseModel):
    name: str
    invoiceNo: str
    description: str
    amount: float
    customer_id: int


class TwoCTwoPRequestPaymentPayload(TwoCTwoPRequestPaymentRequest):
    merchantID: str
    currencyCode: str
    tokenize: bool
    customerToken: List[str]
    request3DS: str
    paymentChannel: List[str]

class TwoCTwoPPaymentResponse(BaseModel):
    webPaymentUrl: str
    paymentToken: str
    respCode: str
    respDesc: str

class TwoCTwoPDirectPaymentResponse(BaseModel):
    data: Optional[str]
    invoiceNo: Optional[str]
    channelCode: str
    respCode: str
    respDesc: str

class TwoCTwoPPaymentResultResponse(BaseModel):
    merchantID: Optional[str]
    invoiceNo: Optional[str]
    accountNo: Optional[str]
    amount: Optional[float]
    currencyCode: Optional[str]
    tranRef: Optional[str]
    referenceNo: Optional[str]
    approvalCode: Optional[str]
    eci: Optional[str]
    transactionDateTime: Optional[str]
    respCode: Optional[str]
    respDesc: Optional[str]
    paymentScheme: Optional[str]
    childMerchantID: Optional[str]
    agentCode: Optional[str]
    channelCode: Optional[str]
    customerToken: Optional[str]
    customerTokenExpiry: Optional[str]
    cardType: Optional[str]
    issuerCountry: Optional[str]
    issuerBank: Optional[str]
    paymentID: Optional[str]
    schemePaymentID: Optional[str]

class TwoCTwoPPaymentWebHookRequest(BaseModel):
    payload: str