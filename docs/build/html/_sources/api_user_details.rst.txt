.. _api_user_details:

User Details
============

This endpoint allows users to retrieve their details.

**Endpoint:** /users/me/

**Response Model:**

.. autoclass:: authAPI.main.User
   :members:
   :noindex:

**Implementation:**

.. autofunction:: authAPI.main.read_users_me
   :noindex:
