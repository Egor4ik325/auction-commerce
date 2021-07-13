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


class TimeWidget(TimeInput):
    input_type = 'time'


class DateWidget(DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        # Always override widget format
        kwargs['format'] = '%Y-%m-%d'
        super().__init__(*args, **kwargs)


def current_datetime_strings():
    """Get current date and time with timezone offset."""
    msk_tz = timezone(timedelta(hours=3), 'MSK')
    cur_dt = datetime.now(tz=msk_tz) + timedelta(hours=1)
    cur_time_str = cur_dt.strftime('%H:00:00')
    cur_date_str = cur_dt.strftime('%Y-%m-%d')
    return cur_time_str, cur_date_str


def current_time_string():
    return current_datetime_strings()[0]


def current_date_string():
    return current_datetime_strings()[1]


class ListingForm(ModelForm):
    """
    Listing form, used for:
    1. HTML form rendering;
    2. client-side <form> validation;
    3. server-side ListingForm validation;
    4. cleanded Model instance saving.
    """
    # Split model start_datetime, end_datetime into multiple fields
    start_time = TimeField(required=True, widget=TimeWidget,
                           label=_("Listing start time"), initial=current_time_string())
    start_date = DateField(required=True, widget=DateWidget,
                           label=_("Listing start date"), initial=current_date_string())
    end_time = TimeField(required=True, widget=TimeWidget,
                         label=_("Listing end time"))
    end_date = DateField(required=True, widget=DateWidget,
                         label=_("Listing end date"))

    class Meta:
        """
        Attribute-style form customization.
        Override default ModelForm settings.
        """
        model = ListingModel
        # Editable form fields
        fields = ["title", "condition", "starting_price",
                  "start_time", "start_date", "end_time", "end_date", "description"]
        widgets = {"description": Textarea(
            attrs={'cols': 80, 'rows': 10, 'class': 'form-control'})}
        # field help_text is not HTML escaped in autoform
        help_texts = {
            "description": 'Description of item at auction'}

    def __init__(self, *args, **kwargs):
        """
        Statement-style form customization.
        """
        # Modify init arguments (modify fields via __init__)
        # ...

        # Pass all got arguments to the parent class
        super(ModelForm, self).__init__(*args, **kwargs)

        # Post-init (modify fields directly):
        # TODO: move form layout to the template
        # Rendering customization (only visible fields)
        for boundfield in self.visible_fields():
            # Change class atribute of widget of fields
            boundfield.field.widget.attrs['class'] = 'form-control'
            # Format help_text for HTML form
            boundfield.field.help_text = f'<small class="form-text text-muted">{boundfield.field.help_text}</small>'
