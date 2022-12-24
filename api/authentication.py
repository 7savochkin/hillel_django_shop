from rest_framework.authentication import \
    TokenAuthentication as RestTokenAuthentication


class TokenAuthentication(RestTokenAuthentication):
    keyword = 'Bearer'
