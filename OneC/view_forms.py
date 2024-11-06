from django import forms


class CreateCheckViewForm(forms.Form):

    start_date = forms.DateField(widget=forms.DateInput())
    end_date = forms.DateField(widget=forms.DateInput())
    check_date = forms.DateField(widget=forms.DateInput())
    client = forms.Select(widget=forms.Select)
    our_company = forms.CharField(widget=forms.TextInput())
    check_type = forms.CharField(widget=forms)
    order_list = ''
