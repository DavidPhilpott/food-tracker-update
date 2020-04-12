from Sessions.AwsSession import AwsSession


class TestSession:

    def test_session_creates(self, test_state):
        session = AwsSession(test_state)
        assert session.session is not None


class TestClient:

    def test_client_creates(self, test_aws_session):
        client = test_aws_session.client("sns")
        assert client is not None


class TestResource:

    def test_resource_creates(self, test_aws_session):
        resource = test_aws_session.resource("s3")
        assert resource is not None
