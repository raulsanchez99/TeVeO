# Defines una clase para tu formulario que hereda de forms.Form
from django import forms

class ConfigForm(forms.Form):
    username = forms.CharField(
        label='Nombre de Usuario', max_length=100, required=False)

    font_size = forms.ChoiceField(
        choices=[('large', 'Grande'),
                 ('standard', 'Normal'),
                 ('small', 'Pequeña')])


    font_family = forms.ChoiceField(choices=[
        ('Arial', 'Arial'),
        ('Times New Roman', 'Times New Roman'),
        ('Courier New', 'Courier New'),
    ])

