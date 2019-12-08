from app import db, login
from flask_login import UserMixin
from flask import url_for, current_app
import base64
from datetime import datetime, timedelta
import os
import json

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class User(PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=True, unique=True)
    email = db.Column(db.String(30), index=True, unique=True)
    password = db.Column(db.String(25))
    lists = db.relationship('List', backref='author', lazy='dynamic')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    def get_lists(self):
        return List.query.filter(List.user_id == self.id).order_by(List.id).all()

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'list_count': self.lists.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'lists': url_for('api.get_lists_of_user', id=self.id)
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class List(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listname = db.Column(db.String(30), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='dir', lazy='dynamic')

    def __repr__(self):
        return '<List {}>'.format(self.listname)

    def get_items(self):
        return Item.query.filter(Item.list_id == self.id).order_by(Item.id).all()

    def to_dict(self):
        data = {
            'id': self.id,
            'listname': self.listname,
            'user_id': self.user_id,
            'item_count': self.items.count(),
            '_links': {
                'self': url_for('api.get_list', id=self.id),
                'items': url_for('api.get_items_of_list', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['listname']:
            if field in data:
                setattr(self, field, data[field])


class Item(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(30), index=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.itemname)

    def to_dict(self):
        data = {
            'id': self.id,
            'itemname': self.itemname,
            'list_id': self.list_id,
            '_links': {
                'self': url_for('api.get_item', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['itemname']:
            if field in data:
                setattr(self, field, data[field])
