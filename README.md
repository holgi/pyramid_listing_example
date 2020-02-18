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

- Initialize the developement environment environment.

    `make devenv`

- Configure the database.

    `.venv/bin/initialize_pyramid_listing_example_db development.ini`

- Run the project's tests.

    `make test`

- Run the project.

    `.venv/bin/pserve development.ini`
