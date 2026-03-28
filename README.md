# HR-ON Backend Task

## Setup and Run

### Local Development (Build from Source):
    docker-compose up

### Production:
    docker-compose -f docker-compose.prod.yml up

### Local Setup:
1. Install dependencies: `pip install -r requirements.txt`
2. Set up PostgreSQL locally and configure .env with: `DATABASE_URL=postgresql://user:password@localhost:5432/tasks`
3. Run: `uvicorn app.main:app --reload`
   
### Run Tests:
With docker:

    docker-compose exec app python -m unittest discover -s tests

With local Python:

    python -m unittest discover -s tests -p "test_*.py" -v

### Project Structure:
- `app/` - Application code
- `app/api/` - API endpoints
- `app/core/` - Database, config, logging
- `app/utils/` - Utilities (rate limiting)
- `tests/` - Unit tests
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Local development setup
- `docker-compose.prod.yml` - Production setup with pre-built image

## CI/CD

This project uses GitHub Actions to automatically:
- Run tests on every push
- Build Docker images
- Push to GitHub Container Registry (GHCR)

Images are available at: `ghcr.io/jbro910/sample-api:latest`
