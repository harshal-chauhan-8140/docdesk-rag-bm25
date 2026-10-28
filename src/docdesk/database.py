from sqlalchemy import URL, Engine, create_engine

from docdesk.config import Settings


def build_engine(settings: Settings) -> Engine:
    """Create the application's PostgreSQL connection manager."""

    url = URL.create(
        drivername="postgresql+psycopg",
        username=settings.user,
        password=settings.password.get_secret_value(),
        host=settings.host,
        port=settings.port,
        database=settings.name,
    )

    return create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        pool_timeout=5,
        connect_args={
            "connect_timeout": 3,
            "options": "-c statement_timeout=3000",
        },
        hide_parameters=True,
    )
