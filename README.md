# Python Code Execution Service

A secure Flask API service that executes Python scripts in a sandboxed environment and returns the result of the `main()` function.

## Features

- 🔒 **Secure Execution**: Uses nsjail for sandboxed code execution
- 📊 **Data Science Ready**: Includes pandas, numpy, matplotlib, and scipy
- ⏱️ **Resource Limits**: CPU, memory, and time limits to prevent abuse
- ✅ **Input Validation**: Validates script structure and syntax
- 🐳 **Docker Ready**: Lightweight containerized deployment
- ☁️ **Cloud Run Compatible**: Ready for Google Cloud Run deployment

## Quick Start

### Local Development

1. **Build the Docker image:**
   ```bash
   docker build -t python-executor .
   ```

2. **Run the service:**
   ```bash
   docker run -p 8080:8080 python-executor
   ```

3. **Test the API:**
   ```bash
   curl -X POST http://localhost:8080/execute \
     -H "Content-Type: application/json" \
     -d '{
       "script": "import json\ndef main():\n    return {\"message\": \"Hello World\", \"numbers\": [1, 2, 3]}"
     }'
   ```

## API Endpoints

### POST /execute

Executes a Python script and returns the result of the `main()` function.

**Request Body:**
```json
{
  "script": "def main():\n    return {\"result\": \"success\"}"
}
```

**Response:**
```json
{
  "result": {"result": "success"},
  "stdout": "Any print statements or output from the script"
}
```

**Requirements:**
- Script must contain a `main()` function
- `main()` function must return valid JSON
- Script must have valid Python syntax

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Example Scripts

### Basic Example
```python
def main():
    return {"message": "Hello from Python!", "timestamp": "2024-01-01"}
```

### Data Science Example
```python
import pandas as pd
import numpy as np

def main():
    # Create sample data
    data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'salary': [50000, 60000, 70000]
    }
    df = pd.DataFrame(data)
    
    # Calculate statistics
    stats = {
        'mean_age': float(df['age'].mean()),
        'total_salary': float(df['salary'].sum()),
        'count': len(df)
    }
    
    return stats
```

### Error Handling Example
```python
def main():
    try:
        # Simulate some computation
        result = 10 / 2
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Security Features

- **nsjail Sandboxing**: Isolated execution environment
- **Resource Limits**: 
  - CPU: 30 seconds
  - Memory: 512MB
  - File size: 1MB
  - Stack: 8MB
- **Non-root User**: Service runs as unprivileged user
- **Input Validation**: Syntax and structure validation
- **Timeout Protection**: 30-second execution timeout

## Available Libraries

The execution environment includes:
- **Standard Library**: All Python standard library modules
- **Data Science**: pandas, numpy, matplotlib, scipy
- **System Access**: Limited file system access to `/tmp` only

## Deployment

### Google Cloud Run

1. **Build and push to Google Container Registry:**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/python-executor
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy python-executor \
     --image gcr.io/YOUR_PROJECT_ID/python-executor \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8080
   ```

3. **Test with Cloud Run URL:**
   ```bash
   curl -X POST https://YOUR_SERVICE_URL/execute \
     -H "Content-Type: application/json" \
     -d '{
       "script": "def main():\n    return {\"deployed\": \"successfully\"}"
     }'
   ```

### Local Docker

```bash
# Build image
docker build -t python-executor .

# Run container
docker run -p 8080:8080 python-executor

# Test locally
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"status\": \"running\"}"}'
```

## Error Handling

The service returns appropriate HTTP status codes:

- **200**: Successful execution
- **400**: Invalid input or script execution error
- **500**: Internal server error

Error responses include:
```json
{
  "error": "Error description",
  "stdout": "Any captured output"
}
```

## Limitations

- Scripts must contain a `main()` function
- `main()` function must return JSON-serializable data
- Maximum execution time: 30 seconds
- Limited file system access
- No network access from within scripts
- No access to system commands

## Development

### Project Structure
```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── nsjail.cfg         # nsjail security configuration
├── Dockerfile         # Docker container definition
└── README.md          # This file
```

### Testing

Test the service with various scripts:

```bash
# Test basic functionality
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"test\": \"passed\"}"}'

# Test data science libraries
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "import numpy as np\ndef main():\n    return {\"array_sum\": float(np.sum([1,2,3]))}"}'

# Test error handling
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return 1/0"}'
```

## Repository

This project is hosted at: [https://github.com/rituraj-gharat/python-execution-api](https://github.com/rituraj-gharat/python-execution-api)

## License

This project is provided as-is for educational and demonstration purposes. 