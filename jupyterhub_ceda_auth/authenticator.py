"""
Custom Authenticator to use CEDA OAuth with JupyterHub.

Derived from the authenticators in oauthenticator.
"""

import os
import json
from urllib.parse import urlencode

from tornado import gen, web
from tornado.auth import OAuth2Mixin
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from oauthenticator.oauth2 import OAuthLoginHandler, OAuthCallbackHandler, OAuthenticator


CEDA_OAUTH_HOST = os.environ.get('CEDA_OAUTH_HOST', 'https://slcs.ceda.ac.uk')

class CedaOAuth2Mixin(OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = '{}/oauth/authorize'.format(CEDA_OAUTH_HOST)
    _OAUTH_ACCESS_TOKEN_URL = '{}/oauth/access_token'.format(CEDA_OAUTH_HOST)


class CedaLoginHandler(OAuthLoginHandler, CedaOAuth2Mixin):
    """
    Login handler that injects the profile scope.
    """
    scope = ['{}/oauth/profile/'.format(CEDA_OAUTH_HOST)]


class CedaOAuthenticator(OAuthenticator, CedaOAuth2Mixin):
    login_service = 'CEDA'
    login_handler = CedaLoginHandler

    @gen.coroutine
    def authenticate(self, handler, data = None):
        code = handler.get_argument("code", False)
        if not code:
            raise web.HTTPError(400, "oauth callback made without a token")

        http_client = AsyncHTTPClient()

        # Exchange the OAuth code for an access token
        req = HTTPRequest(
            self._OAUTH_ACCESS_TOKEN_URL,
            method = "POST",
            headers = { "Accept": "application/json" },
            body = urlencode({
                'client_id' : self.client_id,
                'client_secret' : self.client_secret,
                'code' : code,
                'grant_type' : "authorization_code",
                'redirect_uri' : self.oauth_callback_url,
            }).encode('utf-8')
        )
        resp = yield http_client.fetch(req)
        resp_json = json.loads(resp.body.decode('utf8', 'replace'))
        access_token = resp_json['access_token']

        # Determine who the logged in user is
        headers =
        req = HTTPRequest(
            "{}/oauth/profile/?access_token={}".format(CEDA_OAUTH_HOST, access_token),
            method = "GET",
            headers = { "Accept": "application/json" }
        )
        resp = yield http_client.fetch(req)
        resp_json = json.loads(resp.body.decode('utf8', 'replace'))
        return resp_json.get.get('profile', {}).get('accountid')