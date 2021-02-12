# Soapbox Machine Learning API

Last updated on: January 2nd, 2020

## Overview
This is the main API for interacting with Soapbox's machine learning models. This documentation goes through setting up your local environment to deploying the entire application into production.

## Table of contents
- [Setup](#setup)
- [Managing dependencies using Poetry](#managing-dependencies-using-Poetry)
- [Run project checklist](#run-project-checklist)
- [Key Components](#key-components)
- [Adding a model and creating an endpoint](#adding-a-model-and-creating-an-endpoint)
- [Logging](#logging)
- [Creating custom exceptions](#creating-custom-exceptions)
- [Testing endpoints](#testing-endpoints)
- [Testing on an instance, inside Docker](#testing-on-an-instance-inside-docker)
- [Docker and deploying the app](#docker-and-deploying-the-api)
- [References/Guides](#referencesguides)
- [FAQs](#faqs)

### Setup
1) Install Python 3 using [**Homebrew package manager**](https://brew.sh).

2) Download and install `docker` and `docker-compose`
    * You can download `docker` [here](https://www.docker.com/get-started).
    * The installation instructions for `docker-compose` can be found [here](https://docs.docker.com/compose/install).
    * AWS instances may have `docker` pre-installed. In order to install `docker-compose`, use the following command: `apt-get install docker-compose`

3) Download the pretrained model weights into `/api/models` folder:
    * Sentiment model: `sentiment.pt` ([link](https://drive.google.com/drive/folders/13D3taEIGGo-NmM694nBvuMs9nraNEINr?usp=sharing))

4) If the `config.py` file is not already located in `/api`, download the file [here](https://drive.google.com/open?id=1k9-HO4-nciP0OI7aNF13TS9geRsM1pTS) and add it to the `/api` folder.

For the production server, you need to update the database configuration to talk to Forge.

5) Go into the `ml-api` project directory.

6) Run `docker-compose build` to build the project.
**Note:** To build the project for production use, run the following command:
```bash
docker-compose build --build-arg USE_PRODUCTION_ENV=True api db
```

7) Run the following set of commands before running the server to ensure that proper tables are setup:
- Run this in one terminal session:
```bash
docker-compose up db
```

- Run this in another terminal session:
```bash
docker-compose exec -T db mysql -u ml -psecret < api/database_models/reclassification_setup.sql
```

Finally, run `docker-compose down`.

Note that this step is _optional_ if the associated volume has already been setup with the proper tables.

8) Run `docker-compose up` to start the API and web server.

9) Make sure to run the following command to ensure that git hooks are running on the _pre-commit_ event:
```bash
git config core.hooksPath git_hooks
```

10) If there are any code formatting issues, run the following command:
```bash
docker-compose run --rm api ./utils/check_code_format.sh
```


**Note:** This project requires PyTorch (~650 MB installer) and installing it will
require at least 3 GB RAM, preferably more. This is installed automatically inside the Docker container,
alongside other requirements.

If `docker-compose build` is erroring out, you can [add a swapfile](https://samwize.com/2016/05/19/docker-error-returned-a-non-zero-code-137/), [increase RAM in docker](https://stackoverflow.com/questions/44533319/how-to-assign-more-memory-to-docker-container), or [disable pip caching with `--no-cache-dir`](https://stackoverflow.com/questions/45594707/what-is-pips-no-cache-dir-good-for/45594808)


**Optional: Project setup alias**
This alias will take care of building the Docker image and putting it up.

1) Update the path to the project folder.
2) Remove `git pull` if you do not want to pull.
3) Add this to your `~/.bash_profile` or `~/.zshrc`:
```
alias buildapi='cd <path-to-ml-api-project> && docker-compose down && docker-compose build && docker-compose up'
```
4) Source your bash profile or restart your session (to source your bash profile, run `source ~/.bash_profile` or `source ~/.zshrc`).
5) To use your new alias, run the following:
```
buildapi
```

# Managing dependencies using Poetry
[Poetry](https://python-poetry.org/) is the main dependency package manager used in this project. There's an available [Wiki](https://github.com/Soapbox/ml-api/wiki/Poetry:-Python-dependency-manager) on how to use Poetry.

To perform any operations using Poetry, such as installing or removing dependency, run the following:
```bash
docker exec -it ml-api /bin/bash -c "cd /api && poetry add|update|remove <dependency>
```

After running the operation, both `pyproject.toml` and `poetry.lock` should be changed and committed.

### Run project checklist
Every pull request in this project needs to pass the following checks implemented:
1) Project linting
    - Any warnings and errors will be flagged as errors and will cause the CI system to fail.
    - Address linting issues as specified by the linter

2) Unit tests
    - All tests are found inside `test`. Ensure that when building new features that appropriate unit tests are added and all tests pass.
    - Note that as soon as a test case failure is detected the CI system will fail right away.

The shell script which runs these checks is in `utils/check_project.sh`. It is advised that this script is run everytime you work on any feature set
as this will be the source of truth for any linting errors or unit test failures in the CI system.

Lastly, a convenient script called `utils/run_test.sh` takes a single argument of the Python unit test file's path so it runs the test cases in it.

**Tip:** To run any command inside your Docker container quickly, run the following:
```
docker exec ml-api <command>
```

In this case, Docker will run `command` quickly and exit immediately. For example, replacing `<command>` with `./utils/check-project.sh` will run the linter and unit test. `./utils/check-project.sh --no-linter` will only run the unit test (which is used for testing the `ml-cron` container).

In addition, if you run the following command:
```
docker exec -it ml-api <command>
```

it will allow you to interact with the container itself. This is useful when debugging any issues.

### Key Components
1) **Flask**
    * Flask is a Python library used to make REST APIs. The API is defined in `/api/app.py`
    * For more information about Flask, please visit [this link](https://www.fullstackpython.com/flask.html)

2) **Gunicorn:**
    * Gunicorn is a popular WSGI that works seamlessly with Flask.
    * Flask needs a Web Server Gateway Interface (WSGI) to talk to a web server.
    * Flask's built-in WSGI is not capable of handling production APIs, because it lacks security features and can only run one worker.
    * In this project, Gunicorn will start automatically in the api Docker container with the following config (see `Dockerfile`):
    ```
     [ "/bin/sh", "-c", "/usr/local/bin/wait.sh && gunicorn -w 1 -b :8000 -t 360 --reload api.wsgi:app" ]
    ```
    * **Note**: The bash script, `wait.sh`, ensures that the `ml-db` container goes up before the `ml-api` container.

### Adding a model and creating an endpoint

1) Add your model files to the `/models` folder.
2) To create a new endpoint:
    1) Create a new Python file in the `/endpoints` folder, with the following template:
        ```
        from flask import Blueprint, jsonify, request
        from api.exceptions.unprocessable_entity import UnprocessableEntity
        import json

        X_api = Blueprint('X_api', __name__)


        @X_api.route('/X', methods=['GET'])
        def get():
            try:
                received_obj = json.loads(request.data)
            except json.decoder.JSONDecodeError:
                raise UnprocessableEntity('Unable to read json data. Please ensure that your data is correctly formatted.', status_code=422)

            return jsonify(
                {<object to return>}
            )
        ```

        Here, we are creating a **Blueprint**. A Blueprint helps us connect the endpoint with Flask's main app (`app.py`).

    2) Replace `X` with the name of your endpoint

    3) The `@X_api.route(...` annotation is used to mark the following function as the function to be called when the endpoint is hit. The route specifies the path to query the endpoint. Note that the `@` notation is Python feature called **decorators**.

    4) Inside the `get()` function, `requests.data` holds the data object received in the request - a globally accessible property in available in a Flask application.

3) We can add this new endpoint to the `app.py` file using:
    ```
    from .endpoints.X import X_api

    app.register_blueprint(X_api)
    ```

4) At this point, you can add your functionality in the `get()` method. The `get()` function can be called anything, so you can change the name of the function as required.

5) To add additional endpoints in the same file, create functions and add the `@X_api.route(...` annotation to them. For example, see `classify.py` where we created separate single and bulk endpoints.

6) `/endpoints/util.py` contains some standalone methods that are shared across multiple endpoints

## Logging
If you need to log specific information for debugging purposes, the logging instructions are outline for GUnicorn and Flask.

### For GUnicorn
Add `--log-level=debug` to GUnicorn startup in `Dockerfile`:
```
["gunicorn", "-w", "1", "-b", ":8000", "-t", "360", "--reload", "api.wsgi:app", "--log-level=debug"]
```

You can log in app.py using:
```
app.logger.info("Your log message")
```

### For Flask
You can log in app.py using:
```
app.logger.info("Your log message")
```

For Blueprints, you can log information as follows:
```
from flask import current_app
current_app.logger.info("Your log message")
```

## Creating custom exceptions
To create a custom exception similar to `422 - UnprocessableEntity`, follow the example of `UnprocessableEntity`:

1) Create a new file in `/exceptions` with a class similar to `UnprocessableEntity`

2) Add the error handler to `app.py`, for example:
    ```
    from .exceptions.unprocessable_entity import UnprocessableEntity

    @app.errorhandler(UnprocessableEntity)
       def handle_invalid_usage(error):
           response = jsonify(error.to_dict())
           response.status_code = error.status_code
           return response
    ```

3) Use it in your endpoints using the `try-except-raise` block. For example:
    ```
    from api.exceptions.unprocessable_entity import UnprocessableEntity

    try:
        sample = json.loads(request.data)["sample"]
    except json.decoder.JSONDecodeError:
        raise UnprocessableEntity('<message>', status_code=422)
    ```

## Testing endpoints
We use Python's `unittest` package for testing our code.

1) Create a new test file under the `/test` folder, with the following naming convention, `test_X.py`, where X is the endpoint you want to test.

2) Use this basic test template to get started:
   ```
   import unittest
   from flask import Flask
   import json
   from api.endpoints.X import X_api

   app = Flask(__name__)
   app.register_blueprint(X_api)


   class XTests(unittest.TestCase):

       tester = None

       def __init__(self, *args, **kwargs):
           super(XTests, self).__init__(*args, **kwargs)
           global tester
           tester = app.test_client()

       def test_entity(self):
            # Use tester.get to simulate a GET request
           response = tester.get(
               '/X',
               data=json.dumps({<OBJECT TO SEND>}),
               content_type='application/json'
           )
           data = json.loads(response.get_data(as_text=True))
           self.assertEqual(response.status_code, 200)


   if __name__ == '__main__':
       unittest.main()
   ```

3) To run the test, `cd` to the home directory of the project (i.e. `ml-api/`).
    1) Running a single unit test, run the following command:
    ```
    ./utils/run_test.sh <name-of-unit-test-file>
    ```

    2) Running all unit tests, run the following command:
    ```
    ./utils/check_project.sh
    ```

    Please note that this command will run the linter **and** unit tests found inside the `api/test` folder

## Testing on an instance, inside Docker
Since our blog posts database is built into Docker, we cannot test the `blogs` endpoint without going into the Docker instance.

To test the API:
- SSH into the instance
- Start a new shell session inside ml-api Docker using `docker exec -it ml-api /bin/bash`.
- From the root directory of the Docker container, run `python run_tests.py`.

If all the tests pass, then you should see the following output: `OK`

## Docker and deploying the API
We use Docker to deploy the API

- `docker-compose.yml` contains instructions to create two services:
    - The `ml-api` service Dockerizes the `api` folder using the Dockerfile in it.
    - The `ml-db` service for the local database where blog posts can be stored. Note that this is only useful in local environment. In production, blog posts are stored inside Forge database.
- `docker-compose.yml` also creates a network connection between the `ml-api` and `ml-db` services/
- `Dockerfile` in the `api` folder installs all the required packages from `requirements.txt` and additional resources,
as well as starts the GUnicorn WSGI on port `8000`.

To deploy the API with changes logic only to the endpoints:
1) Use `git pull` to pull `master` and dynamically update the API.
2) The first time you hit the endpoint after updating it, the API will automatically rebuild,
so it may take some time to complete the request.

To deploy the API when a new model/endpoint is added or docker-compose/Dockerfile is changed,
it is better to rebuild the endpoint:
1. `docker-compose down` to pull down the API.
2. `git pull`
3. (optional) `docker system prune -a` to reinstall requirements, if requirements changed.
4. `docker-compose build` to rebuild.
5. `docker-compose up` to bring it up again.

## References/Guides:
* [Flask - WSGI - Gunicorn](http://flask.pocoo.org/docs/1.0/deploying/wsgi-standalone/#gunicorn)
* [Deploying a scalable Flask app using Gunicorn and Nginx, in Docker](https://medium.com/@kmmanoj/deploying-a-scalable-flask-app-using-gunicorn-and-nginx-in-docker-part-1-3344f13c9649)
* [Deploying Machine Learning Models with Docker](https://towardsdatascience.com/deploying-machine-learning-models-with-docker-5d22a4dacb5)

## FAQs:
**Q:** Running `python` on my local machine uses `python2`. How can I fix this so it uses Python 3?
**A:** The macOS ships with Python 2 by default. As a result, you will have to install Python 3 through [**Homebrew package manager**](https://brew.sh). So instead of typing `python3` directly,
add an alias to `python3` by adding the following to your `~/.bash_profile`:
```alias python=python3```.

Finally, run `source ~/.bash_profile` or restart your terminal application. To ensure it is linked properly, type `python --version` to a terminal window and it should use a Python 3 version
