from app import app
from flask import jsonify, make_response


@app.errorhandler(ValueError)
def bad_request(error):
    status_code = 400
    error = {"message": error.message,
             "status_code": status_code}
    return make_response(jsonify(error), status_code)
