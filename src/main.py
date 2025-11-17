import json
import threading

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from application.rabbitmq_consumer.order_consumer import order_consumer
from infrastructure.db.session import SessionLocal
import uvicorn
from api.router import api_router, admin_api_router
from config import settings
from api.rabbitmq_consumers.consumer import listen_message
from application.rabbitmq_consumer.paynow_received_consumer import paynow_received_consumer

app = FastAPI(
    docs_url="/shaker_docs",  # Rename /docs to /shake_docs
    redoc_url=None,  # Disable ReDoc
    openapi_url="/shaker_openapi.json",  # Rename openapi.json
    swagger_ui_parameters={"persistAuthorization": True}  # Enable token persistence
)

app.include_router(api_router, prefix='/api')
app.include_router(admin_api_router, prefix='/admin-api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=settings.CORS_ORIGIN_PATTERN

)

# Dependency
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "success": False,
            "error_message": exc.detail
        }
    ) 

def order_on_message_callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        order_consumer(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

def paynow_received_on_message_callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        paynow_received_consumer(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)


class OrderBackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        print('start listening OrderBackgroundTasks')
        listen_message(queueName='crm-order', on_message_callback=order_on_message_callback)

class PaynowReceivedBackgroundTasks(threading.Thread):
    def run(self,*args,**kwargs):
        print('start listening PaynowReceivedBackgroundTasks')
        listen_message(queueName='crm-paynow-received', on_message_callback=paynow_received_on_message_callback)


OrderMessageQueue = OrderBackgroundTasks()
OrderMessageQueue.start()

PaynowReceivedMessageQueue = PaynowReceivedBackgroundTasks()
PaynowReceivedMessageQueue.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8018)
