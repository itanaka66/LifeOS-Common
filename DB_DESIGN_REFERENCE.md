# Database Design Reference for LifeOS Platform

## Overview

This document provides the comprehensive database design reference for the LifeOS platform, including core tables and plugin-specific schemas.

## Core Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Persons Table
```sql
CREATE TABLE persons (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Documents Table
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    title VARCHAR(255),
    file_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Plugins Registry
```sql
CREATE TABLE plugins (
    id UUID PRIMARY KEY,
    plugin_id VARCHAR(200) UNIQUE NOT NULL,
    version VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    installed_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Migration History
```sql
CREATE TABLE migration_history (
    id UUID PRIMARY KEY,
    plugin_id VARCHAR(200) NOT NULL,
    migration_id VARCHAR(200) NOT NULL,
    version VARCHAR(100) NOT NULL,
    operation VARCHAR(30) NOT NULL,
    checksum VARCHAR(128) NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    status VARCHAR(30) NOT NULL,
    error TEXT
);
```

## Migration System

### Migration Table Structure
The migration system tracks all database changes with:
- **plugin_id**: Identifier of the plugin that owns the migration
- **migration_id**: Unique identifier for this specific migration
- **version**: Version number of the migration
- **operation**: Type of operation (up, down)
- **checksum**: Hash of the migration content for verification
- **started_at**: When the migration started
- **completed_at**: When the migration completed
- **status**: Current status (pending, running, completed, failed)
- **error**: Error message if migration failed

### Migration Example (0001_initial.py)
```python
"""Initial migration for Core DB schema."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Users Table
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Persons Table
    op.create_table('persons',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Documents Table
    op.create_table('documents',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('file_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Plugin Registry
    op.create_table('plugins',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('plugin_id', sa.String(200), unique=True, nullable=False),
        sa.Column('version', sa.String(100), nullable=False),
        sa.Column('status', sa.String(30), nullable=False),
        sa.Column('enabled', sa.Boolean(), default=True),
        sa.Column('installed_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Migration History
    op.create_table('migration_history',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('plugin_id', sa.String(200), nullable=False),
        sa.Column('migration_id', sa.String(200), nullable=False),
        sa.Column('version', sa.String(100), nullable=False),
        sa.Column('operation', sa.String(30), nullable=False),
        sa.Column('checksum', sa.String(128), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(30), nullable=False),
        sa.Column('error', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('migration_history')
    op.drop_table('plugins')
    op.drop_table('documents')
    op.drop_table('persons')
    op.drop_table('users')
```

## Plugin-Specific Schemas

### Schema Naming Convention
Each plugin can define its own schema in a dedicated namespace:
```sql
-- Example: Finance Plugin Schema
CREATE SCHEMA lifeos_plugin_finance;

CREATE TABLE lifeos_plugin_finance.accounts (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(100),
    balance NUMERIC(15,2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Plugin Database Structure
Each plugin's database schema should include:
- **Plugin-specific tables** for the plugin's data
- **Foreign key relationships** to core tables where needed
- **Indexes** for performance optimization
- **Constraints** to maintain data integrity

## Indexing Strategy

### Core Table Indexes
```sql
-- Users table indexes
CREATE INDEX idx_users_email ON users(email);

-- Persons table indexes
CREATE INDEX idx_persons_name ON persons(name);
CREATE INDEX idx_persons_created_at ON persons(created_at);

-- Documents table indexes
CREATE INDEX idx_documents_title ON documents(title);
CREATE INDEX idx_documents_created_at ON documents(created_at);
```

### Plugin Table Indexes
Plugin tables should have appropriate indexes based on query patterns:
```sql
-- Example: Finance plugin transaction table index
CREATE INDEX idx_transactions_account_id ON lifeos_plugin_finance.transactions(account_id);
CREATE INDEX idx_transactions_date ON lifeos_plugin_finance.transactions(date);
CREATE INDEX idx_transactions_category ON lifeos_plugin_finance.transactions(category);
```

## Data Integrity and Constraints

### Foreign Key Relationships
- Persons linked to Users via user_id
- Documents linked to Users via owner_id
- Plugin tables referencing core tables as needed

### Data Validation
- Unique constraints on email addresses
- Not null constraints on required fields
- Check constraints for valid data ranges
- Default values for timestamp fields

## Performance Considerations

### Query Optimization
1. **Index Usage**: Create indexes on frequently queried columns
2. **Query Patterns**: Optimize queries based on usage patterns
3. **Pagination**: Implement pagination for large result sets
4. **Caching**: Use Redis for frequently accessed data

### Schema Design Best Practices
- Normalize tables to reduce redundancy
- Denormalize where performance is critical
- Use appropriate data types
- Implement proper constraints and validation
- Design for scalability from the beginning

## Backup and Recovery

### Database Backup Strategy
1. **Regular Automated Backups**: Daily full backups with incremental backups
2. **Point-in-Time Recovery**: WAL archiving for precise recovery points
3. **Cross-Region Replication**: Geographic redundancy for disaster recovery
4. **Version Control**: Database schema changes tracked in version control

### Migration Best Practices
1. **Rollback Procedures**: Always include downgrade migrations
2. **Data Validation**: Validate data integrity after migration
3. **Testing**: Test migrations on staging environment first
4. **Monitoring**: Monitor migration progress and errors