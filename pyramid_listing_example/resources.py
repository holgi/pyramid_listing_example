from pyramid_listing import ListingResource

from .models import Cheese


class CheeseResource:

    def __init__(self, model, parent):
        self.model = model
        self.__name__ = model.id
        self.__parent__ = parent
        
        
class CheeseListResource(ListingResource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_order_by_field = 'name'
        self.default_order_by_direction = 'asc'

    def get_base_query(self, request):
        return request.dbsession.query(Cheese)

    def get_filtered_query(self, base_query, request):
        search = request.GET.get('search')
        if search is not None:
            # remember this for creaing further query parameters
            self.remember('search', search)
            return base_query.filter(Cheese.description.ilike(search))
        return base_query

    def get_order_by_field(self, identifier):
        map = {
            'name': Cheese.name,
            'country': Cheese.country,
            'region': Cheese.region,
            }
        return map.get(identifier.lower(), None)

    def resource_from_model(self, model):
        return CheeseResource(model, self)

