from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from models.enums import RelationOperator, TriggerActionType


class TriggerForm(FlaskForm):
    operator = SelectField('Operator', choices=RelationOperator.choices())
    controller = SelectField('Controller', coerce=int)
    action_type = SelectField('Action Type', choices=TriggerActionType.choices())
    threshold = IntegerField('Threshold')
