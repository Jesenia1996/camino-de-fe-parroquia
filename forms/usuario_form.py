# forms/usuario_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class UsuarioForm(FlaskForm):

    usuario = StringField(
        'Usuario',
        validators=[
            DataRequired(message="El usuario es obligatorio"),
            Length(min=3, max=50)
        ]
    )

    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message="La contraseña es obligatoria"),
            Length(min=6, max=100)
        ]
    )

    submit = SubmitField('Registrarse')