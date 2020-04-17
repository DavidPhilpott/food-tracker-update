from app.Providers.AwsParameterStoreProvider import AwsParameterStoreProvider


class TestInit:

    def test_provider_establishes_connection_correctly(self, test_logging_provider,
                                                       test_env_var_provider,
                                                       test_aws_session):
        provider = AwsParameterStoreProvider(logging_provider=test_logging_provider,
                                             env_var_provider=test_env_var_provider,
                                             aws_session=test_aws_session)
        assert provider._client is not None


class TestGetNonSecureString:

    def test_provider_can_retrieve_non_secret_correctly(self, test_aws_parameter_store_provider):
        retrieved_value = test_aws_parameter_store_provider.get_non_secure_string("Non_Secure_Test_Parameter")
        assert retrieved_value == 'Non Secure Test Value'


class TestGetSecureString:

    def test_provider_can_retrieve_non_secret_correctly(self, test_aws_parameter_store_provider):
        retrieved_value = test_aws_parameter_store_provider.get_secure_string("Secure_Test_Parameter")
        assert retrieved_value == 'Secure Test Value'
