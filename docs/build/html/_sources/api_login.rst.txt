.. _api_login:

User Login
==========

This endpoint allows users to login and obtain an access token.

**Endpoint:** /token

**Response Model:**

.. autoclass:: authAPI.main.Token
   :members:
   :noindex:

**Implementation:**

.. autofunction:: authAPI.main.login_for_access_token
   :noindex:
