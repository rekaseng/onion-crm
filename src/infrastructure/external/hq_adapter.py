import json
from typing import List
from fastapi import HTTPException
from starlette import status

from application.dto.user_dto import MachineLoginWithUserDto
from config import settings
from domain.repositories.hq_adapter import IHqAdapter
import httpx

from domain.models.sku import HQSku

class HqAdapter(IHqAdapter):
    async def machine_login(self, machine_login_dto: MachineLoginWithUserDto) -> dict:
        url = settings.HQ_URL + "/api/customer/unlock_fridge"

        headers = {
            'api-key': settings.HQ_API_KEY,
            'Content-Type': 'application/json'  # Set content type to JSON
        }

        # Define the dictionary (payload) to send with the POST request
        data = machine_login_dto.dict()

        # Make the POST request
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers)

        # Check the response
        if response.status_code == 200:
            print("Success:", response.json())
            return response.json()
        else:
            print("Failed with status code:", response.status_code)
            print("Response:", response.text)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.text)
        
    async def get_all_skus(self) -> List[HQSku]:
        url = settings.HQ_URL + "/api/thirdparty/opencart/skus"

        headers = {
            'api-key': settings.HQ_API_KEY,
            'Content-Type': 'application/json'  # Set content type to JSON
        }

        # Make the GET request
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        # Check the response
        if response.status_code == 200:
            print("Success:", response.json())
            return json.loads(response.text)['data']
        else:
            print("Failed with status code:", response.status_code)
            print("Response:", response.text)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.text)