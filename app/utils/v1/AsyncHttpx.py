import httpx
#from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type


async def get_client():
    # create a new client for each request
    async with httpx.AsyncClient() as client:
        # yield the client to the endpoint function
        yield client
        # close the client when the request is done



#@retry(wait=wait_fixed(2), stop=stop_after_attempt(3), retry=retry_if_exception_type(httpx.RequestError))
async def fetch_url(method: str, url: str, headers: dict = None, payload: dict = None):
    async with httpx.AsyncClient() as client:
        if method.upper() == 'GET':
            response = await client.get(url, headers=headers,timeout=None)
        elif method.upper() == 'POST':
            response = await client.post(url, headers=headers, json=payload,timeout=None)
        elif method.upper() == 'PUT':
            response = await client.put(url, headers=headers, json=payload,timeout=None)
        elif method.upper() == 'DELETE':
            response = await client.delete(url, headers=headers, json=payload,timeout=None)
        else:
            raise ValueError("Unsupported HTTP method")

        #response.raise_for_status()  # Raise an exception for 4xx and 5xx statuses
        return response
