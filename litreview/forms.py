from django import forms
from .models import Ticket, Review


class UploadTicketForm(forms.ModelForm):
    """Ticket form"""
    class Meta:
        model = Ticket
        fields = ("title", "description", "image", "user")


class UploadReviewForm(forms.ModelForm):
    """Review form"""
    class Meta:
        model = Review
        fields = ("headline", "body", "rating", "ticket", "user")

