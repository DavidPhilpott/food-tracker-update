import boto3


class AwsSession:
    def __init__(self, state):
        self.session = None
        self._region_name = state.get("DEFAULT_AWS_REGION")
        self._client_details = {
            "region_name": self._region_name,
        }
        self._create_session()
        return

    def _create_session(self):
        self.session = boto3.session.Session()
        return

    def resource(self, service):
        current_client_details = {"service_name": service}
        current_client_details.update(self._client_details)
        resource = self.session.resource(**current_client_details)
        return resource

    def client(self, service):
        current_client_details = {"service_name": service}
        current_client_details.update(self._client_details)
        client = self.session.client(**current_client_details)
        return client
