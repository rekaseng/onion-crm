import datetime
from infrastructure.db.session import SessionLocalSync
from infrastructure.repositories.sync.sql_sync_payment_repository import SQLSyncPaymentRepository
from domain.models.payment import Payment, PaymentType
from domain.models.store_credit_transaction import StoreCreditTransaction, StoreCreditTransactionType
from domain.models.store_credits import StoreCredit
from infrastructure.repositories.sync.sql_sync_store_credit_repository import SQLSyncStoreCreditRepository
from infrastructure.repositories.sync.sql_sync_store_credit_transaction_repository import SQLSyncStoreCreditTransactionRepository
from infrastructure.repositories.sync.sql_sync_transaction_repository import SQLSyncTransactionRepository
from utils.constants import PAYMENT_DESC_PAYNOW_TOPUP


def paynow_received_consumer(message) -> None:
    db = SessionLocalSync()
    try:
        result = None

        payment_repository = SQLSyncPaymentRepository(db)
        store_credit_repository = SQLSyncStoreCreditRepository(db)
        store_credit_transaction_repository = SQLSyncStoreCreditTransactionRepository(db)
        transaction_repository = SQLSyncTransactionRepository(db)

        invoice_no = message['bill_reference'].lower()

        transaction = transaction_repository.get_by_ref_sync(invoice_no)
        if transaction == None or transaction.user_id == None:
            print(f"[paynow_received_consumer] cannot upsert store credits due to user_id not found.")
            return result
        
        payment_dto = Payment(
            amount=float(message['txn_amount']),
            invoice_no=str(message['bill_reference']).lower(),
            order_id=None,
            transaction_id = transaction.id,
            user_id= transaction.user_id,
            success=message['status_code'] == '0' or message['status_code'] == '00',
            type=PaymentType.PAYNOW,
            description=PAYMENT_DESC_PAYNOW_TOPUP,
            raw_data=message,
            is_deleted=False,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        result = payment_repository.add_sync(payment_dto)

        # store credits
        if payment_dto.success != True:
            return None

        print("getting " + payment_dto.invoice_no)

        store_credit = StoreCredit(
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now(),
            user_id=transaction.user_id,
            latest_amount=payment_dto.amount,
            type=StoreCreditTransactionType.CREDIT,
            is_deleted=False
        )
        store_credit_id = store_credit_repository.upsert_sync(store_credit)
        store_credit_transaction = StoreCreditTransaction(
            type = StoreCreditTransactionType.CREDIT,
            amount = payment_dto.amount,
            store_credit_id = store_credit_id,
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now(),
        )
        store_credit_transaction_repository.add_sync(store_credit_transaction)

        transaction_repository.update_sync(payment_dto.invoice_no, True)

        print("[paynow_received_consumer] Data processed successfully:", message, result)
        return None
        
    except Exception as e:
        print(f"[paynow_received_consumer] Error processing message: {e}")

    finally:
        db.close()