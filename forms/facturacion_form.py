# forms/facturacion_form.py

from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    cliente_id = SelectField(
        'Cliente',
        coerce=int,
        validators=[
            DataRequired(message="Debe seleccionar un cliente")
        ]
    )

    total = DecimalField(
        'Total ($)',
        places=2,
        validators=[
            DataRequired(message="El total es obligatorio"),
            NumberRange(
                min=0.01,
                message="El total debe ser mayor a 0"
            )
        ]
    )

    submit = SubmitField('Registrar Factura')