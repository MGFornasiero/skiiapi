# SKI Karate API

A FastAPI application providing a comprehensive RESTful API for a Shotokan Karate database. This API serves detailed information on grades (Kyu/Dan), Kihon (basics), Kata (forms), individual techniques, and more.
Necessita della variabile d'ambiente SKIURI con l'URI del db postgres

## Features

-   **Detailed Data Retrieval**: Access structured data for Katas, Kihons, and grading requirements.
-   **Component Information**: Get specific details about techniques, stances, striking parts, and targets.
-   **Inventory Lists**: Enumerate all available entities like Katas, grades, techniques, etc.
-   **Full-Text Search**: A powerful search endpoint to find relevant information across the entire database.
-   **Auto-generated Documentation**: Interactive API documentation provided by FastAPI (Swagger UI and ReDoc).

## Setup and Installation

### Prerequisites

-   Python 3.8+
-   PostgreSQL Server
-   A running instance of the SKI-DB database, which this API connects to.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd skiiapi
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Install all required packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the Database Connection:**
    The application connects to the PostgreSQL database using a connection URI. This must be provided via an environment variable named `SKIURI`.

    **On Linux/macOS:**
    ```bash
    export SKIURI="postgresql://username:password@hostname:5432/database_name"
    ```

    **On Windows (Command Prompt):**
    ```bash
    set SKIURI="postgresql://username:password@hostname:5432/database_name"
    ```

    **On Windows (PowerShell):**
    ```powershell
    $env:SKIURI="postgresql://username:password@hostname:5432/database_name"
    ```

## Running the Application

Once the setup is complete, you can run the API server from the project's root directory (`skiiapi/`) using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The `--reload` flag enables hot-reloading, which automatically restarts the server when code changes are detected, which is very useful for development.

The API will then be available at `http://127.0.0.1:8000`.

## API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at the following URLs:

-   **Swagger UI**: `http://127.0.0.1:8000/docs`
-   **ReDoc**: `http://127.0.0.1:8000/redoc`

## API Endpoints

Here is a summary of the available endpoints.

### General

-   `GET /`: Root endpoint to check if the API is running.

### Grades & Inventories

-   `GET /grade_id/{gradetype}/{grade}`: Retrieves the unique ID for a specific grade (e.g., `/grade_id/dan/1`).
-   `GET /grade_inventory`: Lists all available grades (Kyu and Dan) and their IDs.
-   `GET /kata_inventory`: Lists all available Katas and their IDs.
-   `GET /technic_inventory`: Provides a complete inventory of all techniques.
-   `GET /stand_inventory`: Provides a complete inventory of all stands.
-   `GET /strikingparts_inventory`: Provides a complete inventory of all striking parts.
-   `GET /target_inventory`: Provides a complete inventory of all targets.

### Kihon (Basics)

-   `GET /numberofkihon/{grade_id}`: Gets the total number of Kihon sequences for a given grade ID.
-   `GET /kihon_list/{grade_id}/{sequenza}`: Retrieves a detailed breakdown of a specific Kihon sequence, including all steps and transitions.
-   `GET /kihons/{grade_id}`: Retrieves a formatted list of all Kihon steps for a given grade.

### Kata (Forms)

-   `GET /kata/{kata_id}`: Retrieves a detailed breakdown of a specific Kata, including all steps, techniques per step, and transitions.

### Information Retrieval

-   `GET /info_technic/{item_id}`: Retrieves detailed information for a single technique by its ID.
-   `GET /info_stand/{item_id}`: Retrieves detailed information for a single stand by its ID.
-   `GET /info_strikingparts/{item_id}`: Retrieves detailed information for a single striking part by its ID.
-   `GET /info_target/{item_id}`: Retrieves detailed information for a single target by its ID.

### Search

-   `GET /finder?search={query}`: Performs a full-text search across techniques, stands, targets, and striking parts. Returns ranked results based on relevance (e.g., `/finder?search=mae%20geri`).
-   `GET /findernew?search={query}`: An alternative search endpoint.

### create docker file and deploy
1) create docker file
docker build -t skiiapi .
docker tag skiiapi:latest europe-west12-docker.pkg.dev/eng-hangar-343507/cloud-run-source-deploy/skiiapi:latest (esempio con mio artifactory)
docker push europe-west12-docker.pkg.dev/eng-hangar-343507/cloud-run-source-deploy/skiiapi:latest