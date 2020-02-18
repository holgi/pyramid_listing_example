from pyramid.view import notfound_view_config, view_config


@view_config(
    context="pyramid_listing_example.resources.CheeseListResource",
    renderer="./templates/cheese_list.jinja2",
)
def cheese_list(context, request):
    return {}


@view_config(
    context="pyramid_listing_example.resources.CheeseResource",
    renderer="./templates/cheese_detail.jinja2",
)
def one_cheese(context, request):
    return {}


@notfound_view_config(renderer="./templates/404.jinja2")
def notfound_view(request):
    request.response.status = 404
    return {}
