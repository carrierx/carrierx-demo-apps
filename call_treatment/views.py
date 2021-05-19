from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import re

DIAL_PARAMETERS = ("reason", "text_or_audio")


@csrf_exempt
def call_treatment(request):
    text_or_audio = (
        {
            "value": request.GET.get("text_or_audio"),
            "is_url": re.match(r"^https?://", request.GET.get("text_or_audio")),
        }
        if request.GET.get("text_or_audio")
        else None
    )

    if (
        text_or_audio
        and not text_or_audio["is_url"]
        and any(x in text_or_audio["value"] for x in ["{{to}}", "{{ to }}"])
    ):
        template = " ".join(request.GET.get("To", "10000000000"))
        text_or_audio["value"] = text_or_audio["value"].replace("{{to}}", template)
        text_or_audio["value"] = text_or_audio["value"].replace("{{ to }}", template)

    reason = request.GET.get("reason")
    data = {"reason": reason, "text_or_audio": text_or_audio}
    return render(request, "call_treatment.flexml", data)
