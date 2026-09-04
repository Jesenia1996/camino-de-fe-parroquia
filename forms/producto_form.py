from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        'Nombre del Producto',
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(min=3, max=100)
        ]
    )

    categoria = StringField(
        'Categoría',
        validators=[
            DataRequired(message="La categoría es obligatoria")
        ]
    )

    cantidad = IntegerField(
        'Cantidad',
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                message="No se permiten valores negativos"
            )
        ]
    )

    precio = DecimalField(
        'Precio ($)',
        places=2,
        validators=[
            DataRequired(),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor a 0"
            )
        ]
    )

    submit = SubmitField('Guardar Producto')