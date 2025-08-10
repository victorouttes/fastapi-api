# FastAPI Project Template

A modern, production-ready template for building RESTful APIs with FastAPI, SQLModel, and PostgreSQL.

## Features

- **FastAPI Framework**: High-performance, easy-to-use web framework with automatic OpenAPI documentation
- **SQLModel ORM**: Type-safe ORM for Python based on Pydantic and SQLAlchemy
- **Async Database Support**: Asynchronous database operations with SQLAlchemy and asyncpg
- **Clean Architecture**: Organized with controllers, repositories, and entity models
- **Generic CRUD Operations**: Base classes for common database operations
- **Pagination Support**: Built-in pagination for list endpoints
- **Environment Configuration**: Easy configuration with environment variables
- **Database Migrations**: Automatic table creation on startup
- **Production-Ready**: Includes SSL support and connection pooling

## Project Structure

```
fastapi-api/
├── .env                    # Environment variables configuration
├── LICENSE                 # MIT License
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
├── run.py                  # Application entry point
└── src/                    # Source code
    ├── controllers/        # Business logic layer
    │   ├── base_controller.py
    │   └── book_controller.py
    ├── models/             # Data models and database access
    │   ├── entities/       # SQLModel entity definitions
    │   │   └── book.py
    │   ├── repositories/   # Data access layer
    │   │   ├── base_repository.py
    │   │   └── book_repository.py
    │   └── settings/       # Database configuration
    │       ├── db_connection_handler.py
    │       └── db_init.py
    └── routes/             # API endpoints
        └── book_routes.py
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/victorouttes/fastapi-api.git
   cd fastapi-api
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your database configuration:
   ```
   PG_HOST="your-postgres-host"
   PG_PORT="5432"
   PG_DB="your-database-name"
   PG_USER="your-username"
   PG_PASSWORD="your-password"
   ```

## Running the Application

Start the application with:

```bash
python run.py
```

The API will be available at http://localhost:8000

API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Usage

### Example API Endpoints

The template includes a complete CRUD implementation for a Book entity:

- `GET /books`: List all books with pagination
- `POST /books`: Create a new book
- `GET /books/{id}`: Get a book by ID
- `PUT /books/{id}`: Update a book
- `DELETE /books/{id}`: Delete a book

### Creating a New Entity

To create a new entity with full CRUD operations:

1. Create an entity model in `src/models/entities/`
2. Create a repository in `src/models/repositories/`
3. Create a controller in `src/controllers/`
4. Create routes in `src/routes/`
5. Register the router in `run.py`

## Development Guidelines

### Adding a New Entity

1. Define your entity model:
   ```python
   # src/models/entities/example.py
   from sqlmodel import SQLModel, Field
   
   class Example(SQLModel, table=True):
       id: int = Field(primary_key=True)
       # Add your fields here
   ```

2. Create a repository:
   ```python
   # src/models/repositories/example_repository.py
   from src.models.entities.example import Example
   from src.models.repositories.base_repository import BaseRepository
   
   class ExampleRepository(BaseRepository[Example]):
       pass
   
   example_repository = ExampleRepository()
   ```

3. Create a controller:
   ```python
   # src/controllers/example_controller.py
   from src.controllers.base_controller import BaseController
   from src.models.entities.example import Example
   from src.models.repositories.example_repository import ExampleRepository
   
   class ExampleController(BaseController[Example, ExampleRepository]):
       pass
   
   example_controller = ExampleController
   ```

4. Create routes:
   ```python
   # src/routes/example_routes.py
   from fastapi import APIRouter, Depends
   
   from src.controllers.example_controller import ExampleController, example_controller
   from src.models.entities.example import Example
   
   example_router = APIRouter(prefix="/examples", tags=["examples"])
   
   @example_router.get("/")
   async def list_examples(page: int = 1, size: int = 10, controller: ExampleController = Depends(example_controller)):
       return await controller.get_paginated(page, size)
   
   # Add other CRUD endpoints
   ```

5. Register the router in `run.py`:
   ```python
   from src.routes.example_routes import example_router
   
   # Add this line with the other router registrations
   app.include_router(example_router)
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.