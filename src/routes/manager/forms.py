from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, IPAddress, NumberRange, Length

class MakeBotForm(FlaskForm):
    name = StringField('Bot Name', validators=[DataRequired(), Length(min=2, max=50)])
    ip = StringField('IP Address', validators=[DataRequired(), IPAddress()])
    port = IntegerField('Port', validators=[DataRequired(), NumberRange(min=1, max=65535)])
    steam_id = StringField('Steam ID', validators=[DataRequired(), Length(min=10, max=50)])
    token = StringField('Token', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Create Bot')


class MakeSwitchForm(FlaskForm):
    switch_key = StringField('Switch Key', validators=[DataRequired(), Length(min=5, max=50)])
    switch_name = StringField('Switch Name', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('add_switch')
