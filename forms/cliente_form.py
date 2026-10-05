from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):

    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(max=100)
        ]
    )

    cedula = StringField(
        'Cédula',
        validators=[
            Length(max=20)
        ]
    )

    telefono = StringField(
        'Teléfono',
        validators=[
            Length(max=20)
        ]
    )

    correo = StringField(
        'Correo',
        validators=[
            Email(message="Ingrese un correo válido")
        ]
    )

    submit = SubmitField('Guardar Cliente')