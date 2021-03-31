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


# Google limits us to 15 calls per minute (60 seconds)
API_CALLS = 15
API_PERIOD = 60


@sleep_and_retry
@limits(calls=API_CALLS, period=API_PERIOD)
def execute(resource):
    """A helper function to call the execute method of Google API resources.
    Wraps with a sleep_and_retry + limits decorator from ratelimit

    :param resource: A resource object from Google API
    :type resource: googleapiclient.discovery.Resource
    :return: A dict representing the response from the Google API
    :rtype: dict
    """
    try:
        return resource.execute()
    except HttpError as err:
        error = json.loads(err.content)
        print(error)
