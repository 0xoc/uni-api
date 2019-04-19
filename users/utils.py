
def get_key(enum_class, key_value):
    return next(name for name, value in vars(enum_class).items() if value == key_value)