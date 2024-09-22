# Development of a Hydroponic System in Django

## Objective:

Create a simple CRUD application in Django that allows managing a hydroponic system.

## Functional Requirements:

1. Endpoint to manage the hydroponic system:

    - Enable the user to create, read, update, and delete (CRUD) information about their hydroponic systems.

    - Each hydroponic system should be assigned to a user (owner).

    - Data validation should be added in accordance with Django REST Framework guidelines.

2. Endpoint to manage measurements:

    - Allow sending sensor data (pH, water temperature, TDS) to the existing hydroponic system.
    
    - Measurements should be saved in the database.

3. Retrieving information about systems and measurements:

    - Users should be able to get a list of their hydroponic systems.

    - All data retrieval methods should allow data filtering (time range, value range).

    - These methods should also provide options for sorting results by selected parameters.

    - Where needed, data pagination should be implemented.

    - Ability to fetch details of a specific system, including the last 10 measurements.

4. User login endpoint:

    - System for user authorization and authentication.

## Technical Requirements:

- The application should be written in Django using Django REST Framework.

- Use a PostgreSQL database. Database queries should be optimized.

- The code should comply with PEP8 standards.
    API documentation.

- Source code documentation.

- A `README.md` file with installation, configuration, and application launch instructions.

## Additional Information:

- The project should be available in a public repository on GitHub or GitLab.

- Use of good programming practices, unit tests, and Docker/Kubernetes configuration is welcomed.

- Evaluation will focus on code cleanliness, project structure, adherence to SOLID principles, and efficiency of solutions.

- A good addition would be using version control (Git) properly, with consideration for commit names and frequency.

- Adding development tools, e.g., via Django Admin, would be a strong bonus.

- The project structure should be clear and easily extendable.