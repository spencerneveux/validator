from django import forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(max_length=254, required=True)
    subject = forms.CharField(max_length=254, required=True)
    message = forms.CharField(widget=forms.Textarea)

class EmailForm(forms.Form):
    to_email = forms.EmailField(max_length=254, required=True, label="Send To")
    message = forms.CharField(widget=forms.Textarea, label="Tell your friends what you think")
    article_link = forms.CharField(max_length=254, widget=forms.HiddenInput())