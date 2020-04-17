from app.Providers.EnvVarProvider import EnvVarProvider
import pytest


class TestGetVar:
    def test_get_variable_from_env(self, monkeypatch, test_logging_provider):
        monkeypatch.setenv("test variable", "test value")
        provider = EnvVarProvider(test_logging_provider)
        test_value = provider.get_var("test variable")
        assert test_value == "test value"

    def test_get_variable_throws_error_for_missing_var(self, test_logging_provider):
        provider = EnvVarProvider(test_logging_provider)
        with pytest.raises(KeyError) as exc_info:
            provider.get_var("Random var that shouldn't exist on os")
        assert exc_info is not None
