import httpx



def get_sync_client():
    # create a new client for each request
    with httpx.Client() as client:
        # yield the client to the endpoint function
        yield client
        # close the client when the request is done




def sync_fetch_url(method: str, url: str, headers: dict = None, payload: dict = None):
    with httpx.Client() as client:
        match method.upper():
            case 'GET':
                response = client.get(url, headers=headers)
            case 'POST':
                response = client.post(url, headers=headers, json=payload)
            case 'PUT':
                response = client.put(url, headers=headers, json=payload)
            case 'DELETE':
                response = client.delete(url, headers=headers, json=payload)
            case _:
                raise ValueError("Unsupported HTTP method")


        return response
