import json
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_email

RECORD_PARAMETERS = (
    "action",
    "callbackUrl",
    "containerSid",
    "direction",
    "errorAction",
    "errorMethod",
    "fileFormat",
    "fileMode",
    "fileSid",
    "finishOnKey",
    "integerKey1",
    "integerKey2",
    "maxLength",
    "method",
    "playBeep",
    "timeout",
    "trim",
    "recordSession",
    "stringKey1",
    "stringKey2",
)


@csrf_exempt
def start(request):
    attrs = {
        key: request.GET.get(key)
        for key, value in request.GET.items()
        if key in RECORD_PARAMETERS and value
    }
    data = {
        "record_attrs": attrs,
        "greeting_message": {
            "content": request.GET.get("greeting_message"),
            "is_url": re.match(r"^https?://", request.GET.get("greeting_message")),
        },
        "goodbye_message": request.GET.get("goodbye_message"),
        "voice_type": request.GET.get("voice_type"),
        "file_format": request.GET.get("fileFormat"),
        "email": request.GET.get("email"),
        "email_subject": request.GET.get("email_subject"),
    }
    return render(request, "voicemail.flexml", data)


@csrf_exempt
def say_goodbye(request):
    goodbye_properties = json.loads(request.body.decode("utf-8"))
    data = {
        "message": {
            "content": goodbye_properties.get("message"),
            "is_url": re.match(r"^https?://", goodbye_properties.get("message")),
        },
        "voice_type": goodbye_properties.get("voice_type"),
    }
    return render(request, "voicemail_goodbye.flexml", data)


@csrf_exempt
def send(request):
    recording_properties = json.loads(request.body.decode("utf-8"))
    email_address = recording_properties.get("Storage_email")
    email_subject = recording_properties.get("Storage_email_subject")

    if email_address and recording_properties:
        send_email(email_subject, email_address, recording_properties)
    return HttpResponse(status=204)
