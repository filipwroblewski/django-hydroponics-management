# django-hydroponics-management

🌱💧A Django-based application to manage hydroponic systems with full CRUD capabilities, sensor data management, and user authentication.

# Description

Django Hydroponics Management is a web application built with Django and Django REST Framework that allows users to manage hydroponic systems and sensor data. It provides endpoints for CRUD operations on hydroponic systems and sensor measurements, user authentication, and more.

# Installation

Follow these steps to set up and run the application locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/filipwroblewski/django-hydroponics-management.git
   ```

2. Navigate to the project directory:

   ```bash
   cd django-hydroponics-management
   ```

3. Create a .env file in the root directory and add the following variables:

   ```
   POSTGRES_DB=<your_database_name>
   POSTGRES_USER=<your_database_user>
   POSTGRES_PASSWORD=<your_database_password>
   POSTGRES_HOST=db
   ```

   Replace `<your_database_name>`, `<your_database_user>`, and `<your_database_password>` with your own values.

   **Note**: The `.env` file is used to store environment variables that are specific for local development environment. This file should not be committed to version control. The `.env` should be listed in `.gitignore` file.

# Configuration

Make sure Docker and Docker Compose are installed on your machine. You can download Docker from the [official Docker website](https://docs.docker.com/get-docker/).

# Running the Application

Once everything is set up, you can run the application with Docker using the following commands:

1. Build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

   This command will:

   - Build the Docker images as specified in the Dockerfile.
   - Start the services defined in docker-compose.yml.

2. Apply database migrations:

   After the containers are up and running, apply the Django migrations to set up your database schema:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. Create a superuser:

   To create a Django superuser for accessing the admin interface, run:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. Access application:

   | Description                   | URL                                                        |
   | ----------------------------- | ---------------------------------------------------------- |
   | Access application            | [http://localhost:8000](http://localhost:8000)             |
   | Access Django admin interface | [http://localhost:8000/admin](http://localhost:8000/admin) |

# Stopping the Application

To stop the application, run:

```bash
docker-compose down
```

This command will stop and remove the containers, but the data in the PostgreSQL volume will be preserved.

# License

This project is licensed under the [MIT License](https://github.com/filipwroblewski/django-hydroponics-management/blob/main/LICENSE).
