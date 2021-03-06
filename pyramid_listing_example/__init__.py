""" An example for the pyramid_listing_ package

.. _pyramid_listing: https://github.com/holgi/pyramid_listing
"""

from pyramid.config import Configurator

from .resources import CheeseListResource


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.include("pyramid_jinja2")
    config.include(".models")
    config.add_static_view("static", "static", cache_max_age=3600)
    config.set_root_factory(CheeseListResource)
    config.scan()
    return config.make_wsgi_app()
