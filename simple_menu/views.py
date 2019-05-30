from django.shortcuts import render
from urllib import parse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def start(request):
    data = {"options": parse.urlencode({key[-1]: url for key, url in request.GET.items() if key.startswith("url_")}),
            "instructions": request.GET.get("instructions")}
    return render(request, "simple_menu.flexml", data)


@csrf_exempt
def redirect(request):
    options = {key[-1]: url for key, url in request.GET.items() if key.startswith("url_")}
    response = json.loads(request.body, encoding="utf-8")
    return render(request, "redirect.flexml", {"url": options[response["Digits"][0]]})
