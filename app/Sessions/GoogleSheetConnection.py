from oauth2client.service_account import ServiceAccountCredentials
import gspread


class GoogleSheetConnection:
    def __init__(self, state):
        self._state = state
        self.__authentication_details = self.__extract_authentication_details()
        self.connection = None
        self.__open_connection()
        return

    def __extract_authentication_details(self):
        self._state.debug(__name__, "Extracting Google Sheet authentication information...")
        authentication_details = {
            "type": self._state.get("google_auth_type"),
            "project_id": self._state.get("google_auth_project_id"),
            "private_key_id": self._state.get("google_auth_private_key_id"),
            "private_key": self._state.get("google_auth_private_key"),
            "client_email": self._state.get("google_auth_client_email"),
            "client_id": self._state.get("google_auth_client_id"),
            "auth_uri": self._state.get("google_auth_auth_uri"),
            "token_uri": self._state.get("google_auth_token_uri"),
            "auth_provider_x509_cert_url": self._state.get("google_auth_auth_provider_x509_cert_url"),
            "client_x509_cert_url": self._state.get("google_auth_client_x509_cert_url")
        }
        return authentication_details

    def __open_connection(self):
        self._state.debug(__name__, "Opening connection to Google Sheets...")
        service_scope = ['https://spreadsheets.google.com/feeds',
                         'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.__authentication_details, service_scope)
        self.connection = gspread.authorize(credentials)
        pass

