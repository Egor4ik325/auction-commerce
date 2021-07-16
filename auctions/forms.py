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
                           label=_("Listing start time"))
    start_date = DateField(required=True, widget=DateWidget, label='')
    end_time = TimeField(required=True, widget=TimeWidget,
                         label=_("Listing end time"))
    end_date = DateField(required=True, widget=DateWidget, label='')

    # Erroneous field styling
    error_css_class = 'is-invalid'

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
        # help_text is not escaped
        help_texts = {
            "description": 'Description of item at auction'}

    def __init__(self, *args, **kwargs):
        """
        Statement-style form customization.
        """
        # Modify init arguments (modify fields via __init__)
        if kwargs is None:
            kwargs = {}
        # POST request: data + [instance] - modify
        if kwargs.get('data'):
            # Merge date and time fields from data
            kwargs['data']._mutable = True
            kwargs['data']['start_datetime'] = f"{kwargs['data']['start_date']} {kwargs['data']['start_time']}"
            kwargs['data']['end_datetime'] = f"{kwargs['data']['end_date']} {kwargs['data']['end_time']}"
            kwargs['data']._mutable = False
        # GET request: [instance] - create based-on model
        elif kwargs.get('instance'):
            if not kwargs.get('initial'):
                kwargs['initial'] = {}
            # Split datetime fields from instance (initials from instance)
            kwargs['initial']['start_date'] = kwargs['instance'].start_datetime.strftime(
                '%Y-%m-%d')
            kwargs['initial']['start_time'] = kwargs['instance'].start_datetime.strftime(
                '%H:%M')
            kwargs['initial']['end_date'] = kwargs['instance'].end_datetime.strftime(
                '%Y-%m-%d')
            kwargs['initial']['end_time'] = kwargs['instance'].end_datetime.strftime(
                '%H:%M')
        # GET request: create new
        else:
            if not kwargs.get('initial'):
                kwargs['initial'] = {}
            # Form fill initials
            kwargs['initial']['start_time'] = round_current_time_string()
            kwargs['initial']['start_date'] = current_date_string()
            kwargs['initial']['end_time'] = round_current_time_string()

        # Pass all arguments to the parent class
        super(ModelForm, self).__init__(*args, **kwargs)

        # Post-init (modify fields directly):
        for boundfield in self.visible_fields():
            # Change <input class="form-control">
            boundfield.field.widget.attrs['class'] = 'form-control'
            # Change <p class="form-text">Help text</p>
            boundfield.field.help_text = f'<small class="form-text text-muted">{boundfield.field.help_text}</small>'
