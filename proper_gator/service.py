import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ratelimit import limits, sleep_and_retry


def get_service(credentials):
    """Given a set of credentials, create a Resource object
    to interact with the Google Tag Manager v2 API

    :param credentials: The OAuth 2.0 credentials for the user
    :type credentials: google.oauth2.credentials.Credentials
    :return: A Resource object with methods for interacting with the tagmanager service
    :rtype: googleapiclient.discovery.Resource
    """
    service = build("tagmanager", "v2", credentials=credentials)

    return service


@sleep_and_retry
@limits(calls=15, period=60)
def execute(resource):
    try:
        resource.execute()
    except HttpError as err:
        error = json.loads(err.content)
        print(error)
