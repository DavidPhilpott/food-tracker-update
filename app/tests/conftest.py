import pytest
from app.State import State
from app.tests.mock_interfaces.mock_EnvVarProvider import MockEnvVarProvider
from app.Sessions.GoogleSheetConnection import GoogleSheetConnection
from app.Sessions.GoogleWorksheetSession import GoogleWorksheetSession
from app.Sessions.AwsSession import AwsSession
from app.Providers.AwsParameterStoreProvider import AwsParameterStoreProvider
from app.Providers.LoggingProvider import LoggingProvider


@pytest.fixture
def test_state():
    test_state = State(env_var_provider=MockEnvVarProvider(),
                       aws_parameter_store_provider=AwsParameterStoreProvider(MockEnvVarProvider()),
                       logging_provider=LoggingProvider())
    return test_state


@pytest.fixture
def google_sheet_connection(test_state):
    google_sheet_connection = GoogleSheetConnection(test_state)
    return google_sheet_connection


@pytest.fixture
def test_worksheet_session(test_state, google_sheet_connection):
    spreadsheet_name = 'IntegrationTest'
    worksheet_name = "Sheet1"
    test_worksheet_session = GoogleWorksheetSession(test_state, google_sheet_connection,
                                                    spreadsheet_name, worksheet_name)
    return test_worksheet_session


@pytest.fixture
def test_worksheet_write_session(test_state, google_sheet_connection):
    spreadsheet_name = 'IntegrationTest'
    worksheet_name = "PutTest"
    test_worksheet_write_session = GoogleWorksheetSession(test_state, google_sheet_connection,
                                                          spreadsheet_name, worksheet_name)
    return test_worksheet_write_session


@pytest.fixture
def test_aws_session(test_state):
    test_session = AwsSession(test_state)
    return test_session


@pytest.fixture
def test_env_var_provider():
    test_env_var_provider = MockEnvVarProvider()
    return test_env_var_provider


@pytest.fixture
def test_aws_parameter_store_provider(test_env_var_provider, test_aws_session):
    test_aws_parameter_store_provider = AwsParameterStoreProvider(env_var_provider=test_env_var_provider,
                                                                  aws_session=test_aws_session)
    return test_aws_parameter_store_provider


@pytest.fixture
def test_logging_provider():
    test_logging_provider = LoggingProvider()
    return test_logging_provider
