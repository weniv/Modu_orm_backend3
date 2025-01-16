from django import forms


class PostForm(forms.Form):
    title = forms.CharField()
    contents = forms.CharField()
