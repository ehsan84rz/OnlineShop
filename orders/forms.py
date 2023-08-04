from django import forms
from django.utils.translation import gettext as _

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'order_notes']
        widgets = {
            'order_notes': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': _('If you have any notes, Please write here')
            })
        }
