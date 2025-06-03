# TrendSpotter

TrendSpotter is a web application that identifies and displays trending topics. It consists of a client (frontend) and a server (backend).

## Project Structure

The project is structured as follows:

- `client/`: Contains the frontend code, built with Flask.
  - `main.py`: Main application file for the client.
  - `static/`: Contains static assets such as CSS, images, and fonts.
  - `templates/`: Contains HTML templates for the client.
- `server/`: Contains the backend code.
  - `a.py`:
  - `generate_query_ant.py`:
  - `search_linkedin_posts.py`:
  - `app/`: Contains the backend application code.
    - `main.py`: Main application file for the server.
    - `static/`: Contains static assets such as CSS, images, and fonts.
    - `templates/`: Contains HTML templates for the server.

## Running the Application

### Running the Client (Frontend)

1.  Navigate to the `client/` directory:

    ```bash
    cd client
    ```

2.  Run the client application:

    ```bash
    python main.py
    ```

### Running the Server (Backend)

1.  Navigate to the `server/app/` directory:

    ```bash
    cd server/app
    ```

2.  Run the server application:

    ```bash
    python main.py
    ```

## Dependencies

- Flask
- Other dependencies (check `requirements.txt` if available)

## Additional Information

Add any other relevant information here, such as API keys, configuration details, or deployment instructions.
