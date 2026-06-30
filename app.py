"""Cyclopibus Mistral Vibe Web API - Main Application"""

from litestar import Litestar, get, post
from litestar.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from pydantic import BaseModel


class HelloResponse(BaseModel):
    """Response model for the hello endpoint"""
    message: str


class EchoRequest(BaseModel):
    """Request model for the echo endpoint"""
    message: str


class EchoResponse(BaseModel):
    """Response model for the echo endpoint"""
    echo: str


@get("/hello", status_code=HTTP_200_OK)
async def hello_world() -> HelloResponse:
    """
    Simple hello world endpoint.
    
    Returns:
        HelloResponse: JSON response with hello message
    """
    return HelloResponse(message="Hello World!")


@post("/echo", status_code=HTTP_200_OK)
async def echo_message(data: EchoRequest) -> EchoResponse:
    """
    Echo endpoint that returns what it receives.
    
    Args:
        data: EchoRequest containing the message to echo
        
    Returns:
        EchoResponse: JSON response with the echoed message
    """
    return EchoResponse(echo=data.message)


# Create the Litestar application
app = Litestar([hello_world, echo_message])