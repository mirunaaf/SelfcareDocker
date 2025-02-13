# Self-care Tracker

Django Self-care Tracker is a web application designed to help users track their habits, set goals, and keep a journal.
This README provides an overview of the project's features, installation instructions, usage guidelines.
---
# Installation locally #

To install and run Django Habit Tracker locally, follow these steps:

1. Clone the repository
```
git clone https://github.com/mirunaaf/SelfcareDocker.git
cd SelfcareDocker
```

2. Install dependencies:
```
pip install -r requirements.txt
```
3. ### Database configuration ###
The project uses MySQL as the database, therefore `mysqlclient` was included in the requirements.
If you don't have MySQL installed, you can use the built-in SQLite configuration. Follow these steps:
 
  - Ensure you have SQLite installed on your system.
  - Comment out the MySQL configuration in the 'local_settings.py' file.
  - Copy the '**local_settings.example.py**' file and rename it to `local_settings.py`.
  - Update the database configuration in '**local_settings.py**' with your own database credentials.


4. Apply database migrations:
```
python manage.py migrate
```

5. Run the development server:
```
python manage.py runserver
```

6. Access the application in your web browser at [http://localhost:8000](url)
---
# Running the app using Docker #


This project sets up a Django application with a MySQL database using Docker and Docker Compose.

**Prerequisites**

Ensure you have the following installed:
* Docker Desktop

## Setup Instructions ##

1. Clone the repository
```
git clone https://github.com/mirunaaf/SelfcareDocker.git
cd SelfcareDocker
```
2. Build and Start Containers
```
docker-compose up
```
This will:
* Build the Django application container.
* Start the MySQL database container.
* Apply Django migrations and run the server.

## Accessing the MySQL Database
You can connect to the MySQL database running inside Docker from your local machine:
1. Using MySQL Client
```
mysql -h localhost -P 3308 -u root -p
```
2. Using Docker Exec
If you want to connect directly inside the MySQL container:
```
docker exec -it selfcarenew-db-1 mysql -u root -p
```

## Stopping the Containers

To stop and remove the containers:
``` 
docker-compose down 
```
To stop only the running containers without removing them:
```
docker-compose stop
```
## Making Migrations
If you make changes to your Django models, apply migrations using:
```
docker-compose exec web python manage.py makemigrations
```
```
docker-compose exec web python manage.py migrate
```
___
# Features #
### User Authentication and Registration: ###
  * Users can create accounts and log in to track their habits, set goals and keep a journal.
### Daily Activity Tracking: ###
  * Users can track the following activities: water intake, sleeping hours and meditation duration.
  * Functionalities: Add, delete and update activities.
  * Users will be able to get access to their daily activities records.
  
### Creating Personal Goals: ###
  * Users will be able to set a goal, a target date to complete it, update the status, describe actions towards accomplishing their goal.
  * Functionalities: Add, delete and update personal goals.
  * Access personal goals records.

### Journal Records: ###
  * Users will be able to write their thoughts on a specific date.
  * Functionalities: Add, delete and update journal entries.
  * Access journal records.

### Tips & Tricks ###
  * A dedicated page for improving lifestyle and useful resources.
  * Users will be able to access pages of helpful content and also applications for tracking workouts, meditation and water intake.

___
# Usage #
Once the application is running, you can perform the following actions: 

### Register/Login page: ###
  * Create an account or log in with existing credentials.

### Menu page: ###
  * Navigate to the following pages: Daily Records, Your Goals, Journal, Tips and Tricks.

### Daily Activities page: ###
  * Navigate to the "Daily Records" page and input details such as date, water intake, sleeping hours and meditation.
  * Users can also go to the menu page or view all activities.
### Your Daily Activities page: ###
  * Users can view, delete and update daily activities ordered by most recent date.
  * Users would be able to go back to menu page and logout.
### Your Goal page: ###
  * Navigate to the "Your Goal" page and input details such as goal, target date, status and description.
  * Users can also go to the menu page or view all goals.
### Your Goals page: ###
  * Users can view, delete and update personal goals ordered by target date.
  * Users would be able to go back to menu page and logout.
### Your Thoughts page: ###
  * Navigate to the "Your Thoughts" page and input details such as date and journal thoughts.
  * Users can also go to the menu page or view all journal entries.
### Your Journal page: ###
  * Users can view, delete and update journal entries.
  * Users would be able to go back to menu page and logout.
### Tips and Tricks page: ###
  * Check out reliable information to improve your well-being.
