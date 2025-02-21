# AIAssistant

This repository contains code for AI Assistant integration with the medical VR project.

# Medical VR API

This is a FastAPI-based backend for Medical VR applications.

## Setup:

1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `uvicorn server.main:app --reload`

## Project Strucutre -

```
/server
│── /app
│   │── /api
│   │   │── __init__.py
│   │   │── endpoints.py        # API routes
│   │── /core
│   │   │── __init__.py
│   │   │── config.py           # Configuration settings
│   │── /db
│   │   │── __init__.py
│   │   │── database.py         # Database connection
│   │── /models
│   │   │── __init__.py
│   │   │── api_keys.py         # Database model for API keys
│   │── /services
│   │   │── __init__.py
│   │   │── auth.py             # API key & authentication
│   │   │── rate_limit.py       # Rate limiting with Redis
│   │── /schemas
│   │   │── __init__.py
│   │   │── data_schema.py      # Pydantic models for validation
│   │── main.py                 # FastAPI app entry point
│── /migrations                 # Database migrations Future(Alembic)
│── /tests                      # Unit & Integration tests
│── .env                        # Environment variables (Do not commit this)
│── requirements.txt            # Python dependencies
│── Dockerfile                  # Docker containerization
│── README.md                   # Project documentation
```
