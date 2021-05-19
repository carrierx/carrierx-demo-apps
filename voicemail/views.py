from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_email
import json

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
        "greeting_message": request.GET.get("greeting_message"),
        "goodbye_message": request.GET.get("goodbye_message"),
        "voice_type": request.GET.get("voice_type"),
        "email": request.GET.get("email"),
    }
    return render(request, "voicemail.flexml", data)


@csrf_exempt
def say_goodbye(request):
    data = {
        "message": request.GET.get("message"),
        "voice_type": request.GET.get("voice_type"),
    }
    return render(request, "voicemail_goodbye.flexml", data)


@csrf_exempt
def send(request):
    email_address = request.GET.get("email")
    recording_properties = json.loads(request.body.decode("utf-8"))
    if email_address and recording_properties:
        send_email("voicemail", email_address, recording_properties["RecordingUrl"])
    return HttpResponse(status=204)
