.. AuthenticationAPI documentation master file, created by
   sphinx-quickstart on Fri Jun 21 11:33:33 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OAuth API's documentation!
=============================================

Welcome to the documentation for **OAuth API**. This API provides robust authentication functionalities to secure your application. 
Here’s a brief overview of the features and what users can expect from this API:

**Features**

* User Registration

*Endpoint: /register*

Description: Allows new users to register by providing a username, email, and password. Upon successful registration, 
a unique secret key and client ID are generated for the user.

* User Login

*Endpoint: /token*.

Description: Authenticates a user using their username and password, and returns an access token that can be used for subsequent requests.

* Account Activation

*Endpoint: /account-activation*.

Description: Activates a user's account using a token. This is typically part of an email verification process.

* Token Retrieval

*Endpoint: /retrieve-access-token*.

Description: Allows an authenticated user to retrieve a new access token if their current token has expired or is about to expire.

* User Details Retrieval

*Endpoint: /users/me/*.

Description: Returns the details of the currently authenticated user.

**What to Expect**

* *Secure Authentication:* All endpoints are designed with security best practices in mind, ensuring that user credentials and tokens are handled securely.

* *JWT Tokens:* The API uses JSON Web Tokens (JWT) for authentication. Tokens include an expiration time to enhance security.

* *Password Hashing:* User passwords are hashed using the bcrypt algorithm, providing a high level of security.

* *Ease of Use:* The endpoints are straightforward to use, with detailed response models to help integrate the API with your application seamlessly.

* *Error Handling:* Clear and descriptive error messages are provided to help diagnose issues quickly and accurately.

**How to Use**

* Register a New User: Call the */register* endpoint with a username, email, and password.
* Login: Use the */token* endpoint to authenticate the user and receive an access token.
* Activate Account: Use the */account-activation* endpoint to activate a user's account.
* Retrieve Token: Use the */retrieve-access-token* endpoint to get a new token if the old one expires.
* Fetch User Details: Use the */users/me/* endpoint to retrieve the current user's details.

*For more detailed information on each endpoint, refer to the specific sections in the documentation.*

Thank you for choosing OAuth API!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

