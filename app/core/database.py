from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Determine the database URL and ensure proper driver for PostgreSQL
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    # Convert to postgresql+psycopg for SQLAlchemy 2.0 with psycopg3
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

# Create engine
engine = create_engine(
    database_url,
    connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
    echo=False  # Set to True for SQL debugging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
