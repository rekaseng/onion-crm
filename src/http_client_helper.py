import json

import httpx

async def call_get_method_api(url: str):
    client = httpx.AsyncClient()
    
    return await client.get(url=url)


async def call_post_method_api(url: str, data: any, ):
    client = httpx.AsyncClient()
    jsonStr = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = await client.post(url=url, data=jsonStr, headers=headers)
    return response