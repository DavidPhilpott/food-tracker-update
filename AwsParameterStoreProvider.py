
class AwsParameterStoreProvider:
    def __init__(self, env_var_provider, aws_session):
        self.client = None
        self.env_vars = env_var_provider
        self.aws_session = aws_session

        self._open_client()
        return

    def _open_client(self):
        client = self.aws_session.client('ssm')
        self.client = client

    def get_non_secure_string(self, variable_name):
        response = self.client.get_parameter(
            Name=variable_name,
            WithDecryption=False)
        return response['Parameter']['Value']

    def get_secure_string(self, variable_name):
        response = self.client.get_parameter(
            Name=variable_name,
            WithDecryption=True)
        return response['Parameter']['Value']
