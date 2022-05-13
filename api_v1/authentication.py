from rest_framework.authentication import TokenAuthentication


class TokenAuthWithQueryString(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://{API_URI}/?API_KEY={API_TOKEN_KEY}"
    """
    def authenticate(self, request):
        # Check if 'token_auth' is in the request query params.
        # Give precedence to 'Authorization' header.
        print(request.GET)
        if 'API_KEY' in request.GET and \
                'HTTP_AUTHORIZATION' not in request.META:
            return self.authenticate_credentials(request.GET['API_KEY'])
        else:
            return super(TokenAuthWithQueryString, self).authenticate(request)
