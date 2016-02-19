import base64

from django.contrib.auth import authenticate


def base_auth(authorization_header):
    """
        Authenticates user based on "HTTP_AUTHORIZATION" header values for
            HTTP basic authorization purposes.
    """

    authmeth, auth = authorization_header.split(' ', 1)
    if authmeth.lower() == 'basic':
        auth = base64.b64decode(auth.strip()).decode('utf8')
        username, password = auth.split(':', 1)
        user = authenticate(username=username, password=password)
        return user
    else:
        return None
