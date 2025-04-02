from collections import defaultdict

from django import forms
from core.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', "span-2")

    class Meta:

        model = Recipe
        fields = ('title', 'description', 'preparation_time', 
        'preparation_time_unit', 'servings', 'servings_unit',
        'preparation_steps', 'cover', 'category')

        widgets = {

            'cover' : forms.FileInput(
                attrs={
                'class' : 'span-2'
                },
            ),
            'servings_unit' : forms.Select(
                choices=(
                    ('Porções','Porções'),
                    ('Pedaços','Pedaços'),
                    ('Pessoas','Pessoas'),
                ),
            ),

            'preparation_time_unit' : forms.Select(
                choices=(
                    ('Minutos','Minutos'),
                    ('Horas','Horas'),
                ),
            ),
        }


    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        
        cleaned_data = self.cleaned_data
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")

        if description == title:
            self._my_errors['title'].append(
                "Title can not be equal to description"
                )
            self._my_errors['description'].append(
                "Description can not be equal to title"
                )

        if self._my_errors:
            raise forms.ValidationError(self._my_errors)

        return super_clean
    
    def clean_title(self):
        title = self.cleaned_data.get("title")

        if len(title) < 5:
            self._my_errors['title'].append(
                "Title must have at least 5 characters"
                )

        return title
    
    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get("preparation_time")

        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append(
                "Preparation time must be greatte than 0"
                )
        
        return preparation_time 