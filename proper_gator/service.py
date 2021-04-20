import json
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pyrate_limiter import Duration, Limiter, RequestRate

per_minute_rate = RequestRate(15, Duration.MINUTE)
per_day_rate = RequestRate(10000, Duration.DAY)

limiter = Limiter(per_minute_rate, per_day_rate)
identity = "GTM_api"


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


@limiter.ratelimit(identity, delay=True)
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
        if error["error"]["code"] == 429:
            print("Retrying...")
            # HACK: sometimes the API will return a 429 even with our limiting.
            # If that happens, just sleep for a minute and retry :(
            print("Sleeping :)")
            time.sleep(61)
            return resource.execute()
