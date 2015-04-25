from app import app, api
from app.pagination.pagination import Pagination
from app.pagination.ordering import Ordering
from flask_restful import abort
from flask.ext.restplus import Resource


class PaginatedResource(Resource):

    PAGE_SIZE = 'page_size'
    PAGE_NUMBER = 'page'

    ORDER_BY = 'order_by'
    ORDER_DIRECTION = 'order_direction'

    @app.errorhandler(ValueError)
    def handle_value(error):
        abort(400, message=error.message)

    def get_pagination(self):
        parser = api.parser()
        parser.add_argument(self.PAGE_SIZE, type=int, location='args')
        parser.add_argument(self.PAGE_NUMBER, type=int, location='args')
        args = parser.parse_args()
        return Pagination(args.get(self.PAGE_NUMBER), args.get(self.PAGE_SIZE))

    def get_ordering(self):
        parser = api.parser()
        parser.add_argument(self.ORDER_BY, type=str, location='args')
        parser.add_argument(self.ORDER_DIRECTION, type=str, location='args')
        args = parser.parse_args()
        return Ordering(args.get(self.ORDER_BY),
                        args.get(self.ORDER_DIRECTION))

    def paginated_result_to_json(self, paginate):
        return dict(page=paginate.page,
                    page_size=paginate.per_page,
                    total=paginate.total,
                    results=[item.to_json() for item in paginate.items])


def paginated(func):
    @api.doc(params={PaginatedResource.PAGE_SIZE: 'Page size'})
    @api.doc(params={PaginatedResource.PAGE_NUMBER: 'Page number'})
    @api.doc(params={PaginatedResource.ORDER_BY: 'Which field to order by'})
    @api.doc(params={PaginatedResource.ORDER_DIRECTION:
                     'Direction to order in'})
    def to_paginate(*args, **kwargs):
        return func(*args, **kwargs)
    return to_paginate
