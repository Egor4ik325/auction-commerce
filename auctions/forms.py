from datetime import timedelta, timezone, datetime

from django.contrib.auth import forms, get_user_model
from django.forms import ModelForm, TimeField, DateField, TimeInput, DateInput, DateTimeInput, Textarea
from django.utils.translation import ugettext_lazy as _
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
        Attribute-style form customization.
        Override default ModelForm settings.
        """
        model = ListingModel
        # Editable form fields
        fields = ["title", "condition", "starting_price",
                  "start_datetime", "end_datetime", "description"]
        widgets = {"description": Textarea(
            attrs={'cols': 80, 'rows': 10, 'class': 'form-control'})}
        # field help_text is not HTML escaped in autoform
        help_texts = {
            "description": 'Description of item at auction'}

    def __init__(self, *args, **kwargs):
        """
        Statement-style form customization.
        """
        def current_datetime_string():
            """Get current time with timezone offset."""
            msk_tz = timezone(timedelta(hours=3), 'MSK')
            cur_dt = datetime.now(tz=msk_tz) + timedelta(hours=1)
            cur_dt_str = cur_dt.strftime('%Y-%m-%d %H:00:00')
            return cur_dt_str

        # Default dynamic initial values:
        kwargs['initial'] = kwargs.get('initial', {})
        kwargs['initial']['start_datetime'] = current_datetime_string()

        # Pass all got arguments to the parent class
        super(ModelForm, self).__init__(*args, **kwargs)

        # Post-init:
        # TODO: move all HTML related to the template
        # Rendering customization (only visible fields)
        for boundfield in self.visible_fields():
            # Change class atribute of widget of fields
            boundfield.field.widget.attrs['class'] = 'form-control'
            # Format help_text for HTML form
            boundfield.field.help_text = f'<small class="form-text text-muted">{boundfield.field.help_text}</small>'
