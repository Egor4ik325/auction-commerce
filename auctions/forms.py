from django.contrib.auth import forms, get_user_model
from django.forms import ModelForm, TimeField, DateField, TimeInput, DateInput, DateTimeInput, Textarea, HiddenInput
from django.utils.translation import ugettext_lazy as _
from .models import ListingModel

from .util_datetime import current_datetime, current_date_string


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
    """HTML <input type="time"> form widget."""
    input_type = 'time'


class DateWidget(DateInput):
    """HTML <input type="date"> form widget."""
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        # Always override widget format
        kwargs['format'] = '%Y-%m-%d'
        super().__init__(*args, **kwargs)


def round_current_time_string():
    """Custom hour rounding time str formatting."""
    cur_dt = current_datetime()
    cur_time = cur_dt.strftime('%H:00')
    return cur_time


class ListingForm(ModelForm):
    """
    Listing form, used for:
    1. HTML form rendering;
    2. client-side <form> validation (attributes);
    3. server-side ListingForm validation;
    4. cleanded Model instance saving.
    """
    # Split model start_datetime, end_datetime into multiple fields
    start_time = TimeField(required=True, widget=TimeWidget,
                           label=_("Listing start time"),
                           initial=round_current_time_string())
    start_date = DateField(required=True, widget=DateWidget,
                           label=_("Listing start date"),
                           initial=current_date_string())
    end_time = TimeField(required=True, widget=TimeWidget,
                         label=_("Listing end time"))
    end_date = DateField(required=True, widget=DateWidget,
                         label=_("Listing end date"))

    # self._meta options
    class Meta:
        """
        Attribute-style form customization.
        Override default ModelForm settings.
        """
        model = ListingModel
        # Editable form fields
        fields = ["title", "condition", "starting_price",
                  "start_time", "start_date", "end_time", "end_date", "description", "start_datetime", "end_datetime"]
        widgets = {"description": Textarea(
            attrs={'cols': 80, 'rows': 10, 'class': 'form-control'}),
            # Make fields passed to model instance
            'start_datetime': HiddenInput, 'end_datetime': HiddenInput}
        # field help_text is not HTML escaped in autoform
        help_texts = {
            "description": 'Description of item at auction'}

    def __init__(self, *args, **kwargs):
        """
        Statement-style form customization.
        """
        # Modify init arguments (modify fields via __init__)
        if kwargs:
            # Assign date and time to model datetime field
            if kwargs['data']:
                kwargs['data']._mutable = True
                # Modify django.http.request.QueryDict argument or self.data directly
                kwargs['data']['start_datetime'] = f"{kwargs['data']['start_date']} {kwargs['data']['start_time']}"
                kwargs['data']['end_datetime'] = f"{kwargs['data']['end_date']} {kwargs['data']['end_time']}"
                kwargs['data']._mutable = False

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
