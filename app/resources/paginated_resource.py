from app import app, api
from app.helpers.pagination import Pagination
from flask_restful import abort
from flask.ext.restplus import Resource


class PaginatedResource(Resource):

    @app.errorhandler(ValueError)
    def handle_value(error):
        abort(400, message=error.message)

    def get_pagination(self):
        parser = api.parser()
        parser.add_argument('page_size', type=int, location="args")
        parser.add_argument('page', type=int, location="args")
        args = parser.parse_args()
        return Pagination(args.get("page"), args.get("page_size"))

    def paginated_result_to_json(self, paginate):
        return dict(page=paginate.page,
                    page_size=paginate.per_page,
                    total=paginate.total,
                    results=[item.to_json() for item in paginate.items])
