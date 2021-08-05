# Form and fields

form.fields: (BoundField)
    1. form.visible_fields (BoundField)
        - not field.is_hidden
    2. form.hidden_fields (BoundField)
        - field.is_hidden

form.__iter__ = form.fields
form.field_name = FloatField (UnBoundField)

BoundField:
- data
- fields
- ...

form.errors:
    1. form.add_error (form.has_error)
    2. field.errors
    3. form.non_field_errors
