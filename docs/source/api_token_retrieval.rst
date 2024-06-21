.. _api_token_retrieval:

Token Retrieval
===============

This endpoint allows users to retrieve a new access token.

**Endpoint:** /retrieve-access-token

**Response Model:**

.. autoclass:: authAPI.main.GeneralResponseModel
   :members:
   :noindex:

**Implementation:**

.. autofunction:: authAPI.main.retrieve_access_token
   :noindex:
