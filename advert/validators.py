from django.core.exceptions import ValidationError


def bool_valid(value: bool):
    if value:
        raise ValidationError(
            "Значение не может быть True при создании",
            params={'value': value}
        )