# Migrations

## ✅ Step-by-Step: Set Up Alembic in Your FastAPI Project

### 1. **Install Alembic (if not already installed)**

```sh
pip install alembic
```

### 2. **Initialize Alembic**

In your project root directory:

```sh
alembic init alembic
```

This will create:

```sh
alembic/
  versions/
  env.py
alembic.ini
```

### 3. **Edit `alembic.ini`**

In the `[alembic]` section of `alembic.ini`, set the `sqlalchemy.url` to your database connection string.

For example:

```ini
sqlalchemy.url = postgresql+asyncpg://postgres:yourpassword@localhost:5432/yourdbname
```

> ❗️Note: Alembic uses **sync SQLAlchemy**, so if you're using `asyncpg`, you'll need to slightly adapt `env.py` later.

Alternatively, you can keep this blank and override it via an env var or programmatically in `env.py`.

### 4. **Modify `env.py` to use your models**

In `alembic/env.py`, add your models to the metadata. For example:

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from models import User  # or wherever your Base model is
from sqlmodel import SQLModel

# this is the Alembic Config object
config = context.config

fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata
```

### 5. **Generate the first revision**

Now that it's initialized and connected to your models:

```bash
alembic revision --autogenerate -m "add is_superuser to user"
```

### 6. **Apply the migration**

```bash
alembic upgrade head
```

Let me know if you want this adapted to your actual model layout (e.g., how you’ve defined `SQLModel.metadata`, or if you’re using async engine).
