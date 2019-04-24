from django.core.exceptions import ValidationError

def get_key(enum_class, key_value):
    return next(name for name, value in vars(enum_class).items() if value == key_value)

def validate_image_size(value):
    filesize= value.size
    if filesize > 1048576:
        raise ValidationError("The maximum image size that can be uploaded is 1MB")
    else:
        return value
