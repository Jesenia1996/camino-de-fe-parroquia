from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ProveedorForm(FlaskForm):
    nombre_empresa = StringField('Nombre de la Empresa', validators=[
        DataRequired(), Length(min=5, max=120)
    ])
    ruc = StringField('RUC', validators=[
        DataRequired(), Length(min=13, max=13, message="El RUC debe tener 13 dígitos")
    ])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    pais = StringField('País', validators=[DataRequired()])
    submit = SubmitField('Guardar Proveedor')