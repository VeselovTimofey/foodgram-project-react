from django import forms


def value_is_russia(value):
    """ value must be written in Cyrillic. """
    alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и",
                "й", "к", "л", "м", "н", "о", "п", "р", "с", "т",
                "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь",
                "э", "ю", "я", " ", ".", ",", ";", ":", "-", "_",
                "!", "?"]
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
