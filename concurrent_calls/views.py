from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

DIAL_PARAMETERS = ("action", "method", "timeout", "timeLimit", "hangupOnStar")


@csrf_exempt
def concurrent_calls(request):
    attrs = {
        key: request.GET.get(key)
        for key, value in request.GET.items()
        if key in DIAL_PARAMETERS and value
    }
    data = {"dial_attrs": attrs, "phone_numbers": request.GET.getlist("phone_number")}
    return render(request, "concurrent_calls.flexml", data)
