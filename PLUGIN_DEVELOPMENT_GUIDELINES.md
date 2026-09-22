# Plugin Development Guidelines for LifeOS Platform

## Overview

This document provides comprehensive guidelines for developing plugins for the LifeOS platform. These guidelines ensure consistency, security, and maintainability across all plugins while allowing for innovation and extensibility.

## Getting Started

### 1. Prerequisites
Before beginning plugin development, ensure you have:
- Python 3.9 or higher
- PostgreSQL 13 or higher
- Docker (for containerized deployment)
- Git for version control
- Basic understanding of the platform architecture

### 2. Development Environment Setup
```bash
# Clone the repository
git clone https://github.com/platform/project.git
cd project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Plugin Structure
Each plugin should follow this standardized structure:
```
plugin-name/
├── manifest.yaml          # Plugin metadata and requirements
├── plugin.py              # Main plugin implementation
├── migrations/            # Database migration files
│   └── versions/
│       ├── 0001_initial.py
│       └── ...
├── api/                   # API endpoints
│   └── v1/
│       ├── __init__.py
│       └── endpoints.py
├── models/                # Data models
│   ├── __init__.py
│   └── entities.py
├── services/              # Business logic
│   ├── __init__.py
│   └── service.py
├── static/                # Static assets (UI, etc.)
│   └── ui/
├── tests/                 # Test files
│   └── test_plugin.py
├── requirements.txt       # Plugin-specific dependencies
└── README.md              # Documentation
```

## Plugin Manifest File

The manifest file (`manifest.yaml`) is crucial for plugin registration and compatibility checking:

```yaml
id: lifeos.finance

version: 2.1.0

core:
  min_version: 1.5.0
  max_version: "<3.0.0"

database:
  schema: lifeos_plugin_finance
  migration:
    engine: alembic
    path: migrations
    current: 0004

dependencies:
  required:
    - lifeos.core
  optional:
    - lifeos.receipt
    - lifeos.salary

permissions:
  - finance.read
  - finance.write

entities:
  - Account
  - Transaction
  - Budget

ui:
  menu:
    label: 家計簿
    icon: money
    order: 50

ai:
  tools:
    - search_transactions
    - get_monthly_expenses
    - categorize_transaction

metadata:
  author: "LifeOS Team"
  description: "A comprehensive financial management plugin for LifeOS"
  homepage: "https://lifeos.io/plugins/finance"
  license: "MIT"
```

## Plugin Implementation Requirements

### 1. Core Interface Implementation
All plugins must implement the `PluginInterface` defined in the common library:

```python
# plugin.py
from common.plugin_interface import PluginInterface
from common.plugin_config import PluginConfig
import logging

class SamplePlugin(PluginInterface):
    """Sample plugin implementation."""
    
    def __init__(self):
        self._id = "sample.plugin"
        self._version = "1.0.0"
        self._name = "Sample Plugin"
        self._config = None
        self._logger = logging.getLogger(__name__)
        
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def version(self) -> str:
        return self._version
    
    @property
    def name(self) -> str:
        return self._name
    
    def initialize(self, config: dict) -> None:
        """Initialize the plugin."""
        self._config = PluginConfig(**config)
        self._logger.info(f"Plugin initialized with config: {config}")
    
    def get_manifest(self) -> dict:
        """Get plugin manifest."""
        return {
            "id": self._id,
            "version": self._version,
            "name": self._name,
            "description": "A sample plugin for demonstration",
            "min_version": "1.0.0"
        }
    
    def get_endpoints(self) -> list:
        """Get API endpoints."""
        return [
            {
                "path": "/sample/health",
                "method": "GET",
                "handler": self.health_check
            },
            {
                "path": "/sample/data",
                "method": "POST",
                "handler": self.create_data
            }
        ]
    
    def get_entities(self) -> list:
        """Get entities provided."""
        return ["DataItem", "Record"]
    
    def get_permissions(self) -> list:
        """Get required permissions."""
        return ["sample.read", "sample.write"]
    
    def start(self) -> bool:
        """Start the plugin."""
        self._logger.info("Starting Sample plugin")
        return True
    
    def stop(self) -> bool:
        """Stop the plugin."""
        self._logger.info("Stopping Sample plugin")
        return True
    
    def cleanup(self) -> None:
        """Clean up resources."""
        self._logger.info("Cleaning up Sample plugin")
```

### 2. API Endpoint Design
API endpoints must follow REST conventions:

```python
# api/v1/endpoints.py
from flask import jsonify, request
from lifeos_common.decorators import require_permission

class FinanceEndpoints:
    def __init__(self, service):
        self.service = service
    
    @require_permission("finance.read")
    def get_accounts(self):
        """Get all accounts."""
        accounts = self.service.get_accounts()
        return jsonify({"data": accounts})
    
    @require_permission("finance.write")
    def create_account(self):
        """Create a new account."""
        data = request.json
        account = self.service.create_account(data)
        return jsonify({"data": account}), 201
    
    def health_check(self):
        """Health check endpoint."""
        return jsonify({"status": "healthy", "plugin": "Finance"})
```

### 3. Data Models
Data models should be consistent with the platform's data standards:

```python
# models/entities.py
from common.data_models import BaseModel
from uuid import UUID
from datetime import datetime

class DataItem(BaseModel):
    """Sample data item model."""
    
    def __init__(self, id: UUID = None, name: str = "", type: str = "", 
                 value: float = 0.0, created_at: datetime = None, 
                 updated_at: datetime = None):
        self.id = id
        self.name = name
        self.type = type
        self.value = value
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.type,
            "value": self.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def from_dict(self, data: dict) -> None:
        """Initialize model from dictionary."""
        self.id = UUID(data["id"]) if data.get("id") else None
        self.name = data.get("name", "")
        self.type = data.get("type", "")
        self.value = data.get("value", 0.0)
        self.created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        self.updated_at = datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None
```

## Database Migration Strategy

### 1. Migration Files
All database changes should be implemented through migrations:

```python
# migrations/versions/0001_initial.py
"""Initial migration for Finance plugin schema."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create finance-specific tables
    op.create_table('accounts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('type', sa.String(100), nullable=True),
        sa.Column('balance', sa.Numeric(15,2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('transactions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('account_id', sa.UUID(), nullable=False),
        sa.Column('amount', sa.Numeric(15,2), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('transactions')
    op.drop_table('accounts')
```

### 2. Migration Best Practices
- Always include both `upgrade()` and `downgrade()` functions
- Test migrations on staging environment first
- Ensure rollback procedures are functional
- Validate data integrity after migration
- Include checksums for verification

## Security Guidelines

### 1. Input Validation
All inputs must be validated:
```python
def validate_data(data):
    """Validate plugin data."""
    errors = []
    
    if not data.get('name'):
        errors.append("Name is required")
    
    if not data.get('type'):
        errors.append("Type is required")
    
    if 'value' in data and data['value'] < 0:
        errors.append("Value cannot be negative")
    
    return errors
```

### 2. Authentication and Authorization
- Use existing authentication system
- Implement proper permission checks
- Log security-related events
- Validate all API requests

### 3. Data Protection
- Encrypt sensitive data at rest
- Use HTTPS for all communications
- Sanitize user inputs to prevent injection attacks
- Implement proper session management

## Performance Considerations

### 1. Database Optimization
- Create appropriate indexes on frequently queried columns
- Use connection pooling
- Implement pagination for large result sets
- Optimize queries with EXPLAIN ANALYZE

### 2. Caching Strategy
```python
from lifeos_common.cache import cache

@cache.memoize(timeout=300)
def get_account_summary(account_id):
    """Get account summary with caching."""
    # Expensive database query here
    pass
```

### 3. Asynchronous Processing
For long-running operations:
```python
from celery import Celery

celery = Celery('finance_plugin')

@celery.task
def process_large_transaction_batch(transactions):
    """Process large batch of transactions asynchronously."""
    # Heavy processing here
    pass
```

## Testing Requirements

### 1. Unit Tests
All functions must have unit tests:
```python
# tests/test_finance.py
import unittest
from plugin import FinancePlugin

class TestFinancePlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = FinancePlugin()
    
    def test_plugin_initialization(self):
        """Test plugin initialization."""
        self.assertEqual(self.plugin.id, "lifeos.finance")
        self.assertEqual(self.plugin.version, "2.1.0")
    
    def test_get_endpoints(self):
        """Test endpoint retrieval."""
        endpoints = self.plugin.get_endpoints()
        self.assertIsInstance(endpoints, list)
        self.assertTrue(len(endpoints) > 0)
```

### 2. Integration Tests
Test plugin integration with core system:
- Database connection tests
- API endpoint functionality
- Event bus integration
- Permission checks

### 3. Performance Tests
- Load testing with synthetic users
- Response time measurements
- Resource utilization tracking

## Documentation Standards

### 1. README.md Requirements
Each plugin must include a comprehensive README file with:
- Plugin description and features
- Installation instructions
- Configuration options
- API documentation
- Usage examples
- Troubleshooting guide

### 2. Code Documentation
- Document all public methods with docstrings
- Include parameter descriptions
- Explain return values
- Provide usage examples where appropriate

### 3. API Documentation
Use OpenAPI/Swagger for API documentation:
```yaml
openapi: "3.0.0"
info:
  title: "Finance Plugin API"
  version: "2.1.0"

paths:
  /finance/accounts:
    get:
      summary: "Get all accounts"
      responses:
        200:
          description: "List of accounts"
```

## Versioning Strategy

### 1. Semantic Versioning
Follow semantic versioning principles:
- MAJOR version for breaking changes
- MINOR version for new features (backward compatible)
- PATCH version for bug fixes (backward compatible)

### 2. Compatibility Matrix
Maintain a compatibility matrix showing which plugin versions work with which core platform versions.

## Deployment Process

### 1. Build Pipeline
- Automated testing on every commit
- Code quality checks
- Security scanning
- Package creation

### 2. Release Process
- Create release tags
- Update changelog
- Publish to package repository
- Notify users of new releases

### 3. Rollback Procedures
- Maintain backup of previous versions
- Document rollback steps
- Test rollback procedures regularly

## Quality Assurance

### 1. Code Reviews
All code changes must be reviewed by at least one other developer before merging.

### 2. Automated Testing
Implement comprehensive automated testing:
- Unit tests (80%+ coverage)
- Integration tests
- Performance tests
- Security tests

### 3. Continuous Integration
- Run tests automatically on every commit
- Monitor code quality metrics
- Check for security vulnerabilities
- Verify build process works correctly

## Best Practices Summary

### 1. Code Quality
- Follow PEP8 style guide
- Use type hints where appropriate
- Write clean, readable code
- Avoid code duplication

### 2. Error Handling
- Implement proper error handling
- Provide meaningful error messages
- Log errors appropriately
- Don't expose sensitive information in error responses

### 3. Logging
- Use structured logging
- Include relevant context in log messages
- Set appropriate log levels
- Rotate logs to prevent disk space issues

### 4. Configuration
- Externalize configuration
- Support environment variables
- Provide sensible defaults
- Validate configuration at startup

This comprehensive set of guidelines ensures that all plugins developed for the LifeOS platform are consistent, secure, performant, and maintainable.