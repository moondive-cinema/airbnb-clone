from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):

    accuracy = forms.IntegerField(max_value=5, min_value=0)
    communication = forms.IntegerField(max_value=5, min_value=0)
    cleanliness = forms.IntegerField(max_value=5, min_value=0)
    location = forms.IntegerField(max_value=5, min_value=0)
    check_in = forms.IntegerField(max_value=5, min_value=0)
    value = forms.IntegerField(max_value=5, min_value=0)

    class Meta:
        model = models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )

    def save(self):
        review = super().save(commit=False)
        return review
