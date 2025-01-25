Sensory
Micro Weather Sensory App

The main idea is:

Your IoT device (or data source) sends new readings to your backend server and stores them in MongoDB Atlas.
The backend then pushes these new readings to the UI (browser or Streamlit app) using either a WebSocket (e.g., Socket.IO, Django Channels) or Server-Sent Events.
The UI receives these updates automatically and renders them immediately.


Pipeline

UI

Description: The user interface will display real-time weather data received from the backend.
Data Retrieval

Description: Data is retrieved from IoT devices and stored in MongoDB Atlas.
Backend

Database: MongoDB
Framework: Django

How to Deploy the Django Server

Follow these steps to set up and deploy the Django server:

1. Create a Project Folder

1st. Create a project folder (e.g., hello_django) and navigate into it:
 mkdir hello_django
 cd hello_django

 2. Create a Virtual Environment

Create a virtual environment using Python 3. Replace .venv with your preferred environment name.

Linux: 
sudo apt-get install python3-venv    # If needed
python3 -m venv .venv
source .venv/bin/activate



MAC:
python3 -m venv .venv
source .venv/bin/activate


Windows: 
py -3 -m venv .venv
.venv\scripts\activate


3. Select the Python Interpreter in VS Code

Open the VS Code command palette (Ctrl+Shift+P or Cmd+Shift+P on macOS).
Select Python: Select Interpreter.
Choose the virtual environment in your project folder (e.g., ./.venv or \.venv).

4. Verify the Virtual Environment

The status bar in VS Code should display the Python version and virtual environment.
5. Update pip

Update pip in the virtual environment:

Command: python -m pip install --upgrade pip

 6. Install Django

Install Django in the virtual environment:

Command: python -m pip install django

 7. Create the Django Project

Create a Django project using the following command:

Command: django-admin startproject web_project 

This creates the following file structure:

manage.py: Django's command-line utility.
web_project/: Contains project settings and configurations.
__init__.py: Marks the folder as a Python package.
asgi.py: Entry point for ASGI-compatible web servers.
settings.py: Project settings.
urls.py: URL routing for the project.
wsgi.py: Entry point for WSGI-compatible web servers.


8. Create the Development Database

Run the following command to create an empty development database:

Command: python manage.py migrate.

 - This creates a default SQLite database (db.sqlite3) for development purposes.


9. Run the Development Server

Start the Django development server:

 Commnand: python manage.py runserver

 - The server runs on http://127.0.0.1:8000/ by default.
- Open the URL in your browser to verify the Django project.

10. Create a Django App

1. Create a Django app named hello:

Command: python manage.py startapp hello

This creates a folder named hello with the following files:
views.py: Contains functions to define pages.
models.py: Contains classes defining data objects.
migrations/: Used for database version management.


2. Modify hello/views.py:

 Code: from django.http import HttpResponse

 def home(request):
     return HttpResponse("Hello, Django!")

 3. Create hello/urls.py:

    Code: from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name="home"),
]


4. Update web_project/urls.py:

   from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("hello.urls")),
    path('admin/', admin.site.urls)
]
5th. Save all modified files.


6th. Run the development server again:

python manage.py runserver
Open http://127.0.0.1:8000/ in your browser to see the "Hello, Django!" page.

File Structure:

hello_django/
├── .venv/
├── manage.py
├── web_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── hello/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    ├── models.py
    ├── tests.py
    └── views.py


    








