from django import forms


class ContactForm(forms.Form):
	name = forms.CharField(max_length=100, required=False)
	email = forms.CharField(max_length=100, required=False)
	number = forms.CharField(max_length=100, required=False)
	question = forms.CharField(max_length=200, required=False)
	message = forms.CharField(max_length=1000, required=False)