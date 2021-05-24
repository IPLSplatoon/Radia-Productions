from fastapi import Request, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

api_key_header_design = APIKeyHeader(name="Authorization", auto_error=True)


async def get_api_key(request: Request, api_key_header: str = Security(api_key_header_design)):
    response = await request.state.db.get_access_key_details(api_key_header)
    if response:
        return response
    else:
        raise HTTPException(status_code=401, detail="Not Authorised / Invalid API Key")
