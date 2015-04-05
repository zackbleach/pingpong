from app import app, db
from flask import jsonify, make_response


@app.errorhandler(ValueError)
def bad_request(error):
    db.session.rollback()
    status_code = 400
    error = {"message": error.message,
             "status_code": status_code}
    return make_response(jsonify(error), status_code)
