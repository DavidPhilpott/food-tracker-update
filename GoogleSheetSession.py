import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread


class GoogleSheetSession:
    def __init__(self, state):
        self.__authentication_details = {
            "type": state.get("google_auth_type"),
            "project_id": state.get("google_auth_project_id"),
            "private_key_id": state.get("google_auth_private_key_id"),
            "private_key": state.get("google_auth_private_key"),
            "client_email": state.get("google_auth_client_email"),
            "client_id": state.get("google_auth_client_id"),
            "auth_uri": state.get("google_auth_auth_uri"),
            "token_uri": state.get("google_auth_token_uri"),
            "auth_provider_x509_cert_url": state.get("google_auth_auth_provider_x509_cert_url"),
            "client_x509_cert_url": state.get("google_auth_client_x509_cert_url")
        }
        self.connection = None
        self.__open_session()
        return

    def __open_session(self):
        service_scope = ['https://spreadsheets.google.com/feeds',
                         'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.__authentication_details, service_scope)
        self.connection = gspread.authorize(credentials)
        pass

