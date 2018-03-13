# package

import pytest
import transaction

from pyramid import testing

from pyramid_listing_example.scripts.initializedb import add_example_data


APP_SETTINGS = {
    'sqlalchemy.url': 'sqlite:///:memory:',
    'pyramid_listing.items_per_page_default': '10',
    'pyramid_listing.items_per_page_limit': '50',
    'pyramid_listing.page_window_left': '2',
    'pyramid_listing.page_window_right': '5'
    }


@pytest.fixture(scope='session')
def app_config():
    ''' fixture for tests requiring a pyramid.testing setup '''
    with testing.testConfig(settings=APP_SETTINGS) as config:
        config.include('pyramid_jinja2')
        config.include('pyramid_listing')
        yield config


@pytest.fixture(scope='session')
def dbsession(app_config):
    ''' fixture for testing with database connection '''
    from pyramid_listing_example.models.meta import Base
    from pyramid_listing_example.models import (
        get_engine,
        get_session_factory,
        get_tm_session
        )

    settings = app_config.get_settings()
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    session = get_tm_session(session_factory, transaction.manager)
    Base.metadata.create_all(engine)

    add_example_data(session)
    yield session

    transaction.abort()
    Base.metadata.drop_all(engine)
