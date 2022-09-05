from django import forms
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit


class AddComment(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['rows'] = 1
        self.fields['content'].widget.attrs['columns'] = 10

    class Meta:
        model = Comment
        fields = ("content",)
        labels={"content": "comment here:"}


class Genres(forms.Form):
    choices = (
        (1, "Happiness"),
        (2, "Sadness"),
        (3, "Fear"),
        (4, "Anger"),
        (5, "Disgust"),
        (6, "Surprise"),
        (7, "Amusement"),
        (8, "Contempt"),
        (9, "Embarrassment"),
        (10, "Excitement"),
        (11, "Guilt"),
        (12, "Pride"),
        (13, "Relief"),
        (14, "Satisfaction"),
        (15, "Shame"),
        (16, "Not Intrested in this genre"),
        (17, "Intrested in this genre")
    )

    Alternative = forms.MultipleChoiceField(choices=choices)
    Anime = forms.MultipleChoiceField(choices=choices)
    Blues = forms.MultipleChoiceField(choices=choices)
    Childrens_music = forms.MultipleChoiceField(choices=choices)
    Classical = forms.MultipleChoiceField(choices=choices)
    Comedy = forms.MultipleChoiceField(choices=choices)
    Commercial = forms.MultipleChoiceField(choices=choices)
    Country = forms.MultipleChoiceField(choices=choices)
    Dance = forms.MultipleChoiceField(choices=choices)
    Disney = forms.MultipleChoiceField(choices=choices)
    Easy_listening = forms.MultipleChoiceField(choices=choices)
    Electronic = forms.MultipleChoiceField(choices=choices)
    Enka = forms.MultipleChoiceField(choices=choices)
    French_pop = forms.MultipleChoiceField(choices=choices)
    German_Folk = forms.MultipleChoiceField(choices=choices)
    German_pop = forms.MultipleChoiceField(choices=choices)
