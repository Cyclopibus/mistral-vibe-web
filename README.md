# Cyclopibus Mistral Vibe Web API

A Python Web API that agglomerate multiple tools into a single API.

## Features

- Built with **Litestar** (fast ASGI framework)
- Uses **Pydantic** for data validation and serialization
- Managed with **uv** for dependency management

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

### Run the server
```bash
python main.py
```

The server will start on `http://0.0.0.0:8000`

### API Endpoints

#### GET /hello
- **Method**: GET
- **Query Parameters**:
  - `name` (optional): Name to personalize the greeting
- **Status Code**: 200 OK (success)
- **Response Body**: 
  - With name: `{"message": "Hello <name>!"}`
  - Without name: `{"message": "Hello World!"}`

#### POST /echo
- **Method**: POST
- **Request Body**: `{"message": "your message here"}`
- **Status Code**: 200 OK (success) / 400 Bad Request (validation error)
- **Response Body**: `{"echo": "your message here"}`
- **Description**: Returns the message that was sent in the request

#### GET /weather
- **Method**: GET
- **Query Parameters**:
  - `city` (required): Name of the city to get weather for
- **Status Code**: 200 OK (success) / 400 Bad Request (missing or invalid city)
- **Response Body**: `{"weather": "<weather description>"}`
- **Description**: Returns current weather description for the specified city using Open-Meteo API

#### POST /to-binary
- **Method**: POST
- **Request Body**: `{"number": <integer>}`
- **Status Code**: 200 OK (success) / 400 Bad Request (validation error)
- **Response Body**: `{"binary": "<binary string>"}`
- **Description**: Converts a base 10 integer to its binary (base 2) string representation

## Project Structure

- `app.py` - Main application with Litestar routes
- `main.py` - Entry point for running the server
- `pyproject.toml` - Project configuration and dependencies
- `test_app.py` - Unit tests for the API endpoints

## Testing

You can test the endpoints using:

### Test /hello endpoint (no name)
```bash
curl http://localhost:8000/hello
```

Expected response:
```json
{"message": "Hello World!"}
```

### Test /hello endpoint (with name)
```bash
curl "http://localhost:8000/hello?name=Alice"
```

Expected response:
```json
{"message": "Hello Alice!"}
```

### Test /echo endpoint
```bash
curl -X POST http://localhost:8000/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Echo!"}'
```

Expected response:
```json
{"echo": "Hello Echo!"}
```

### Test /weather endpoint
```bash
curl "http://localhost:8000/weather?city=Paris"
```

Expected response:
```json
{"weather": "Clear sky"}
```

### Test /to-binary endpoint
```bash
curl -X POST http://localhost:8000/to-binary \
  -H "Content-Type: application/json" \
  -d '{"number": 42}'
```

Expected response:
```json
{"binary": "101010"}
```

### Run all tests
```bash
python -m pytest test_app.py -v
```