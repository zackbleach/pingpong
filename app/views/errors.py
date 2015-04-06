from app import app, db
from flask import jsonify, make_response


@app.errorhandler(ValueError)
def bad_request(error):
    db.session.rollback()
    return make_error(error.message, 400)


@app.errorhandler(404)
def not_found(error):
    return make_error("Not Found", 404)


@app.errorhandler(401)
def unauthorised(error):
    return make_error("Unauthorised", 401)


def make_error(message, code):
    error = {"message": message,
             "status_code": code}
    return make_response(jsonify(error), code)
