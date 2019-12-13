# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import app, db
from app.main.forms import ListCreationForm, ListEditionForm, ItemAdditionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, List, Item
from app.main import bp

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = current_user
    lists = user.get_lists()
    items = []
    for list in lists:
        items += list.get_items()
    form = ListCreationForm()
    if form.validate_on_submit():
        list = List(listname=form.listname.data, author=current_user)
        db.session.add(list)
        db.session.commit()
        flash('Новый список создан')
        return redirect(url_for('main.index'))
    return render_template('index.html', user=user, lists=lists, items=items, form=form)


@bp.route('/list/<list_id>', methods=['GET', 'POST'])
@login_required
def show_list(list_id):
    list = List.query.filter_by(id=list_id).first_or_404()
    items = list.get_items()
    form = ItemAdditionForm()
    if form.validate_on_submit():
        item = Item(itemname=form.itemname.data, dir=list)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('main.show_list', list_id=list.id))
    # form2 = DeleteItemForm
    # if form2.validate_on_submit():
    #     list =
    return render_template('list.html', title='Список '+list.listname, list=list, items=items, form=form)


@bp.route('/lists/<list_id>', methods=['GET', 'POST'])
def show_list_from_app(list_id):
    list = List.query.filter_by(id=list_id).first_or_404()
    items = list.get_items()
    return render_template('list_from_app.html', title='Список '+list.listname, list=list, items=items)

@bp.route('/list/<list_id>/edit_list', methods=['GET', 'POST'])
@login_required
def edit_list(list_id):
    list = List.query.filter_by(id=list_id).first_or_404()
    form = ListEditionForm()
    if form.validate_on_submit():
        list.listname = form.listname.data
        db.session.commit()
        flash('Список изменен')
        return redirect(url_for('main.show_list', list_id=list.id))
    elif request.method == 'GET':
        form.listname.data = list.listname
    return render_template('edit_list.html', title='Изменить список', form=form)
