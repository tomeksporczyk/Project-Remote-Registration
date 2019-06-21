import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def is_user_unique(value):
    if User.objects.filter(username=value):
        raise ValidationError('Ten login jest już zajęty')


def is_password_strong(value):
    length = len(value) >= 7
    has_uppercase = any([char.isupper() for char in value])
    has_lowercase = any([char.islower() for char in value])
    has_number = any([char.isnumeric() for char in value])
    has_special = any(re.findall('[^a-z, ^A-Z, ^0-9]', value))
    if not(length and has_uppercase and has_lowercase and has_number and has_special):
        raise ValidationError('Hasło musi mieć minimum siedem znaków i zawierać minimum jedną wielką literę, małą literę, cyfrę oraz znak specjalny')
