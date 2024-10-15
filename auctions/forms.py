from django import forms
from django.forms import ModelForm
from .models import Category, List, Bid, Commentary

class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ['title', 'category', 'description', 'starting_bid',  'image_url']
        widget = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),  
        }

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")
    starting_bid = forms.DecimalField(max_digits=9, decimal_places=2, min_value=0, widget=forms.NumberInput(attrs={'step': '0.01'}))


    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

class CommentForm(ModelForm):
    class Meta:
        model = Commentary
        fields = ['headline', 'comment']
        widgets = {
            'headline': forms.TextInput(attrs={'placeholder': 'Título del comentario'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Escribe tu comentario...'}),
        }