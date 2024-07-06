from django import forms
from .models import Rating

# inspired by Desphinx tutorial:
# https://www.youtube.com/watch?v=TIDldj2BDuY
class RateProductForm(forms.ModelForm):
    '''
    Rating Form, to rate Products
    '''
    # rating = forms.ChoiceField(choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')], widget=forms.RadioSelect)
   
    class Meta:
        model =  Rating
        fields = ['rating']
        

