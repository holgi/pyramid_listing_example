''' resources for travesal style routing '''

from pyramid_listing import ListingResource

from .models import Cheese


class CheeseResource:
    ''' a resource for the Cheese database model '''

    def __init__(self, model, parent):
        self.model = model
        self.__name__ = model.id
        self.__parent__ = parent
        
        
class CheeseListResource(ListingResource):
    ''' A result list resource, you're propably here for this '''

    # define default order-by field and direction
    default_order_by_field = 'name'
    default_order_by_direction = 'asc'

    def get_base_query(self, request):
        ''' setup of the basic database query

        :param pyramid.Request request: request object
        :returns: the basic sqlalchemy query for the listing

        The base query can be used for basic filtering that should be applied 
        in all cases; for example to filter out any products that are not in 
        stockor ariticles in draft mode.

        This method is orignially defined in 
        ``pyramid_listing.listing.SQLAlchemyListing``
        '''
        return request.dbsession.query(Cheese)

    def get_filtered_query(self, base_query, request):
        ''' setup of the database query for a specific view

        :param sqlalchemy.Query base_query: the basic query for the listing
        :param pyramid.Request request: request object
        :returns: sqlalchemy query with custom filters

        the filtered query extends the base query and applies filters for a
        specific view, like show only blue cheeses. This query is used for
        calulating pagination and sorting is applied when listing child
        resources.

        It is important to remember applied filters if they should be used for
        constructing other urls' query parameters.

        This method is orignially defined in 
        ``pyramid_listing.listing.SQLAlchemyListing``
        '''
        search = request.GET.get('search')
        if search is not None and search.strip():
            # remember this for creaing further query parameters
            self.remember('search', search)
            term = f'%{search}%'
            return base_query.filter(Cheese.description.ilike(term))
        return base_query

    def get_order_by_field(self, identifier):
        ''' returns the SQLalchemy model field to sort by or None

        :param str identifier: a identifier for the field to sort by
        :returns: SQLalchemy model field or None

        This method is orignially defined in 
        ``pyramid_listing.listing.SQLAlchemyListing``
        '''
        map = {
            'name': Cheese.name,
            'country': Cheese.country,
            'region': Cheese.region,
            }
        return map.get(identifier, None)

    def resource_from_model(self, model):
        ''' returns a child resource from an sqlalchemy model instance 

        This method is orignially defined in 
        ``pyramid_listing.resource.ListingResource``
        '''
        return CheeseResource(model, self)

