import boto3


class AwsParameterStoreProvider:
    def __init__(self, env_var_provider, aws_session=None):
        self._client = None
        self._env_var_provider = env_var_provider
        self._aws_session = aws_session
        if aws_session is None:
            self._aws_session = self._open_own_session()
        self._open_client()
        return

    def _open_own_session(self):
        self._region_name = self._env_var_provider.get_var("DEFAULT_AWS_REGION")
        self._client_details = {
            "region_name": self._region_name,
        }
        return boto3.session.Session()

    def _open_client(self):
        client = self._aws_session.client('ssm')
        self._client = client

    def get_non_secure_string(self, variable_name):
        response = self._client.get_parameter(
            Name=variable_name,
            WithDecryption=False)
        return response['Parameter']['Value']

    def get_secure_string(self, variable_name):
        response = self._client.get_parameter(
            Name=variable_name,
            WithDecryption=True)
        return response['Parameter']['Value']

    def get_secure_pem_key(self, variable_name):
        pem_key = self.get_secure_string(variable_name)
        pem_key = pem_key.replace("\\n", "\n")
        return pem_key
