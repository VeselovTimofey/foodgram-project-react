from django import forms


def value_is_russia(value):
    """ value must be written in Cyrillic. """
    alphabet = ["ё", " ", ".", ",", ";", ":", "-", "_", "!", "?"]
    a = ord('а')
    [alphabet.append(chr(letter)) for letter in range(a, a + 32)]
    value = value.lower()
    for letter in value:
        if letter not in alphabet:
            raise forms.ValidationError(
                "Название должно быть написано кириллицей.",
                params={"value": value},
            )


def value_must_not_be_null(value):
    if value == 0:
        raise forms.ValidationError(
            "Значение не может быть нулём.",
            params={"value": value},
        )
