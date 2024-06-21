.. Registration Endpoint
.. =====================

.. This endpoint allows users to register.

.. .. automodule:: authAPI.main
..     :members:
..     :undoc-members:
..     :show-inheritance:
..     :exclude-members: GeneralResponseModel

.. _api_registration:

User Registration
=================

This endpoint allows users to register.

**Endpoint:** /register

**Response Model:**

.. autoclass:: authAPI.main.RegistrationResponseModel
   :members:
   :noindex:

**Implementation:**

.. autofunction:: authAPI.main.register_user
   :noindex:
