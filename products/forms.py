from django import forms
from .widgets import CustomClearableFileInput
from .models import Rating, Product, Category

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
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

# inspired by CI boutique ado:
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'