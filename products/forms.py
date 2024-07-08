from django import forms
from .models import Rating

# inspired by Desphinx tutorial:
# https://www.youtube.com/watch?v=TIDldj2BDuY
class RatingForm(forms.ModelForm):
    '''
    Rating Form, to rate Products
    '''
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    review = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Rating
        fields = ['rating', 'review']

