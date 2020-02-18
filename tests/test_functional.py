""" functional tests for ordr2 """

import pytest
import transaction
import webtest

from . import APP_SETTINGS, add_example_data


@pytest.fixture(scope="module")
def testapp():
    """ fixture for using webtest """
    from pyramid_listing_example.models.meta import Base
    from pyramid_listing_example.models import get_tm_session
    from pyramid_listing_example import main

    app = main({}, **APP_SETTINGS)
    testapp = webtest.TestApp(app)

    session_factory = app.registry["dbsession_factory"]
    engine = session_factory.kw["bind"]
    Base.metadata.create_all(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        add_example_data(dbsession)
        dbsession.flush()

    yield testapp


def get_first_cheese(response):
    return response.html.td.a.string


@pytest.mark.parametrize(
    "page,expected",
    [
        (1, "Akkawi"),
        (2, "Castelo Branco cheese"),
        (3, "Kadaka juust"),
        (4, "Malaka"),
        (5, "Panquehue"),
        (6, "Redykołka"),
        (7, "Travnički (Vlašić) cheese"),
        (8, "Akkawi"),
    ],
)
def test_result_pagination_ten(testapp, page, expected):
    response = testapp.get(f"/?p={page}&n=10")
    assert get_first_cheese(response) == expected
    assert "<h2>" not in response


@pytest.mark.parametrize(
    "page,expected",
    [
        (1, "Akkawi"),
        (2, "Kadaka juust"),
        (3, "Panquehue"),
        (4, "Travnički (Vlašić) cheese"),
        (5, "Akkawi"),
    ],
)
def test_result_pagination_twenty(testapp, page, expected):
    response = testapp.get(f"/?p={page}&n=20")
    assert get_first_cheese(response) == expected
    assert "<h2>" not in response


@pytest.mark.parametrize(
    "order_by,direction,expected",
    [
        ("name", "asc", "Akkawi"),
        ("name", "desc", "Ġbejna"),
        ("country", "asc", "Passendale cheese"),
        ("country", "desc", "Guayanés cheese"),
        ("region", "asc", "Akkawi"),
        ("region", "desc", "Brie de Meaux"),
        ("unknown", "asc", "Akkawi"),
        ("name", "unknown", "Akkawi"),
    ],
)
def test_result_ordering(testapp, order_by, direction, expected):
    response = testapp.get(f"/?p=1&n=10&o={order_by}&d={direction}")
    assert get_first_cheese(response) == expected
    assert "<h2>" not in response


@pytest.mark.parametrize(
    "what,expected", [("", "Akkawi"), ("salt", "Gorgonzola")]
)
def test_search(testapp, what, expected):
    response = testapp.get(f"/?p=1&n=10&o=name&d=asc&search={what}")
    assert get_first_cheese(response) == expected
    if what:
        assert "<h2>" in response
    else:
        assert "<h2>" not in response


def test_cheesy_details(testapp):
    response = testapp.get("/50/")
    assert '<h2>The delicious "Roquefort"</h2>' in response


def test_not_found_view(testapp):
    response = testapp.get("/unknown/", status=404)
    assert "Cheese Not Found Error" in response
    assert response.status == "404 Not Found"
