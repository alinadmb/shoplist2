from app.api import bp
from flask import jsonify, request, url_for
from app.models import User, List, Item
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth

""""
@bp.route('/users/<string:username>', methods=['GET'])
def login(username):
    return jsonify(User.query.filter_by(username=username).first_or_404().to_dict())
"""

@bp.route('/users/<int:id>', methods=['GET'])
# @token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>/lists', methods=['GET'])
# @token_auth.login_required
def get_lists_of_user(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)
    data = User.to_collection_dict(user.lists, page, per_page,
                                   'api.get_lists_of_user', id=id)
    return jsonify(data)

@bp.route('/users', methods=['POST'])
# @token_auth.login_required
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/login', methods=['POST'])
# @token_auth.login_required
def login():
    data = request.get_json() or {}
    if 'username' not in data or 'password' not in data:
        return bad_request('must include username and password fields')
    user = User.query.filter_by(username=data['username']).first()
    if user is None:
        return bad_request('wrong username')
    if user.password != data['password']:
        return bad_request('wrong password')
    response = jsonify(user.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['DELETE'])
# @token_auth.login_required
def remove_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/lists/<int:id>', methods=['GET'])
# @token_auth.login_required
def get_list(id):
        return jsonify(List.query.get_or_404(id).to_dict())

@bp.route('/lists/<int:id>/items', methods=['GET'])
# @token_auth.login_required
def get_items_of_list(id):
    list = List.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)
    data = List.to_collection_dict(list.items, page, per_page,
                                   'api.get_items_of_list', id=id)
    return jsonify(data)

@bp.route('/users/<int:u_id>/lists', methods=['POST'])
# @token_auth.login_required
def create_list_for_user(u_id):
    user = User.query.get_or_404(u_id)
    data = request.get_json() or {}
    if not data:
        return bad_request('must include something')
    list = List()
    list.from_dict(data)
    list.user_id = u_id
    db.session.add(list)
    db.session.commit()
    response = jsonify(list.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_list', id=list.id)
    return response

@bp.route('/lists/<int:id>', methods=['PUT'])
# @token_auth.login_required
def update_list(id):
    list = List.query.get_or_404(id)
    data = request.get_json() or {}
    if not data:
        return bad_request('Build should contain something')
    list.from_dict(data)
    db.session.commit()
    return jsonify(list.to_dict())

@bp.route('/lists/<int:id>', methods=['DELETE'])
# @token_auth.login_required
def remove_list(id):
    list = List.query.get_or_404(id)
    db.session.delete(list)
    db.session.commit()
    return jsonify(list.to_dict())



@bp.route('/items/<int:id>', methods=['GET'])
# @token_auth.login_required
def get_item(id):
    return jsonify(Item.query.get_or_404(id).to_dict())

@bp.route('/lists/<int:l_id>/items', methods=['POST'])
# @token_auth.login_required
def create_item_for_list(l_id):
    list = List.query.get_or_404(l_id)
    data = request.get_json() or {}
    if not data:
        return bad_request('must include something')
    item = Item()
    item.from_dict(data)
    item.list_id = l_id
    db.session.add(item)
    db.session.commit()
    response = jsonify(item.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_item', id=item.id)
    return response

@bp.route('/items/<int:id>', methods=['PUT'])
# @token_auth.login_required
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json() or {}
    if not data:
        return bad_request('Build should contain something')
    item.from_dict(data)
    db.session.commit()
    return jsonify(item.to_dict())

@bp.route('/items/<int:id>', methods=['DELETE'])
# @token_auth.login_required
def remove_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(item.to_dict())
