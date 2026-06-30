"""Cyclopibus Mistral Vibe Web API - Main Application"""

from litestar import Litestar, get
from litestar.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from pydantic import BaseModel


class HelloResponse(BaseModel):
    """Response model for the hello endpoint"""
    message: str


@get("/hello", status_code=HTTP_200_OK)
async def hello_world() -> HelloResponse:
    """
    Simple hello world endpoint.
    
    Returns:
        HelloResponse: JSON response with hello message
    """
    return HelloResponse(message="Hello World!")


# Create the Litestar application
app = Litestar([hello_world])