from __future__ import division
from django.forms import ModelForm, Textarea
from .models import UserModel
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab, Div
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset


class UserModelDescriptionForm(ModelForm):

    class Meta:
        model = UserModel
        fields = ('name', 'description')
        widgets = {
          'description': Textarea(attrs={'rows':2, 'cols':20}),
        }

    def __init__(self, *args, **kwargs):
        super(UserModelDescriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'description-id'
        self.helper.form_method = 'post'
        self.helper.form_action = "/my_models_settings/" + str(self.instance.id) + '/'
        self.helper.add_input(Submit('submit', 'Save', css_class="pull-right"))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field('name', placeholder="New model's name"),
            Field('description', placeholder="Model's description"))


# widgets = {
#   'description': Textarea(attrs={'rows':2, 'cols':20}),
#   'simulation_date': DateTimePicker(
#         options={"format": "YYYY-MM-DD HH:mm",
#                  "pickSeconds": False},
#         attrs={'placeholder': 'ex: 2016-06-17 23:50'}
#     )
# }
