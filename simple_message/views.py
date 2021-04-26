from django.shortcuts import render
import re

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def simple_message(request):
    items = (
        {"item": item, "is_url": re.match(r"^https?://", item)}
        for item in request.GET.getlist("text_or_audio")
    )
    voice_type = request.GET.get("voice_type")
    return render(
        request, "simple_message.flexml", {"items": items, "voice_type": voice_type}
    )
