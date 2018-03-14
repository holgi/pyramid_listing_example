Pyramid Listing Example
=======================

This is an example pyramid project for the [pyramid_listing](https://github.com/holgi/pyramid_listing) package.

The most interesting files – if you know pyramid – are propably:

- `pyramid_listing_example/resouces.py`
- `pyramid_listing_example/templates/cheese_list.py`


Getting Started
---------------

- Clone the project from github:

    `git clone https://github.com/holgi/pyramid_listing_example.git`

- Change directory into of the project.

    `cd pyramid_listing_example`

- Create a Python virtual environment.

    `python3 -m venv env`

- Upgrade packaging tools.

    `env/bin/pip install --upgrade pip setuptools`

- Install the project in editable mode with its testing requirements.

    `env/bin/pip install -e ".[testing]"`

- Configure the database.

    `env/bin/initialize_pyramid_listing_example_db development.ini`

- Run the project's tests.

    `env/bin/pytest`

- Run the project.

    `env/bin/pserve development.ini`
