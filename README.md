# HR-ON Backend Task

## Setup and Run

### With Docker:
    docker-compose up

### Local Setup:
1. Install dependencies: `pip install -r requirements.txt`
2. Set DATABASE_URL in .env pointing to local PostgreSQL
3. Run: `uvicorn app.main:app --reload`
   
### Run Tests:
    docker-compose exec app python -m unittest discover -s tests