from AwsParameterStoreProvider import AwsParameterStoreProvider


class TestInit:

    def test_provider_establishes_connection_correctly(self, test_env_var_provider, test_aws_session):
        provider = AwsParameterStoreProvider(test_env_var_provider, test_aws_session)
        assert provider.client is not None


class TestGetNonSecureString:

    def test_provider_can_retrieve_non_secret_correctly(self, test_aws_parameter_store_provider):
        retrieved_value = test_aws_parameter_store_provider.get_non_secure_string("Non_Secure_Test_Parameter")
        assert retrieved_value == 'Non Secure Test Value'


class TestGetSecureString:

    def test_provider_can_retrieve_non_secret_correctly(self, test_aws_parameter_store_provider):
        retrieved_value = test_aws_parameter_store_provider.get_secure_string("Secure_Test_Parameter")
        assert retrieved_value == 'Secure Test Value'
