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
- **Status Code**: 200 OK (success)
- **Response Body**: `{"message": "Hello World!"}`

## Project Structure

- `app.py` - Main application with Litestar routes
- `main.py` - Entry point for running the server
- `pyproject.toml` - Project configuration and dependencies

## Testing

You can test the endpoint using:
```bash
curl http://localhost:8000/hello
```

Expected response:
```json
{"message": "Hello World!"}
```