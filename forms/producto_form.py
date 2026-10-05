# forms/producto_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        'Nombre del Recurso',
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(min=3, max=100)
        ]
    )

    descripcion = TextAreaField(
        'Descripción',
        validators=[
            Length(max=255, message="La descripción no puede superar los 255 caracteres")
        ]
    )

    precio = DecimalField(
        'Precio ($)',
        places=2,
        validators=[
            DataRequired(message="El precio es obligatorio"),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor a 0"
            )
        ]
    )

    stock = IntegerField(
        'Stock',
        validators=[
            DataRequired(message="El stock es obligatorio"),
            NumberRange(
                min=0,
                message="No se permiten valores negativos"
            )
        ]
    )

    submit = SubmitField('Guardar Recurso')