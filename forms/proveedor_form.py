from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ProveedorForm(FlaskForm):
    nombre_empresa = StringField('Nombre de la Empresa', validators=[DataRequired(), Length(max=100)])
    ruc = StringField('RUC', validators=[DataRequired(), Length(max=20)])
    contacto = StringField('Persona de Contacto', validators=[DataRequired(), Length(max=100)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pais = StringField('País', validators=[DataRequired(), Length(max=50)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Guardar Proveedor')