from django.contrib.auth import forms, get_user_model
from django.forms import ModelForm, Textarea
from .models import ListingModel


class UserCreationForm(forms.UserCreationForm):
    """
    Custom form for:
    1. validating (cleaning) fields;
    2. saving instance from validated data;
    3. rendering form in template.
    """
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'phone']


class ListingForm(ModelForm):
    """
    Listing form, used for:
    1. HTML form rendering;
    2. client-side <form> validation;
    3. server-side ListingForm validation;
    4. cleanded Model instance saving.
    """
    class Meta:
        """
        Override default ModelForm settings
        from inside a class.
        """
        model = ListingModel
        fields = ["title", "condition", "starting_price",
                  "start_time", "end_time", "description"]
        widgets = {"description": Textarea(
            attrs={'cols': 80, 'rows': 20, 'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        """
        Statement-style form customization.
        """
        # Pass all got arguments to the parent class
        super(ModelForm, self).__init__(*args, **kwargs)

        # Change class atribute of widget of field of all visible boundfields
        for boundfield in self.visible_fields():
            boundfield.field.widget.attrs['class'] = 'form-control'
