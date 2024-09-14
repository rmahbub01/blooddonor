# BLOOD DONOR Project using FastAPI

This is a [FastAPI](https://fastapi.tiangolo.com/) application built for high-performance API development with Python. FastAPI is a modern, fast (high-performance), web framework for building APIs with ```Python 3.12+ ``` based on standard Python type hints. It uses the official fastapi cookiecutter.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/rmahbub01/blooddonor.git
    cd blooddonor
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Quick Start

00. Create First Super User
    ```bash
    python initial_data.py
    ```

1. Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. Open your browser and visit:

    - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

Refer to the [interactive API docs](http://127.0.0.1:8000/docs) for a full list of available endpoints.


## Environment Variables


##### Create ```.env``` file in the project directory

 ```python
   PROJECT_NAME=BloodDonor
   SERVER_NAME=127.0.0.1:8000
   SERVER_HOST=http://localtest.me
   # secret key use only in productions
   # Change this key using openssl rand -hex 32 in production
   SECRET_KEY=e7349af4f2d09ec73a820455615fafae531a36b22eb16553060d0fc4be7fc02e
   
   # your allowed domain for frontend goes in cors origin
   # Leave it blank until production
   BACKEND_CORS_ORIGINS=[]
   
   # this project is designed to use only sqlite
   SQLALCHEMY_DATABASE_URI=sqlite+aiosqlite:///./blood_donor_db.db
   
   FIRST_SUPERUSER=admin
   FIRST_SUPERUSER_PASSWORD=admin
   FIRST_SUPERUSER_GENDER=<male | female | other>
   FIRST_SUPERUSER_EMAIL=admin@gmail.com
   FIRST_SUPERUSER_MOBILE=<015******** bd mobile no. without +88>
   FIRST_SUPERUSER_DEPARTMENT=41
   FIRST_SUPERUSER_STUDENT_ID=20204006
   FIRST_SUPERUSER_DISTRICT=<dhaka for more option see docs>
   FIRST_SUPERUSER_BLOOD_GROUP=<b+ for more option see docs>
   FIRST_SUPERUSER_STUDENTSHIP_STATUS=<4th for more option see docs>
   
   #use smtp for emailing
   # set SMTP_TLS to True to send password reset email
   SMTP_TLS=False
   SMTP_PORT=587
   SMTP_HOST=smtp.gmail.com
   SMTP_USER=<email>
   SMTP_PASSWORD=<smtp password or app password>
   EMAILS_ENABLED=False
   EMAIL_VERIFICATION_FOR_ACCOUNT=True
   EMAILS_FROM_EMAIL=<company email or just email>
   EMAILS_FROM_NAME=BloodDonor
   
   # Automatics Documentations UI. Set None to disable
   # if you want to disable the automatic docs then uncomment the two lines below
   # DOCS_URL=None
   # REDOC_URL=None
 ```

