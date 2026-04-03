import pytest
from src.core.config import Settings


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """
    Fixture que proporciona una instancia de Settings configurada específicamente
    para entornos de prueba, evitando el uso del archivo .env de desarrollo.
    """
    return Settings(
        PROJECT_NAME="ScoreFlow API - Test Environment",
        POSTGRES_USER="postgres_test",
        POSTGRES_PASSWORD="password_test",
        POSTGRES_SERVER="localhost",
        POSTGRES_PORT=5432,
        POSTGRES_DB="scoreflow_test",
        DEBUG=True,
        _env_file=None,  # Evita cargar el archivo .env real
    )
