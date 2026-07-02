"""Cyclopibus Mistral Vibe Web API - Main Application"""

from litestar import Litestar, get, post, Request
from litestar.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from litestar.exceptions import HTTPException
from pydantic import BaseModel
import httpx


class HelloResponse(BaseModel):
    """Response model for the hello endpoint"""
    message: str


class EchoRequest(BaseModel):
    """Request model for the echo endpoint"""
    message: str


class EchoResponse(BaseModel):
    """Response model for the echo endpoint"""
    echo: str


class WeatherResponse(BaseModel):
    """Response model for the weather endpoint"""
    weather: str


class BinaryRequest(BaseModel):
    """Request model for the binary conversion endpoint"""
    number: int


class BinaryResponse(BaseModel):
    """Response model for the binary conversion endpoint"""
    binary: str


# Open-Meteo API Constants
OPEN_METEO_GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Weather code to human-readable description mapping
WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}


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


@get("/weather", status_code=HTTP_200_OK)
async def get_weather(request: Request) -> WeatherResponse:
    """
    Weather endpoint that returns current weather for a given city.
    
    Query Parameters:
        city: Name of the city to get weather for (required)
        
    Returns:
        WeatherResponse: JSON response with weather description
        - Format: {"weather": "<current weather description>"}
        
    Raises:
        HTTP_400_BAD_REQUEST: If city parameter is missing or not found
        HTTP_500_INTERNAL_SERVER_ERROR: If weather API calls fail
    """
    city = request.query_params.get("city")
    
    if not city:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="City parameter is required")
    
    try:
        # Step 1: Use Open-Meteo Geocoding API to get coordinates for the city
        geocoding_url = f"{OPEN_METEO_GEOCODING_API_URL}?name={city}"
        
        async with httpx.AsyncClient() as client:
            # Get coordinates from city name
            geocoding_response = await client.get(geocoding_url)
            geocoding_response.raise_for_status()
            geocoding_data = geocoding_response.json()
            
            if not geocoding_data.get("results"):
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"City '{city}' not found")
            
            # Extract latitude and longitude from first result
            latitude = geocoding_data["results"][0]["latitude"]
            longitude = geocoding_data["results"][0]["longitude"]
            
            # Step 2: Use Open-Meteo Weather API to get current weather
            weather_url = f"{OPEN_METEO_WEATHER_API_URL}?latitude={latitude}&longitude={longitude}&current_weather=true"
            weather_response = await client.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            
            # Extract weather description from current_weather
            current_weather = weather_data["current_weather"]
            weather_code = current_weather["weathercode"]
            
            # Convert weather code to human-readable description
            weather_description = WEATHER_CODE_MAP.get(weather_code, f"Unknown weather code: {weather_code}")
            
            return WeatherResponse(weather=weather_description)
            
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Weather API error: {str(e)}")
    except HTTPException:
        # Re-raise HTTPException to avoid being caught by the general Exception handler
        raise
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching weather: {str(e)}")


@post("/to-binary", status_code=HTTP_200_OK)
async def convert_to_binary(data: BinaryRequest) -> BinaryResponse:
    """
    Convert a base 10 number to binary (base 2).
    
    Args:
        data: BinaryRequest containing the number to convert
        
    Returns:
        BinaryResponse: JSON response with the binary representation
        - Format: {"binary": "<binary string>"}
        
    Raises:
        HTTP_400_BAD_REQUEST: If the number is negative (validation handled by Pydantic)
    """
    # Convert the number to binary string (removes '0b' prefix)
    binary_string = bin(data.number)[2:]
    return BinaryResponse(binary=binary_string)


# Create the Litestar application
app = Litestar([hello_world, echo_message, get_weather, convert_to_binary])