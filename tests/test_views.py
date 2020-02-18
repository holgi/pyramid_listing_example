from pyramid.testing import DummyRequest


def test_cheese_list():
    from pyramid_listing_example.views import cheese_list

    assert cheese_list(None, None) == {}


def test_one_cheese():
    from pyramid_listing_example.views import one_cheese

    assert one_cheese(None, None) == {}


def test_notfound_view():
    from pyramid_listing_example.views import notfound_view

    request = DummyRequest()
    assert notfound_view(request) == {}
    assert request.response.status == "404 Not Found"
