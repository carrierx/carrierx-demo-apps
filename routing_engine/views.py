import re
import time

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import orjson
import httpx


@csrf_exempt
def route(request):
    start_time = time.time()

    api_token = request.GET.get('api_token')
    lcr = request.GET.get('lcr') == 'true'
    dst = request.GET.get('dst')
    max_pstn_rate = request.GET.get('max_pstn_rate', request.GET.get('mpr'))
    max_rate = request.GET.get('max_rate', request.GET.get('mr'))
    min_margin_percent = request.GET.get('min_margin_percent', request.GET.get('mmp'))
    min_margin_rate = request.GET.get('min_margin_rate', request.GET.get('mmr'))
    trr_socn = {}
    for s in request.GET.get('trr_socn', '').split(','):
        m = re.match(r'([^:]+):(.*)', s)
        if m:
            trr_socn[m[1]] = set(m[2].split(':'))
    last_tr = request.GET.get('last_tr', '').replace(',', '|')
    pin_tr = request.GET.get('pin_tr', '').replace(',', '|')
    weight_tr = []
    for w in request.GET.get('weight_tr', '').split(','):
        m = re.match(r'([^:]+):(-?\d*):(-?(?:\d+\.)?\d+)$', w)
        if m:
            weight_tr.append((m[1], m[2], float(m[3]),))

    body = orjson.loads(request.body)
    partner_sid = body['call_detail']['PartnerSid']
    direction = body['call_detail']['Direction']
    src = body['call_detail']['EndpointSidSrc'] 
    if not dst:
        dst = body['call_detail']['TrunkGroupSidDst']
    to = body['To'][0]['user']
    from_ = body['From'][0]['user']
    call_id = body.get('Call-ID', [])[0]
    print(f"{to}/{call_id} - {partner_sid} {direction} - {from_} @ {src} => {dst}")

    r = httpx.get(
        'http://ow-api-carrierx.int/core/v2/system/rating/lcr',
        headers={
            "Authorization": f"Bearer {api_token}",
        },
        params={
            "partner_sid": partner_sid,
            "endpoint_sid": src,
            "trunk_group_sid_dst": dst,
            "to": to,
            "from": [from_],
        }
    )
    print(f"{to}/{call_id} - api:{r.elapsed} - {r.text}")

    resp_json = orjson.loads(r.text)
    pstn_rate = resp_json.get('pstn', {}).get('rate', 0)
    if max_pstn_rate:
        if pstn_rate <= max_pstn_rate:
            print(f"{to}/{call_id} - pstn rate {pstn_rate} <= {max_pstn_rate}, continue checks")
        else:
            # if pstn rate too expensive we can reject call immediately
            print(f"{to}/{call_id} - elapsed:{time.time() - start_time} - pstn rate {pstn_rate} > {max_pstn_rate}, rejecting call")
            return HttpResponse(orjson.dumps(
                [
                    {
                        "action": "reject",
                        "operands": ["unavailable", "lcr"]
                    }
                ]
            ))
    src_rate = resp_json['lcr_src']
    dst_rates = resp_json['lcr_dst']
    from_ocn = set([o['ocn'] for o in resp_json.get('from', {}).values()])

    # check if we have any rates at all
    if not dst_rates:
        print(f"{to}/{call_id} - elapsed:{time.time() - start_time} - incomplete routing data, return noop")
        return HttpResponse(orjson.dumps([]))

    # reject any drains over our threshold
    drain_rate = {}
    for tr in dst_rates:
        # source ocn trunk filters
        socn_filtered = False
        for trr in trr_socn.keys():
            if tr['trunk_sid'].startswith(trr):
                if not from_ocn & trr_socn[trr]:
                    print(f"{to}/{call_id} - {from_ocn} not in {trr_socn[trr]} - removing trunk {tr['trunk_sid']}")
                    socn_filtered = True
                    continue
                else:
                    print(f"{to}/{call_id} - {from_ocn} in {trr_socn[trr]} - allowing trunk {tr['trunk_sid']}")
        if socn_filtered:
            continue

        # max rate protection
        buy_rate = float(tr['rate'])
        if max_rate is not None and buy_rate > float(max_rate):
            print(f"{to}/{call_id} - excluding {tr['trunk_sid']} due to max rate {buy_rate} > {float(max_rate)}")
            continue

        # margin protection
        if src_rate is not None:
            sell_rate = float(src_rate['rate'])
            margin_rate = sell_rate - buy_rate
            if buy_rate > 0:
                margin_percent = margin_rate / buy_rate
            else:
                margin_percent = 1.00
            if min_margin_rate is not None and margin_rate < float(min_margin_rate):
                print(f"{to}/{call_id} - excluding {tr['trunk_sid']} due to margin rate {margin_rate} < {min_margin_rate}")
                continue
            if min_margin_percent is not None and margin_percent < float(min_margin_percent):
                print(f"{to}/{call_id} - excluding {tr['trunk_sid']} due to margin percent {margin_percent} < {min_margin_percent}")
                continue

        # weight applies after margin protection and affects sorting only
        for w in weight_tr:
            if tr['trunk_sid'].startswith(w[0]) and to.startswith(w[1]):
                print(f"{to}/{call_id} - adjusting sort weight on tr {w[0]} for prefix {w[1]} to {buy_rate} => {buy_rate + w[2]}")
                buy_rate += w[2]

        drain_rate[tr['trunk_sid']] = float(buy_rate)

    if not drain_rate:
        # if no eligible trunks, reject must be used to send proper cause code
        print(f"{to}/{call_id} - elapsed:{time.time() - start_time} - no eligible drains, rejecting call")
        return HttpResponse(orjson.dumps(
            [
                {
                    "action": "reject",
                    "operands": ["unavailable", "lcr"]
                }
            ]
        ))
    elif direction == 'inbound':
        # return sorted list of eligible trunks
        drain_list = [x[0] for x in sorted(drain_rate.items(), key=lambda kv: kv[1])]
        if last_tr:
            drain_list = sorted(drain_list, key=lambda x: bool(re.search(f'^({last_tr})', x)))
        if pin_tr:
            drain_list = sorted(drain_list, key=lambda x: not bool(re.search(f'^({pin_tr})', x)))
        
        print(f"{to}/{call_id} - elapsed:{time.time() - start_time} - lcr ordering as {drain_list}: {drain_rate}")
        return HttpResponse(orjson.dumps(
            [
                {
                    "action": "set_trunk_list",
                    "operands": drain_list
                }
            ]
        ))
    else:
        # if handler on outbound trunk, and not all drains removed, we cannot take any action
        print(f"{to}/{call_id} - elapsed:{time.time() - start_time} - possible drains on outbound trunk, return noop")
        return HttpResponse(orjson.dumps([]))
