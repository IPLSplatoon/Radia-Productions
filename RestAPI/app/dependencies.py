from fastapi import Request, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from app.database import AccessKey
from typing import Optional

header_authorization = APIKeyHeader(name="Authorization", auto_error=True)


async def get_api_key(request: Request, api_key_header: str = Security(header_authorization)) -> Optional[AccessKey]:
    response = await request.state.db.get_access_key_details(api_key_header)
    if response:
        return response
    else:
        raise HTTPException(status_code=401, detail="Not Authorised / Invalid API Key")
