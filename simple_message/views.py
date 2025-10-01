import json
import re
import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def simple_message(request):
    items = ({"item": item, "is_url": re.match(r"^https?://", item)}
             for item
             in request.GET.getlist("text_or_audio"))
    voice_type = request.GET.get("voice_type", "")
    notify_on_key = request.GET.get("notify_on_key", "")

    return render(request, "simple_message.flexml", {
        "items": items,
        "voice_type": voice_type,
        "notify_on_key": notify_on_key,
    })


@csrf_exempt
def digits(request):
    voice_type = request.GET.get("voice_type", "")
    notify_on_key = request.GET.get("notify_on_key", "")
    notify_text_or_audio = request.GET.get("notify_text_or_audio", "")
    notify_email = request.GET.get("notify_email", "")

    request_data = json.loads(request.body.decode())
    if len(request_data.get('Digits')) == 0:
        return render(request, "notify_hangup.flexml")

    sent = send_mail(
        "Simple Message Notification",
        f"Simple Message Notification:\n{request_data.get('To')}\n{request_data.get('Digits')}",
        settings.DEFAULT_FROM_EMAIL,
        [notify_email],
        fail_silently=True
    )
    if not sent:
        return render(request, "notify_failure.flexml")

    notify_item = {
        "item": notify_text_or_audio,
        "is_url": re.match(r"^https?://", notify_text_or_audio)
    }
    return render(request, "notify_success.flexml", {
        "message": notify_item,
        "voice_type": voice_type,
    })