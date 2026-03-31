FastAPI Functions & Concepts in Your Project
1. FastAPI() - Creating the Application
```python
from fastapi import FastAPI

app = FastAPI(title="HR-ON Backend Task", lifespan=lifespan)
```
What it does: Creates the main FastAPI application instance.
- title: Names your API (appears in API documentation)
- lifespan: Handles startup/shutdown logic (explained below)

2. lifespan() - App Startup & Shutdown

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs BEFORE the app starts
    Base.metadata.create_all(bind=engine)  # Create database tables
    yield  # App now runs
    # Runs when app shuts down (cleanup code would go here)

app = FastAPI(lifespan=lifespan)
```
What it does:
- Code before yield runs once when the app starts
- Code after yield runs once when the app shuts down
- In your case: creates database tables on startup
 
3. APIRouter() - Organizing Routes
```python
from fastapi import APIRouter

router = APIRouter()  # Create a router (container for routes)

@router.get("/api/health")  # Define a GET endpoint
def health_check(...):
    return {...}

app.include_router(router)  # Add routes to the main app
```
What it does:
- Groups related endpoints together
- Makes code modular and organized
- In your project: keeps health check endpoints separate from main app
 
4. @router.get() - HTTP GET Route
```python
@router.get("/api/health")
def health_check(...):
    """Health check endpoint with logging."""
```
What it does:
- Defines an endpoint that responds to HTTP GET requests
- URL: GET /api/health
- Returns data to the client

Other HTTP methods available:
  - @router.post() - Create data
  - @router.put() - Update data
  - @router.delete() - Delete data
 
5. Depends() - Dependency Injection
```python
from fastapi import Depends

def health_check(
    db: Session = Depends(get_db),  # Inject database session
    _: None = Depends(rate_limiter),  # Inject rate limiter
):
```
What it does:
- Automatically calls the function inside Depends() and passes the result to your endpoint
- For get_db: Provides a fresh database session for each request (with automatic cleanup)
- For rate_limiter: Checks rate limits before the endpoint runs
- Example flow:
  - User makes request → FastAPI calls get_db()
  - Database session is created and passed to health_check()
  - Endpoint runs
  - Session is automatically closed (cleanup in finally block)
 
6. Query() - URL Query Parameters
```python
from fastapi import Query

def health_check(
    query: str | None = Query(None),  # Optional query parameter
):
```
What it does:
- Extracts URL query parameters: GET /api/health?query=database
- None = optional (can be skipped)
- Your code uses it to filter responses
 
7. HTTPException() - Error Responses
```python
from fastapi import HTTPException

raise HTTPException(status_code=400, detail="Invalid query parameter")
```
What it does:
- Sends an HTTP error response to the client
- status_code=400: Bad Request (client error)
- status_code=429: Too Many Requests (rate limiting in rate_limiter.py)
- detail: Error message shown to client
 
8. Request - Access Request Information
```python
from fastapi import Request

def health_check(request: Request):
    client_ip = request.client.host  # Get client's IP address
```
What it does:
- Provides access to incoming request details
- Your code uses it to log which IP is making requests
 
How They Work Together in Your Project
```
User makes request
    ↓
app receives GET /api/health?query=database
    ↓
FastAPI runs dependencies:
  1. Calls get_db() → creates database session
  2. Calls rate_limiter() → checks if client is rate limited
    ↓
health_check() function runs with injected dependencies
    ↓
Returns JSON response
    ↓
get_db() cleanup code runs (closes database connection)
```
Key Takeaway
FastAPI handles:
- Routing (matching URLs to functions)
- Dependency injection (automatically providing what functions need)
- Request/response handling (converting Python to JSON automatically)
- Validation (checking data types)
- Auto-generating API documentation at /docs
