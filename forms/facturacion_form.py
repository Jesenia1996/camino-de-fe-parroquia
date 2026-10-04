from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class FacturacionForm(FlaskForm):
    numero_factura = StringField('Número de Factura', validators=[
        DataRequired(message="El número de factura es obligatorio"),
        Length(max=20, message="Máximo 20 caracteres")
    ])
    fecha_emision = DateField('Fecha de Emisión', 
        format='%Y-%m-%d',
        validators=[DataRequired(message="La fecha es obligatoria")]
    )
    cliente = StringField('Identificación del Cliente', validators=[
        DataRequired(message="La identificación es obligatoria"),
        Length(max=20, message="Máximo 20 caracteres")
    ])
    total = IntegerField('Total a Pagar ($)', validators=[
        DataRequired(message="El total es obligatorio"),
        NumberRange(min=1, message="El total debe ser mayor a 0")
    ])
    submit = SubmitField('Emitir Factura')