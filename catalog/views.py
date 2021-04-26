from django.shortcuts import render
from django.http import Http404
from . import forms

FLEXIAPP_NAMES = (
    "simple_message",
    "simple_menu",
    "concurrent_calls",
    "voicemail",
    "forward",
    "call_treatment",
)


def snake_to_upper_camel_case(input_string: str) -> str:
    return "".join(str.capitalize(token) for token in input_string.split("_"))


def snake_to_natural_capitalized(input_string: str) -> str:
    return " ".join(str.capitalize(token) for token in input_string.split("_"))


def main(request):
    return render(request, "home.html")


def detail(request, flexiapp_name):
    if flexiapp_name in FLEXIAPP_NAMES:
        return render(
            request,
            f"{flexiapp_name}.html",
            {
                "flexiapp_name": flexiapp_name,
                "natural_flexiapp_name": snake_to_natural_capitalized(flexiapp_name),
                "form": getattr(
                    forms, snake_to_upper_camel_case(flexiapp_name) + "Form"
                )(),
            },
        )
    raise Http404("The page does not exist")
