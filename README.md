# Product Management API

A full-stack product management system built with Python, FastAPI, and MySQL following Domain-Driven Design (DDD) principles.

## 🚀 Features

- **Product Management**: CRUD operations for products
- **Search Functionality**: Search by product name (partial match) and price range
- **DDD Architecture**: Clean separation of concerns with domain, application, and infrastructure layers
- **Modular Architecture**: Separated middleware and error handling for better maintainability
- **Comprehensive Error Handling**: Custom exceptions with detailed error responses
- **Request Tracking**: Unique request IDs for better debugging and monitoring
- **Performance Monitoring**: Built-in slow request detection and logging
- **Database Migrations**: Automated schema management with Alembic
- **Docker Support**: Containerized application with Docker Compose
- **API Documentation**: Interactive Swagger UI
- **Comprehensive Testing**: 79.8% test coverage with organized test structure
- **Type Safety**: Full type hints and validation
- **Structured Logging**: JSON-formatted logs with contextual information

## 🏗️ Architecture

This project follows Domain-Driven Design (DDD) principles with the following structure:

```
src/
├── domain/           # Domain layer (entities, value objects, repositories)
├── application/      # Application layer (use cases, services)
├── infrastructure/   # Infrastructure layer (database, external services)
└── presentation/     # Presentation layer (API endpoints, controllers)
    ├── controllers/  # FastAPI route handlers
    ├── middleware/   # Custom middleware (CORS, logging, performance)
    └── error_handlers/ # Exception handling and custom error responses
```

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Testing**: pytest, pytest-cov
- **Logging**: structlog (structured JSON logging)
- **Containerization**: Docker, Docker Compose
- **Documentation**: Swagger/OpenAPI
- **Code Quality**: Type hints, linting, coverage reporting

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <git@github.com:hiccup1202/fastAPI_CRUD_Demonstration.git>
   cd fastAPI_CRUD_Demonstration
   ```

2. **Start the application**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development

#### Option 1: Using Makefile (Recommended)
```bash
# Install dependencies and set up virtual environment
make install

# Run the application
make run
```

#### Option 2: Using Setup Script
```bash
# Run the development setup script
./scripts/setup_dev.sh

# Activate virtual environment
source venv/bin/activate

# Run the application
make run
```

#### Option 3: Manual Setup
1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   uvicorn src.presentation.main:app --reload
   ```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication
Currently, the API does not require authentication.

### Endpoints

#### 1. Create Product
- **POST** `/api/v1/products`
- **Description**: Add a new product
- **Request Body**:
  ```json
  {
    "name": "Sample Product",
    "price": 1000
  }
  ```
- **Response**: Product details with generated ID

#### 2. Get Product by ID
- **GET** `/api/v1/products/{product_id}`
- **Description**: Retrieve a specific product by ID
- **Response**: Product details

#### 3. Search Products
- **GET** `/api/v1/products/search`
- **Description**: Search products by name or price range
- **Query Parameters**:
  - `name`: Product name (partial match)
  - `min_price`: Minimum price (inclusive)
  - `max_price`: Maximum price (inclusive)
  - `skip`: Number of records to skip (default: 0)
  - `limit`: Number of records to return (default: 100)
- **Response**: List of matching products

#### 4. Update Product
- **PUT** `/api/v1/products/{product_id}`
- **Description**: Update existing product information
- **Request Body**:
  ```json
  {
    "name": "Updated Product Name",
    "price": 1500
  }
  ```
- **Response**: Updated product details

#### 5. Delete Product
- **DELETE** `/api/v1/products/{product_id}`
- **Description**: Delete an existing product
- **Response**: Success message

### Example Usage

#### Create a product
```bash
curl -X POST "http://localhost:8000/api/v1/products" \
     -H "Content-Type: application/json" \
     -d '{"name": "Laptop", "price": 150000}'
```

#### Search products
```bash
curl "http://localhost:8000/api/v1/products/search?name=laptop&min_price=100000&max_price=200000"
```

## 🧪 Testing

The project has comprehensive test coverage (79.8%) with organized test structure using `__init__.py` imports for cleaner test code.

### Test Structure
```
tests/
├── __init__.py           # Centralized imports for all tests
├── unit/
│   ├── __init__.py       # Unit test specific imports
│   ├── test_domain_entities.py
│   └── test_use_cases.py
└── integration/
    ├── __init__.py       # Integration test specific imports
    └── test_api_endpoints.py
```

### Run all tests
```bash
# Using Docker
docker-compose exec api pytest

# Local development (with virtual environment)
source venv/bin/activate
pytest tests/ -v
```

### Coverage Reports

#### Quick Coverage Script
```bash
# Use the convenient coverage script
./scripts/coverage.sh
```

#### Manual Coverage Commands
```bash
# Terminal report with missing lines
pytest tests/ --cov=src --cov-report=term-missing

# HTML report for detailed analysis
pytest tests/ --cov=src --cov-report=html

# Open HTML report in browser
python -m http.server 8080 --directory htmlcov
# Then visit: http://localhost:8080
```

#### Coverage Configuration
The project includes a `.coveragerc` file for consistent coverage reporting:
- **Source tracking**: Only measures `src/` directory
- **Exclusions**: Ignores test files, virtual env, cache files
- **Multiple formats**: Terminal, HTML, and XML reports

### Run specific test categories
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Domain layer tests
pytest tests/unit/test_domain_entities.py -v

# Use case tests
pytest tests/unit/test_use_cases.py -v

# API endpoint tests
pytest tests/integration/test_api_endpoints.py -v
```

### Coverage Goals
- **Overall**: 80.5% (target: >80%)

## 🗄️ Database

### Schema
The application uses a single `products` table with the following structure:

```sql
CREATE TABLE products (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    price INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Migrations
Database migrations are managed with Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🐳 Docker

### Services
- **api**: FastAPI application (port 8000)
- **db**: MySQL database (port 3306)

### Environment Variables
Key environment variables can be configured in `docker-compose.yml`:

- `MYSQL_ROOT_PASSWORD`: MySQL root password
- `MYSQL_DATABASE`: Database name
- `MYSQL_USER`: Database user
- `MYSQL_PASSWORD`: Database password

### Docker Development
```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Execute commands in container
docker-compose exec api pytest

# Stop services
docker-compose down
```

## 📁 Project Structure

```
.
├── src/
│   ├── domain/                    # Domain layer (business logic)
│   │   ├── entities/              # Domain entities (Product)
│   │   ├── value_objects/         # Value objects (Price, ProductId, ProductName)
│   │   └── repositories/          # Repository interfaces
│   ├── application/               # Application layer (use cases)
│   │   └── use_cases/             # Business use cases (CRUD operations)
│   ├── infrastructure/            # Infrastructure layer (external concerns)
│   │   ├── database/              # Database configuration and models
│   │   └── repositories/          # Repository implementations
│   └── presentation/              # Presentation layer (API)
│       ├── controllers/           # FastAPI route handlers
│       ├── middleware/            # Custom middleware (CORS, logging)
│       ├── error_handlers/        # Exception handling
│       └── main.py                # Application entry point
├── tests/
│   ├── __init__.py                # Centralized test imports
│   ├── unit/                      # Unit tests
│   │   ├── __init__.py            # Unit test imports
│   │   ├── test_domain_entities.py
│   │   └── test_use_cases.py
│   └── integration/               # Integration tests
│       ├── __init__.py            # Integration test imports
│       └── test_api_endpoints.py
├── scripts/
│   ├── coverage.sh                # Coverage reporting script
│   └── setup_dev.sh               # Development setup script
├── htmlcov/                       # Coverage HTML reports
├── alembic/                       # Database migrations
├── docker/                        # Docker configuration files
├── requirements.txt               # Python dependencies
├── .coveragerc                    # Coverage configuration
├── .gitignore                     # Git ignore patterns
├── docker-compose.yml             # Docker Compose configuration
├── Dockerfile                     # Docker image definition
└── README.md                      # Project documentation
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string
- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging level

### Database Configuration
The application supports MySQL with the following default configuration:
- Host: `db` (Docker) or `localhost` (local)
- Port: `3306`
- Database: `product_management`
- User: `product_user`

## 🚨 Error Handling

The application features comprehensive error handling with custom exceptions and detailed error responses.

### Error Response Format
All errors include a standardized format with request tracking:
```json
{
  "error": "Error Type",
  "detail": "Human-readable error message",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status_code": 400
}
```

### HTTP Status Codes
- `400 Bad Request`: Business logic violations
- `401 Unauthorized`: Authentication failures
- `403 Forbidden`: Authorization failures  
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Unexpected server errors
- `502 Bad Gateway`: External service errors

### Custom Exceptions
The application defines several custom exception types:
- **BusinessLogicError**: Business rule violations
- **ResourceNotFoundError**: Missing resources with context
- **ValidationError**: Custom validation failures
- **AuthenticationError**: Authentication issues
- **AuthorizationError**: Permission denials
- **ExternalServiceError**: Third-party service failures

### Request Tracking
Every request is assigned a unique `request_id` that appears in:
- Error responses
- Application logs
- Response headers (`X-Request-ID`)

This enables easy correlation between client requests and server logs for debugging.

## 📊 Monitoring & Logging

### Structured Logging
The application uses `structlog` for JSON-formatted logging with contextual information:

```json
{
  "event": "Incoming request",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "method": "POST",
  "path": "/api/v1/products",
  "client_ip": "127.0.0.1",
  "user_agent": "curl/7.68.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Performance Monitoring
- **Request Tracking**: Every request gets a unique ID
- **Processing Time**: Logged for all requests
- **Slow Request Detection**: Configurable threshold (default: 1 second)
- **Error Correlation**: Request IDs link errors to specific requests

### Middleware Features
- **CORS Handling**: Configurable for development and production
- **Request Logging**: Comprehensive request/response logging
- **Performance Monitoring**: Built-in slow request detection
- **Error Context**: Automatic error context injection

### Log Levels
- `INFO`: Normal operations, request/response logging
- `WARNING`: Slow requests, business logic violations
- `ERROR`: Unexpected errors, external service failures
- `DEBUG`: Detailed debugging information (development only)

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints throughout the codebase
- Write docstrings for all public functions
- Organize imports using `__init__.py` files
- Separate concerns (middleware, error handling, business logic)

### Testing
- Maintain >80% test coverage (current: 80.5%)
- Write unit tests for all business logic
- Include integration tests for API endpoints
- Use organized test structure with centralized imports
- Run coverage reports before committing

### Architecture Principles
- Follow Domain-Driven Design (DDD) patterns
- Keep domain logic pure and framework-agnostic
- Use dependency injection for repositories
- Separate middleware and error handling concerns
- Implement comprehensive logging and monitoring

### Git Workflow
- Use feature branches for development
- Write descriptive commit messages
- Include tests with new features
- Ensure all tests pass before merging
- Update documentation for new features

### Performance & Monitoring
- Use structured logging with request IDs
- Monitor slow requests (>1 second threshold)
- Include performance metrics in logs
- Set up proper error tracking and alerting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions or issues, please create an issue in the repository.

---

## 🚀 Recent Improvements

### Architecture Enhancements
- ✅ **Separated Middleware**: Modular CORS and logging middleware
- ✅ **Custom Error Handling**: Comprehensive exception handling with custom error types
- ✅ **Request Tracking**: Unique request IDs for better debugging
- ✅ **Performance Monitoring**: Built-in slow request detection

### Testing Improvements  
- ✅ **Organized Test Structure**: Clean imports using `__init__.py` files
- ✅ **Coverage Reporting**: 79.8% test coverage with HTML reports
- ✅ **Coverage Tooling**: Convenient script and configuration
- ✅ **Test Organization**: Separated unit and integration tests

### Development Experience
- ✅ **Structured Logging**: JSON-formatted logs with context
- ✅ **Coverage Scripts**: Easy-to-use coverage reporting tools
- ✅ **Git Ignore**: Comprehensive `.gitignore` for Python projects
- ✅ **Documentation**: Updated README with detailed guidance

### Code Quality
- ✅ **Type Safety**: Comprehensive type hints throughout
- ✅ **Clean Architecture**: Clear separation of concerns
- ✅ **Error Context**: Detailed error responses with tracking
- ✅ **Performance Metrics**: Request timing and monitoring 