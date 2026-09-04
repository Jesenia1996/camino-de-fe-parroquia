from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(), Length(min=5, max=120)
    ])
    documento = StringField('Documento / Cédula', validators=[
        DataRequired(), Length(min=10, max=13)
    ])
    correo = EmailField('Correo Electrónico', validators=[
        DataRequired(), Email(message="Ingrese un correo válido")
    ])
    direccion = StringField('Dirección', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    submit = SubmitField('Guardar Cliente')