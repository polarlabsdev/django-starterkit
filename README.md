# polar_labs Django Backend

**TODO: FILL THIS README WITH INFO RELATED TO POLAR_LABS - FOR NOW IT IS PASTED FROM A PREVIOUS PROJECT AS A ROUGH GUIDE. TAKE WITH A GRAIN OF SALT. ALSO USE POETRY NOT VIRTUALENV**

## Installation

Installation involves several steps. If you are unfamilar with Django, particularly with how migration works, it is recommended to familiarize yourself with this process first. Django has very robust [documentation](https://docs.djangoproject.com/en/) and a very active development community.

**1. Sync Code**

The first thing to do is to clone this repo somewhere you are comfortable with. This does **not** have to be in the root of a webserver as there is a built-in dev server.

**2. Dependencies**

For this project we are using [poetry](https://python-poetry.org/docs) to simplify dependency and virtual environment management. It functions just like npm, simply [install poetry](https://www.notion.so/Installing-Using-Poetry-477e7c4dadaf470e9140e68dedc48dfd?pvs=4) and run `poetry install` to get started from the same directory as the `pyproject.toml` or `poetry exec` to run a script in the project file.

**3. Database**

Before you can migrate you need to install a local postgresql. There are many good tutorials online depending on your OS. Create a database and user just for this project and copy `.env.example` to a new file called `.env` at the root of your project (this will be ignored by git). Update your newly copied `.env` file with relevant values to replace the ones in the template. You will never need to interact directly with the database, the ORM will do everything for you. If you want to explore freely, you can run `python manage.py shell` and import your models just as you would in application code.

**4. Static Files (TBD)**
Static files are files like images, or JS files that aren't dynamically generated in our API routes. They will be served from our Digital Ocean CDN using `django-storages`. To generate them for local development run `python manage.py collectstatic`, they will be gitignored.

**5. Migrate**

Once your database is configured properly, simply run `python manage.py migrate` and Django will automatically build your database for you. You must do this in the `polar_labs` folder (the top level, not the one with the env files in it). You will need to generate a superuser with `python manage.py createsuperuser` and from there you can manage the database with the [built in admin panel](http://localhost:8000/admin). To start the server run `python manage.py runserver`.

**7. Get Started!**

That should be everything you need to get the API installed. Instructions on usage are below.

## Development server

Run `python manage.py runserver` for a dev server. The server will be started on `http://localhost:8000/`. The app will automatically reload if you change any of the source files, and Graphene will enable you to play with the routes via GraphIQL. **TBD: add details to this section**

## Running unit tests (TBD)

Run `python manage.py test {optional-name-of-app}` to execute the tests. Django will generate a test database to work with, so don't worry about losing any data. Tests are stored with their respective target. For example, any `tests.py` will be stored in the relevant app folder.

It is required to update and run your tests before creating any pull requests to master. The tests will be run automatically on the PR and if you didn't write any new tests there will be questions in the code review.

## Contribution (TBD)

#### Pull requests

All contributions to this project require a Pull Request (PR) that needs to be reviewed before merging to master.

Once a commit is merged to master it will be automatically deployed. See deployments section for more info.

All PRs will be subject to a series of tests run by Bitbucket Pipelines. The config can been seen in `bitbucket-pipelines.yml` in the root directory of the project. All dependencies will be installed, a fork of black called axblack that allows for single quotes will check your formatting, bandit and safety will check security, and finally tests will be run. It is recommended to install `axblack` either in your editor or as a pre-commit hook.

**TODO: Investigate to see if there is a python equivalent of husky**

## Deployments

TBD

## User Roles/Groups in Admin

In production, the admin panel has a number of roles/groups set up to assign to users to control their permissions. This includes the following groups:

TBD

To give someone full permissions as a dev, make them a superuser, no group needed. To allow someone to sign into admin, make them a staff user, they will inherit their own individual permissions + the permissions of their group.

## Further help

To get more help on the tools used in this project check out:

- [Django Docs](https://docs.djangoproject.com/en/)
- [Bitbucket Pipelines](https://confluence.atlassian.com/bitbucket/configure-bitbucket-pipelines-yml-792298910.html)
- [Black Fork](https://github.com/axiros/axblack)
- [Bandit](https://github.com/PyCQA/bandit)
- [Safety](https://github.com/pyupio/safety)
- [Understanding async python](https://www.b-list.org/weblog/2022/aug/16/async/)

## To be documented

- usage of django storages + the vars in .env
- usage of core/management
- usage of base models
- usage of case user model
- ~~usage of .env~~
- core utils
- configuring jet
