"""Cyclopibus Mistral Vibe Web API - Main Application"""

from typing import Optional
from litestar import Litestar, get, post, Request
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
async def hello_world(request: Request) -> HelloResponse:
    """
    Improved hello endpoint that accepts an optional name parameter.
    
    Query Parameters:
        name: Optional name to personalize the greeting
        
    Returns:
        HelloResponse: JSON response with hello message
        - If name is provided (even if empty): {"message": "Hello <name>!"}
        - If name is not provided: {"message": "Hello World!"}
    """
    name = request.query_params.get("name")
    if name is not None:  # Check if parameter is present, even if empty
        return HelloResponse(message=f"Hello {name}!")
    else:
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