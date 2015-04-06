from app import app, auth
from flask import g
from flask import jsonify


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.api_user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})
