from src.core.config import Settings


def test_config_fixture_is_correct(test_settings: Settings):
    """
    Verifica que el fixture de configuración en integration/conftest.py
    está devolviendo los valores de prueba esperados.
    """
    assert test_settings.PROJECT_NAME == "ScoreFlow API - Test Environment"
    assert "postgres_test" in test_settings.DATABASE_URL
    assert "scoreflow_test" in test_settings.DATABASE_URL
    assert test_settings.DEBUG is True
