# AuthenticationAPI

## Overview

The `AuthenticationAPI` provides endpoints for user authentication functionalities including registration, login, account activation, token retrieval, and user details retrieval. This API is built using FastAPI and integrates JWT for secure token-based authentication.

## Features

- **User Registration:** Allows new users to register and create an account.
- **User Login:** Provides an access token upon successful authentication.
- **Account Activation:** Activates user accounts using an access token.
- **Token Retrieval:** Generates a new access token upon authorization.
- **User Details Retrieval:** Fetches details of the authorized user.

## Endpoints

### User Registration
- **Endpoint:** `/register`
- **Method:** `POST`
- **Description:** Registers a new user and returns a response with user details and a secret key.

### User Login
- **Endpoint:** `/token`
- **Method:** `POST`
- **Description:** Authenticates the user and returns an access token.

### Account Activation
- **Endpoint:** `/account-activation`
- **Method:** `POST`
- **Description:** Activates the user's account using a provided token.

### Token Retrieval
- **Endpoint:** `/retrieve-access-token`
- **Method:** `GET`
- **Description:** Retrieves a new access token for the authorized user.

### User Details Retrieval
- **Endpoint:** `/users/me/`
- **Method:** `GET`
- **Description:** Fetches the current authorized user's details.

## Installation

### Prerequisites
- Python 3.7+
- FastAPI
- SQLAlchemy
- Uvicorn

### Steps

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    uvicorn authAPI.main:app --reload
    ```

## Documentation

The full API documentation is generated using Sphinx and is available online. You can also build and view the documentation locally.

### Online Documentation

The documentation is hosted on Netlify and can be accessed [here](<Netlify-URL>).

### Building Documentation Locally

1. Navigate to the `docs` folder:
    ```sh
    cd docs
    ```

2. Build the HTML documentation using Sphinx:
    ```sh
    sphinx-build -b html source build/html
    ```

3. Open the documentation in your browser:
    ```sh
    open build/html/index.html  # On Windows: start build/html/index.html
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING](CONTRIBUTING.md) guidelines before submitting a pull request.

## Contact

For any questions or feedback, please contact [your-email@example.com].

