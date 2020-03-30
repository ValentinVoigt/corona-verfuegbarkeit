from wtforms import ValidationError


def validate_password(form, field):
    if len(field.data) < 8:
        raise ValidationError("Dein Passwort muss mindestens 8 Zeichen lang sein.")
    if not any([c.isdigit() for c in field.data]):
        raise ValidationError("Dein Passwort muss mindestens eine Ziffer beinhalten.")
    if not any([c.isalpha() for c in field.data]):
        raise ValidationError(
            "Dein Passwort muss mindestens einen Buchstaben beinhalten."
        )
