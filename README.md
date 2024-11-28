# Polar Labs Django REST API Starter Kit

This repo is a standard starter kit for a Django REST API powered by Django Rest Framework. By following the README below, updating your settings.py to match your project needs, and configuring your CI/CD with the right environments, you should have a basic Django API out of the box letting you get right to the coding.

## Installation

Installation involves several steps. If you are unfamilar with Django, particularly with how migration works, it is recommended to familiarize yourself with this process first. Django has very robust [documentation](https://docs.djangoproject.com/en/) and a very active development community.

**1. Sync Code**

The first thing to do is to clone this repo somewhere you are comfortable with. This does **not** have to be in the root of a webserver as there is a built-in dev server, and you will deploy with an external server called Daphne pointed to this repo.

**2. Dependencies**

For this project we are using [poetry](https://python-poetry.org/docs) to simplify dependency and virtual environment management. It functions just like npm, simply [install poetry](https://www.notion.so/Installing-Using-Poetry-477e7c4dadaf470e9140e68dedc48dfd?pvs=4) and run `poetry install` to get started from the same directory as the `pyproject.toml` or `poetry exec` to run a script in the project file.

We also recommend using [pyenv](https://github.com/pyenv/pyenv) to manage your python versions.

In order to get set up with [Poetry](https://python-poetry.org/docs), follow the steps below (but read the docs first!):

```
# Install poetry
curl -sSL <https://install.python-poetry.org> | python -

# Add this to your .bashrc or .zshrc
export PATH="/Users/{YOUR_USER}/.local/bin:$PATH"

# If you are using pyenv (which you should be)
poetry config virtualenvs.prefer-active-python true

# Installs the task runner that should be a part of poetry already
poetry self add 'poethepoet[poetry_plugin]'

# cd into the project folder and run
poetry install
poetry shell

```

Lastly, you need to install the [precommit](https://pre-commit.com/) hooks into your environment. You don't need to install precommit to your machine, it is a dependency of this project. You can install the hooks like this:

```
# install pre-commit (not techincally part of poetry, but still needs to be done)
poetry exec pc_init
```

**3. Environment**

We manage our environments using the [django-environ package](https://django-environ.readthedocs.io/en/latest/). This means you can use a `.env` file locally, and environment variables on a server. Doing this means you don't need to worry about exporting env vars on your machine, but we can use the same Docker image on any server we want just swapping the necessary variables.

First, create a new file called `.env` at the root of your project (this will be ignored by git). In the `api_chart/values.yaml` file you will find all the environment variables you need in order to run this project. You're gunna want both the env vars and the secrets, but just all together in your `.env` file.

If you're missing anything, don't worry. Django will get mad at you until you get all the pieces.

**4. Database**

Before you can run migrations you need to install a local postgresql. There are many good tutorials online depending on your OS. Create a database and user (if you'd like, or just use root) for this project and make sure the user has the permission to create databases. This is so that you can test your code and Django can create test databases.

> NOTE: On production however, your user should only have permissions on a single DB just for your application. Don't use root, don't give it any more permissions than necessary!

You will never need to interact directly with the database, the ORM will do everything for you. If you want to explore freely, you can run `python manage.py shell` and import your models just as you would in application code.

Once your database is configured properly, simply run `python manage.py migrate` and Django will automatically build your database for you. You must do this in the `polar_labs` folder (the top level, not the one with settings.py in it). You can generate a superuser with `python manage.py ensure_adminuser --username= --password=` and from there you can manage the database with the [built in admin panel](http://localhost:8000/admin). To start the server run `python manage.py runserver`. If you would like the dev server to be accessible over your network, use `python manage.py runserver 0.0.0.0:8000` instead.

**5. Static Files**
Static files are files like images, or JS files that aren't dynamically generated in our API routes. They will be served from a CDN using [django-storages](https://django-storages.readthedocs.io/en/latest/). To generate them for local development run `python manage.py collectstatic`, they will be gitignored.

To configure this for yourself, visit the docs and adjust the environment variables in `settings.py`.

**6. Get Started!**

That should be everything you need to get the API installed! Instructions on usage are below.

## Development server

As mentioned, run `python manage.py runserver` for a dev server. The server will be started on `http://localhost:8000/`. The app will automatically reload if you change any of the source files, and you'll find that if you visit your routes in the browser while `DEBUG=True` in your settings, there is a GUI that Django Rest Framework (DRF) provides.

You can also find the Django Admin Panel at `http://localhost:8000/admin`. We have included the [django-jet](https://django-jet-reboot.readthedocs.io/en/latest/) theme to make it much prettier.

## Running Tests

Run `python manage.py test {optional-name-of-app}` to execute the tests. Django will generate a test database to work with, so don't worry about losing any data. Tests are stored with their respective target app (the folders inside `polar_labs` that you register in `settings.py`).

We have 2 base classes that we provide for some extra utility you can find in `polar_labs/core/base_tests.py`:

**BaseUnitTest:** This is currently just an extension of the built in Django `TestCase`. But by extending from it early, you give yourself room to add custom functionality later.

**LiveApiTestCase**: This is an extension of LiveServerTestCase. This is kind of like a pseudo-integration test. It boots up a server in the background and runs your tests against that server as if it were a real one. This allows you to simulate HTTP requests and check responses locally and in CI without having to be running a real staging server.

Finally, we recommend adding `poetry run python manage.py ensure_tests_run` to your CI in order to ensure you didn't mess up the naming scheme! It is in our example `bitbucket-pipelines.yml`.

## Integration Testing with Tavern

This project uses [Tavern](https://tavern.readthedocs.io/en/latest/) for integration testing of API endpoints. Tavern is built on top of pytest and provides a YAML-based syntax for defining API tests.

### Overview

Our integration tests verify API endpoints against live servers (staging and production) to ensure:

- Expected HTTP response codes
- Response data shape validation using JSON Schema
- End-to-end functionality across service boundaries

### Running Integration Tests

Integration tests can be run using the poetry task defined in `pyproject.toml`:

```bash
poetry exec run_integ_tests
```

This command:

- Uses the global configuration from `tavern_config.yaml`
- Runs all test files matching the pattern `*.tavern.yaml`
- Can be executed locally or in CI/CD pipelines

### Configuration

Global test configuration is stored in `tavern_config.yaml`. This includes:

- Base URLs for different environments
- Common headers
- Global variables
- Retry configurations

### Test Files

Test files follow the naming pattern `*.tavern.yaml` and are organized by feature area. For example:

- `polar_labs/blog/integ_tests/blog.tavern.yaml`

### Example Test Structure

```yaml
# blog.tavern.yaml
test_name: Verify blog post retrieval
stages:
  - name: Get single blog post
    request:
      url: "{host}/api/blog/posts/{post_id}"
      method: GET
    response:
      status_code: 200
      verify_response_with:
        function: polar_labs.blog.integ_tests.verify_blog_post_schema
```

### Response Schema Validation

We use Python's [jsonschema](https://python-jsonschema.readthedocs.io/) library to validate response shapes. Our approach combines:

1. YAML-defined tests in `*.tavern.yaml` files
2. Python functions for response validation
3. Utility functions in `polar_labs/core/utils/tavern.py` that:
   - Generate consistent schemas
   - Enforce required properties
   - Fail on unexpected properties
   - Handle retry logic for CI/CD scenarios

### Schema Validation Example

```python
from polar_labs.core.utils.tavern import create_schema

def verify_blog_post_schema(response):
    schema = create_schema({
        "id": "integer",
        "title": "string",
        "content": "string",
        "author": {
            "id": "integer",
            "name": "string"
        }
    })
    return schema.matches(response.json())
```

## Best Practices

1. **Environment Testing**:

   - Run tests against staging before production deployments
   - Use the same tests as smoke tests in production
   - Configure appropriate timeouts and retries for CI/CD

2. **Schema Validation**:

   - Always validate response shapes
   - Use the utility functions in `tavern.py` for consistent schema generation
   - Define clear, reusable schemas for common response patterns

3. **Test Organization**:
   - Group tests by feature area
   - Use clear, descriptive test names
   - Include both happy path and error cases

## Future Improvements

Some areas identified for potential enhancement:

- Expanded test coverage across all endpoints
- More comprehensive schema validation patterns
- Additional utility functions for common testing scenarios
- Performance testing integration
- Enhanced error reporting and logging

## Other Utility Classes We Include

**BaseAdmin in polar_labs/core/base_admin.py:** Also just an extension of the built-in `ModelAdmin` class for now. But you might want to extend this later so use this now!

**BaseModel in polar_labs/core/base_models.py:** An extension of the built-in `Model` class that automatically adds an id, created, and updated field. It also adds validation to the `save()` method by default. You can extend your models from this class and get these plus anything you add by default.

**CoreUser in polar_labs/core/models.py:** This is an extension of the default User model that doesn't currently add anything. However, it is a MAJOR pain in the ass to change your User model late in the game. Using this class from day 1 means you can extend it if you need to. Note the standard approach to user data in Django is to create a new model called Profile (or similar) and one-to-one with the User model.

## Deployments

This repo comes with a working Dockerfile that you can simply build and deploy. It uses `python:3.11.1-slim` and uses [Daphne](https://github.com/django/daphne) to serve the site. There is no nginx proxy as we use Kubernetes ingresses for that purpose. There is a startup script in `bin/start-daphne` that does some setup and starts the server.

There is an example docker-compose in this project as well if you would prefer that we have set up to deploy a built image to your local machine. You can easily convert this to work for your own deployments if you prefer. The docker-compose file relies on you having a `.env` file instead of using env vars like we do with Kubernetes.

> **Note:** We deploy this container using our open source helm template you can see in `web_chart/Chart.yaml`. However it's up to you how you would like to deploy.

### CI/CD

We include our bitbucket pipelines file as a reference for how to deploy this container in an automated fashion. We use the github branch model and aim for quick deploys over complicated release models. Our flow looks like this:

- Pull Requests
  - On every pull request run tests. We set branch restrictions in our repo to only allow merges to main, and only after the pipeline passes
  - We use kubernetes to deploy preview environments with a manual trigger instead of keeping a dedicated staging env alive (for now)
  - We do all our linting/formatting with precommit (included in this repo) to keep our build minutes low
- Merge to Main
  - Run all the tests again to make sure everything still jives with the existing code before we deploy it
  - On manual trigger, build the docker image, upload to a private registry, deploy to kubernetes with the Polar Labs helm chart.

Keeping our process simple means we can rapidly deploy updates without having to worry about named branches, release branches, or hotfix merges back to develop. In our eyes, all code should be complete and passing tests before it goes to main, and if that's true it can go to prod.

> **Note:** Make sure you set the pipeline variables/secrets from the file in the CI runner!

## User Roles/Groups in Admin

In production, the admin panel has a number of roles/groups set up to assign to users to control their permissions. You can configure these yourself following the Django docs, and apply them through the admin panel GUI.

To give someone full permissions as a dev, make them a superuser, no group needed. To allow someone to sign into admin, make them a staff user, they will inherit their own individual permissions + the permissions of their group.

## Tips

- End all your urls with a "/"! Django gets kind of quirky around urls without a / at the end, and doesn't play nicely with node fetch (if you're using JS on your front end)
- Don't forget to run `poetry exec pc_init` at the beginning of each project to configure precommit!

## Further help

To get more help on the tools used in this project check out:

- [Django Docs](https://docs.djangoproject.com/en/)
- [Bitbucket Pipelines](https://confluence.atlassian.com/bitbucket/configure-bitbucket-pipelines-yml-792298910.html)
- [Understanding async python](https://www.b-list.org/weblog/2022/aug/16/async/)
