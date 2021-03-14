from django import forms
from .models import *

class RouterForm(forms.ModelForm):
    class Meta:
        model = RouterList
        fields = ('name','ip_address', 'username', 'password','routerboard' )
        widgets = {'name': forms.HiddenInput(),
            'ip_address':forms.TextInput(attrs={'placeholder': '192.168.x.x','autocomplete':'off'}),
            'username':forms.TextInput(attrs={'placeholder': 'username','autocomplete':'off'}),
            'password':forms.PasswordInput(attrs={'placeholder': '*******','autocomplete':'off'}),
            'routerboard': forms.HiddenInput(),
        }

class ClientForm(forms.Form):
    CHOICES = (
                ('any', 'any'),
                ('l2tp', 'l2tp'),
                ('pppoe', 'pppoe'),
                ('pptp', 'pptp'),
                ('ovpn', 'ovpn'),
                ('sstp', 'sstp'),
            )
    name     = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'nama client','autocomplete':'off'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value = True, attrs={'placeholder': '********'}))
    service  = forms.ChoiceField(choices=CHOICES)
    profile  = forms.ChoiceField()




