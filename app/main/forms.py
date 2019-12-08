from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import User, List, Item

class ListCreationForm(FlaskForm):
    listname = StringField('Новый список', validators=[DataRequired()])
    submit = SubmitField('Создать')

class ListEditionForm(FlaskForm):
    listname = StringField('Новое название', validators=[DataRequired()])
    submit = SubmitField('Изменить')

class ItemAdditionForm(FlaskForm):
    itemname = StringField('Новый продукт', validators=[DataRequired()])
    submit = SubmitField('Добавить')
"""
class DeleteListForm(FlaskForm):
    delete = SubmitField('Удалить список')

class DeleteItemForm(FlaskForm, item_id):
    item = Item.query.filter_by(id=item_id)
    delete = SubmitField('Удалить продукт')
"""