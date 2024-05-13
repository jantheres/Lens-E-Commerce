from dataclasses import fields

from django import forms
from . models import Orders


class  checkoutform(forms.ModelForm):
    class Meta:
        model=Orders
        fields=["address","mobile"]
