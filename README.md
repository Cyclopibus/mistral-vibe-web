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
- **Status Code**: 200 OK (success)
- **Response Body**: `{"message": "Hello World!"}`

#### POST /echo
- **Method**: POST
- **Request Body**: `{"message": "your message here"}`
- **Status Code**: 200 OK (success) / 400 Bad Request (validation error)
- **Response Body**: `{"echo": "your message here"}`
- **Description**: Returns the message that was sent in the request

## Project Structure

- `app.py` - Main application with Litestar routes
- `main.py` - Entry point for running the server
- `pyproject.toml` - Project configuration and dependencies
- `test_app.py` - Unit tests for the API endpoints

## Testing

You can test the endpoints using:

### Test /hello endpoint
```bash
curl http://localhost:8000/hello
```

Expected response:
```json
{"message": "Hello World!"}
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

### Run all tests
```bash
python -m pytest test_app.py -v
```