from EnvVarProvider import EnvVarProvider
import pytest


class TestVariablesProvider:
    def test_get_variable_from_env(self, monkeypatch):
        monkeypatch.setenv("test variable", "test value")
        provider = EnvVarProvider()
        test_value = provider.get_var("test variable")
        assert test_value == "test value"

    def test_get_variable_throws_error_for_missing_var(self):
        provider = EnvVarProvider()
        with pytest.raises(KeyError) as exc_info:
            provider.get_var("Random var that shouldn't exist on os")
        assert exc_info is not None