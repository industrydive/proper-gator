import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/tagmanager.edit.containers"]


def get_credentials():
    """Read credentials from token.json if it exists.
    If token.json does not exist, try to refresh expired credentials.
    If credentials are completely missing, allow the user to login via
    console using OAuth 2.0

    :return: The OAuth 2.0 credentials for the user
    :rtype: google.oauth2.credentials.Credentials
    """
    credentials = None

    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", SCOPES
            )
            credentials = flow.run_console()
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    return credentials
