from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    documento = StringField('Documento', validators=[DataRequired(), Length(max=20)])
    correo = StringField('Correo', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=20)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Guardar Cliente')