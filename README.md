# Library Service

This repository contains the implementation of a Library Management System designed to facilitate the management of
books, borrowings, and returns. The system enables users to borrow and return books seamlessly, while administrators can
efficiently manage the library's inventory and track active borrowings.

## Features

- **JWT Authentication**: Secure access to the API endpoints.
- **Admin Panel**: Manage data directly from `/admin/`.
- **API Documentation**: Swagger documentation is available at `/api/doc/swagger/`.
- **Book Management**: Allows users to view books available for check-out.
- **Borrowing Management**: Allows users to borrow and return books.
- **Filter**: Filtering borrows by status or users.

---

## Installation Using GitHub

To set up and run the Library Service locally, follow the steps below:

### Prerequisites

- **Python 3.9+**

### Steps to Install

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd library-service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables using the `.env.sample` file provided in the repository:
   ```bash
   cp .env.template .env
   ```

   Fill out the `.env` file with your database credentials and other required values.

5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
6. Load demo data:
   ```bash 
   python manage.py loaddata demo_data.json
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

## Getting Access

1. **Register a new user**:
   ```
   POST /api//v1/user/register/
   ```

2. **Get access token**:
   ```
   POST /api/v1/user/token/
   ```

Use the access token in the Authorization header to access protected endpoints. Demo user
(**email**: admin@example.com, **password**: adminpass)

---

## Contribution

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.
