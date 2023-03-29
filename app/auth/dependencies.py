from app.auth.authorization_header_elements import get_bearer_token
from fastapi import Depends, Request
from app.auth.json_web_token import JsonWebToken


def validate_token(request: Request, token: str = Depends(get_bearer_token)):
    payload = JsonWebToken(token).validate()
    if payload:
        request.state.payload = payload
    return payload
