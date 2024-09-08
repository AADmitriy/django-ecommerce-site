from django import forms
from .models import AvailableForShippingRegion, OrderAddress, OrderContact


def get_region_choices():
    if not AvailableForShippingRegion.objects.all().exists():
        new_region_names = ['Ukraine', 'France', 'Germany', 'Spain', 'Italy', 'Poland', 'Portugal']

        for region_name in new_region_names:
            AvailableForShippingRegion.objects.create(name=region_name)

    return [(region.name, region.name) for region in AvailableForShippingRegion.objects.all()]

class AddressForm(forms.ModelForm):
    class Meta:
        model = OrderAddress
        fields = {
            'country',
            'city',
            'address',
            'zipCode',
        }

        widgets = {
            'country': forms.Select(choices=get_region_choices(), attrs={'required': ''}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'required': ''}),
            'zipCode': forms.NumberInput(attrs={'placeholder': 'ZIP Code', 'required': ''}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'required': ''}),
        }


class OrderContactForm(forms.ModelForm):
    class Meta:
        model = OrderContact
        fields = {
            'firstname',
            'lastname',
            'phoneNumber',
            'email',
        }
        widgets = {
            'firstname': forms.TextInput(attrs={'placeholder': 'Firstname', 'required': ''}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Lastname', 'required': ''}),
            'phoneNumber': forms.NumberInput(attrs={'placeholder': 'Phone Number',  'type': 'tel', 'required': ''}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'required': ''})
        }
