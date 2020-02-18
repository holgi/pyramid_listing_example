import pytest
from pyramid.testing import DummyRequest

from pyramid_listing_example.models import Cheese

from . import app_config, dbsession  # noqa: F401


def test_cheese_resource_init():
    from pyramid_listing_example.resources import CheeseResource

    # using a dummy request as a model since it provides properties just
    # from initialization
    model = DummyRequest(id=1)
    resource = CheeseResource(model, "some parent")
    assert resource.model == model
    assert resource.__name__ == 1
    assert resource.__parent__ == "some parent"


def test_cheese_list_get_base_query(dbsession):  # noqa: F811
    from pyramid_listing_example.resources import CheeseListResource
    from sqlalchemy.orm.query import Query

    request = DummyRequest(dbsession=dbsession)
    resource = CheeseListResource(request)
    assert isinstance(resource.get_base_query(request), Query)


def test_cheese_list_get_filtered_query_no_search(dbsession):  # noqa: F811
    from pyramid_listing_example.resources import CheeseListResource
    from sqlalchemy.orm.query import Query

    request = DummyRequest(dbsession=dbsession, GET={})
    resource = CheeseListResource(request)
    filtered_query = resource.get_filtered_query(resource.base_query, request)
    assert isinstance(filtered_query, Query)
    assert filtered_query == resource.base_query


def test_cheese_list_get_filtered_query_empty_search(dbsession):  # noqa: F811
    from pyramid_listing_example.resources import CheeseListResource
    from sqlalchemy.orm.query import Query

    request = DummyRequest(dbsession=dbsession, GET={"search": ""})
    resource = CheeseListResource(request)
    filtered_query = resource.get_filtered_query(resource.base_query, request)
    assert isinstance(filtered_query, Query)
    assert filtered_query == resource.base_query


def test_cheese_list_get_filtered_query_with_search(dbsession):  # noqa: F811
    from pyramid_listing_example.resources import CheeseListResource
    from sqlalchemy.orm.query import Query

    request = DummyRequest(dbsession=dbsession, GET={"search": "milk"})
    resource = CheeseListResource(request)
    filtered_query = resource.get_filtered_query(resource.base_query, request)
    assert isinstance(filtered_query, Query)
    assert filtered_query != resource.base_query


@pytest.mark.parametrize(
    "identifier,expected",
    [
        (None, None),
        ("unknown", None),
        ("name", Cheese.name),
        ("country", Cheese.country),
        ("region", Cheese.region),
    ],
)
def test_cheese_list_get_order_by_field(
    dbsession, identifier, expected  # noqa: F811
):
    from pyramid_listing_example.resources import CheeseListResource

    request = DummyRequest(dbsession=dbsession)
    resource = CheeseListResource(request)
    assert resource.get_order_by_field(identifier) == expected


def test_cheese_list_resource_from_model(dbsession):  # noqa: F811
    from pyramid_listing_example.resources import CheeseListResource
    from pyramid_listing_example.resources import CheeseResource

    # using a dummy request as a model since it provides properties just
    # from initialization
    model = DummyRequest(id=1)
    request = DummyRequest(dbsession=dbsession)
    resource = CheeseListResource(request)
    child = resource.resource_from_model(model)
    assert isinstance(child, CheeseResource)
    assert child.model == model
    assert child.__name__ == 1
    assert child.__parent__ == resource
