from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

DIAL_PARAMETERS = ("action",
                   "method",
                   "timeout",
                   "timeLimit",
                   "hangupOnStar")


@csrf_exempt
def forward(request):
    attrs = {key: request.GET.get(key)
             for key, value
             in request.GET.items()
             if key in DIAL_PARAMETERS and value}
    data = {"attrs": attrs, "phone_number": request.GET.get("phone_number")}
    return render(request, "forward.flexml", data)
