from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(max=100)
    ])
    descripcion = TextAreaField('Descripción', validators=[Length(max=255)])
    precio = FloatField('Precio', validators=[
        DataRequired(message="El precio es obligatorio"),
        NumberRange(min=0.01, message="El precio debe ser mayor a 0")
    ])
    stock = IntegerField('Stock', validators=[
        DataRequired(message="El stock es obligatorio"),
        NumberRange(min=0, message="El stock no puede ser negativo")
    ])
    categoria = StringField('Categoría', validators=[
        DataRequired(message="La categoría es obligatoria"),
        Length(max=50)
    ])
    submit = SubmitField('Guardar Producto')