from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturacionForm(FlaskForm):
    numero_factura = StringField('Número de Factura', validators=[DataRequired()])
    fecha_emision = DateField('Fecha de Emisión', validators=[DataRequired()])
    cliente = StringField('Identificación del Cliente', validators=[DataRequired()])
    total = IntegerField('Total a Pagar ($)', validators=[
        DataRequired(), NumberRange(min=1, message="El total debe ser mayor a 0")
    ])
    submit = SubmitField('Emitir Factura')