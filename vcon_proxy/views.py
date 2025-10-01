from datetime import datetime
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from openai import OpenAI
import orjson
import requests
import vcon


@csrf_exempt
def route(request):
    dst = request.GET.get("dst", "")
    if dst == '*':
        data = orjson.loads(request.body)
        dst = data.get('To')

    return render(request, "vcon_start.flexml", {
        "dst": dst,
        "conserver": request.GET.get("conserver", ""),
        "conserver_api_token": request.GET.get("conserver_api_token", ""),
        "transcribe": request.GET.get("transcribe", ""),
        "transcribe_api_token": request.GET.get("transcribe_api_token", ""),
    })

@csrf_exempt
def end(request):
    data = orjson.loads(request.body)

    timestamp = datetime.utcfromtimestamp(float(data.get('StartTime', 0))).isoformat() + 'Z'
    from_ = strip_uri_param(data.get('OriginalFrom'))
    to = strip_uri_param(data.get('OriginalTo'))
    recording = data.get('RecordingUrl')
    print(f"data:{data}")

    transcript = ''
    if data.get('Storage_transcribe', '') == 'true':
        transcript = transcribe(data.get('Storage_transcribe_api_token'), recording)

    vc = vcon.Vcon.build_new()
    vc.add_party(vcon.party.Party(tel=from_))
    vc.add_party(vcon.party.Party(tel=to))
    vc.add_dialog(vcon.dialog.Dialog(
        type='recording',
        start=timestamp,
        parties=[0, 1],
        originator=0,
        mimetype='audio/mp3',
        url=recording,
    ))
    if transcript:
        vc.add_analysis(
            type='transcript',
            dialog=0,
            vendor='openai',
            body=transcript,
        )
    vcon_payload = vc.dumps()

    r = requests.post(
            data.get("Storage_conserver"),
            headers={
                "Content-type": "application/json",
                "x-conserver-api-token": data.get('Storage_conserver_api_token')
            },
            data=vcon_payload
    )
    print(r.status_code, r.content)

    return render(request, "vcon_end.flexml", {})

def transcribe(api_key, url):
    openai_client = OpenAI(api_key=api_key)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    audio_bytes = BytesIO(response.content)
    audio_bytes.name = "audio.mp3"
    transcription = openai_client.audio.transcriptions.create(model="whisper-1", file=audio_bytes)
    return transcription.text

def strip_uri_param(uri):
    if ';' in uri:
        return uri.split(';')[0]
    else:
        return uri
