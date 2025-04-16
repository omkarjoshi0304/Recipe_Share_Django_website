from django import forms
from .models import ContactMessage
from django import forms
from .models import MarketplaceItem, ItemReview, ItemOffer, ItemCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'email', 'ingredients', 'category', 'duration', 'uploaded_file']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ItemForm(forms.ModelForm):
    class Meta:
        model = MarketplaceItem
        fields = ['title', 'description', 'price', 'condition', 'image', 'category']
        
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price

class ItemReviewForm(forms.ModelForm):
    class Meta:
        model = ItemReview
        fields = ['rating', 'comment']

class ItemOfferForm(forms.ModelForm):
    class Meta:
        model = ItemOffer
        fields = ['offer_price', 'message']
        
    def clean_offer_price(self):
        price = self.cleaned_data.get('offer_price')
        if price <= 0:
            raise forms.ValidationError("Offer price must be greater than zero")
        return price

class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ['name', 'description']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']


def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required")
        return email