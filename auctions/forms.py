from django.contrib.auth import forms, get_user_model
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber


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
