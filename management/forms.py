# forms.py
from django import forms
from .models import Management, ManagementRule, ConverterTranslator
from users.models import UserProfile


class ManagementForm(forms.ModelForm):
    """
    this is the management form
    """
    #  all the date added here
    date_of_lease_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    first_day_of_term_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    last_day_of_term_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    lease_expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    notice_term_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    index_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    start_payment_schedule = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    end_payment_schedule = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    index_date_sr2 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])

    #  all the decimal add here
    required_amount = forms.DecimalField(max_digits=10, decimal_places=2,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))

    term = forms.DecimalField(max_digits=10, decimal_places=2,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    notice_term = forms.DecimalField(max_digits=10, decimal_places=2,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gross_area = forms.DecimalField(max_digits=10, decimal_places=2,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    net_area = forms.DecimalField(max_digits=10, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amount_rent = forms.DecimalField(max_digits=10, decimal_places=2,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amount_service_charge = forms.DecimalField(max_digits=10, decimal_places=2,
                                               widget=forms.NumberInput(
                                                   attrs={'class': 'form-control'}))
    amount_others = forms.DecimalField(max_digits=10, decimal_places=2,
                                       widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amount_discount = forms.DecimalField(max_digits=10, decimal_places=2,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))

    vat_code = forms.DecimalField(max_digits=10, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    vat_rate = forms.DecimalField(max_digits=10, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    vat_amount = forms.DecimalField(max_digits=10, decimal_places=2,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))

    value = forms.DecimalField(max_digits=10, decimal_places=2,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    value_sr2 = forms.DecimalField(max_digits=10, decimal_places=2,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))

    # integer field
    type_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    charge_frequency = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    option_by_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    index_series = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    security_type_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    term_frequency = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    index_frequency = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Management
        fields = "__all__"
        widgets = {
            'date_field': forms.DateInput(format='%y-%m-%d'),  # Specify the desired display format for the date field
        }


class ManagementRuleForm(forms.ModelForm):
    """
    this  form is used to update rules
    """

    class Meta:
        model = ManagementRule
        fields = "__all__"


class ConverterTranslatorForm(forms.ModelForm):
    """
    this is used to update or create the convert transal
    """

    class Meta:
        model = ConverterTranslator
        fields = "__all__"
