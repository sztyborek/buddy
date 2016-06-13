from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras import SelectDateWidget
from .models import Project
from users.models import Skill

class SkillsTextInput(TextInput):
    def _format_value(self, value, *args, **kwargs):
        print value
        for skill in value:
            print skill.programming_lang
        super(SkillsTextInput, self)._format_value(value, *args, **kwargs)

print dir(SkillsTextInput)

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'expiration_date', 'number_of_users_required', 'opensource', 'url', 'skills')
        widgets = {
	    'name': Textarea(attrs={'rows':2, 'cols':50}),
	    'description': Textarea(attrs={'rows':2, 'cols':45}),
	    'expiration_date': SelectDateWidget(),
	    'number_of_users_required': NumberInput(attrs={'style':'text-align:right'}),
	    'url': TextInput(attrs={'size':54}),
        'skills': SkillsTextInput(),
	    }

class SkillForm(ModelForm):
    programming_lang = forms.CharField(required=False)
    class Meta:
        model = Skill
        exclude = ('skills',)

    def validate_unique(self):
        return True
