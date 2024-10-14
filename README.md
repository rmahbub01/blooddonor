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

4. Rename ```.env.example``` file to ```.env```
   - Set the required variables
   - To see variable choices option, move to the bottom part of the documentation
   - Like, ```FIRST_SUPERUSER_DISTRICT=dhaka, FIRST_SUPERUSER_DISTRICT=munshiganj, FIRST_SUPERUSER_BLOOD_GROUP=ab+```
   - If you have separate frontend in different location, set the ```BACKEND_CORS_ORIGINS``` to that address.
 

```python
   PROJECT_NAME=BloodDonor
   SERVER_NAME=http://127.0.0.1:8000
   SERVER_HOST=http://localtest.me
   # Change the url to your frontend url
   FRONTEND_HOST=http://localhost:5367
   
   # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
   # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
   # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
   BACKEND_CORS_ORIGINS=["http://127.0.0.1:8000", "http://localtest.me", "http://localhost:5367", "http://localhost"]
   
   # secret key use only in productions
   # Change this key using openssl rand -hex 32 in production
   SECRET_KEY=e7349af4f2d09ec73a820455615fafae531a36b22eb16553060d0fc4be7fc02e
   
   # this project is designed to use only sqlite
   SQLALCHEMY_DATABASE_URI=sqlite+aiosqlite:///./blood_donor_db.db
   
   FIRST_SUPERUSER=admin
   FIRST_SUPERUSER_PASSWORD=admin
   FIRST_SUPERUSER_GENDER=<male or female or other>
   FIRST_SUPERUSER_EMAIL=<email of the superuser>
   FIRST_SUPERUSER_MOBILE=<Bangladeshi mobile no. of superuser>
   FIRST_SUPERUSER_DEPARTMENT=<204=Dept. of Statistics>
   FIRST_SUPERUSER_STUDENT_ID=<20204006, 20=admission year, 204=dept. code, 006=serial of student>
   FIRST_SUPERUSER_DISTRICT=dhaka
   FIRST_SUPERUSER_BLOOD_GROUP=<a+, a-, b+, b-, ab+, ab-, o+, o->
   FIRST_SUPERUSER_ACADEMIC_YEAR=<2019-2020, 2022-2023 and so on>
   
   #use smtp for emailing
   SMTP_TLS=False
   SMTP_PORT=587
   SMTP_HOST=smtp.gmail.com
   SMTP_USER=<organization email>
   SMTP_PASSWORD=<smtp application password>
   EMAILS_ENABLED=False
   EMAILS_FROM_EMAIL=<organization email>
   EMAILS_FROM_NAME=BloodDonor
   
   # Automatics Documentations UI. Set None to disable
   #DOCS_URL=None
   #REDOC_URL=None
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


## List of Choices

   - Gender Choices
      ```
         male
         female
         other
      ```
   - Department Choices

       - Faculty of Arts and Humanities:
    
                "101" - Bangla
                "102" - English
                "103" - History
                "104" - Islamic History and Culture
                "105" - Philosophy
                "106" - Fine Arts
                "107" - Arabic
                "108" - Pali
                "110" - Islamic Studies
                "111" - Dramatics
                "112" - Persian Language and Literature
                "113" - Education and Research
                "114" - Modern Languages
                "115" - Sanskrit
                "116" - Music
                "117" - Bangladesh Studies
    
       - Faculty of Science:
                
                "201" - Physics
                "202" - Chemistry
                "203" - Mathematics
                "204" - Statistics
                "208" - Forestry and Environmental Sciences
                "209" - Applied Chemistry and Chemical Engineering
                
       - Faculty of Business Administration:
                
                "301" - Accounting
                "302" - Management
                "303" - Finance
                "304" - Marketing
                "305" - Human Resource Management
                "306" - Banking and Insurance
                
       - Faculty of Social Sciences:
                
                "401" - Economics
                "402" - Political Science
                "403" - Sociology
                "404" - Public Administration
                "405" - Anthropology
                "406" - International Relations
                "407" - Communication and Journalism
                "408" - Development Studies
                "409" - Criminology and Police Science
                
       - Faculty of Law:
                
                "501" - Law
                
       - Faculty of Biological Sciences:
                
                "601" - Zoology
                "602" - Botany
                "603" - Geography and Environmental Studies
                "604" - Biochemistry and Molecular Biology
                "605" - Microbiology
                "606" - Soil Science
                "607" - Genetic Engineering and Biotechnology
                "608" - Psychology
                "609" - Pharmacy
                
       - Faculty of Engineering:
                
                "701" - Computer Science and Engineering
                "702" - Electrical and Electronic Engineering
                
       - Faculty of Education:
                
                "801" - Physical Education and Sports Science
                
       - Faculty of Marine Sciences and Fisheries:
                
                "901" - Marine Sciences
                "902" - Oceanography
                "903" - Fisheries

   - Student ID
     - 8 digits number 
     - First two digits are admission year
     - Second 3 digits are department choice number
     - Third 3 digits are serial of the student
     - Note: Student ID must be matched with corresponding department, otherwise account can't be created.

   - District Choices
        
     ```
        bagerhat
        bandarban
        barguna
        barisal
        bhola
        bogura
        brahmanbaria
        chandpur
        chapainawabganj
        chattogram
        chuadanga
        cox's bazar
        cumilla
        dhaka
        dinajpur
        faridpur
        feni
        gaibandha
        gazipur
        gopalganj
        habiganj
        jamalpur
        jessore
        jhalokati
        jhenaidah
        joypurhat
        khagrachhari
        khulna
        kishoreganj
        kurigram
        kushtia
        lakshmipur
        lalmonirhat
        madaripur
        magura
        manikganj
        meherpur
        moulvibazar
        munshiganj
        mymensingh
        naogaon
        narail
        narayanganj
        narsingdi
        natore
        netrokona
        nilphamari
        noakhali
        pabna
        panchagarh
        patuakhali
        pirojpur
        rajbari
        rajshahi
        rangamati
        rangpur
        satkhira
        shariatpur
        sherpur
        sirajganj
        sunamganj
        sylhet
        tangail
        thakurgaon
     ```
   - Blood Group Choices
       ```
            a+
            a-
            b+
            b-
            ab+
            ab-
            o+
            o-
        ```
   - Academic Year Choices
        ```
            2010-2011
            2011-2013
            ....
            2048-2049
            2049-2050
            ...
        ```
   - Employment Status Choices
        ```
           student
           employed
           unemployed
        ```