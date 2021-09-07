# Todo App for Deployment 4

## Installation Requirements.

1. Create .env file in the root of the repository with the following values.
```
DEBUG=True
FLASK_ENV=development
FLASK_APP=api.app.py
```
2. This allows you to quickly run the application without constantly exporting environment variables.

3. Create and activate a virtual environment for python in the root of the repo.
```
$ python3 -m venv venv
$ source ./venv/bin/activate
```
4. Install dependencies.
```
$ pip install -r requirements.txt
```
5. Run the application
```
$ flask run
```

## Notes

- Remember to change the env file according to if you want to run the application in development or production mode. As well as turning off DEBUG mode. 