from django import forms
from .models import Order
from user_profile.models import UserProfile


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.user)
            self.fields['full_name'].initial = user_profile.default_full_name
            self.fields['email'].initial = self.user.email
            self.fields['phone_number'].initial = user_profile.default_phone_number
            self.fields['country'].initial = user_profile.default_country
            self.fields['postcode'].initial = user_profile.default_postcode
            self.fields['town_or_city'].initial = user_profile.default_town_or_city
            self.fields['street_address1'].initial = user_profile.default_street_address1
            self.fields['street_address2'].initial = user_profile.default_street_address2
            self.fields['county'].initial = user_profile.default_county
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County', 'state_or_locality': 'State or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
        
        if 'user' in kwargs and kwargs['user'].is_authenticated:
            user_profile = UserProfile.objects.get(user=kwargs['user'])
            for field in self.fields:
                self.fields[field].initial = getattr(user_profile, f'default_{field}', '')