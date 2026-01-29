import base64, requests
from datetime import datetime, timezone

BASE_URL = "https://api.planningcenteronline.com/services/v2"
TARGET_SERVICE_TYPE_NAME = "Celebration Service"

def auth_header(app_id, secret):
    token = base64.b64encode(f"{app_id}:{secret}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

def get_service_type_id(app_id, secret):
    r = requests.get(f"{BASE_URL}/service_types", headers=auth_header(app_id, secret))
    r.raise_for_status()
    for svc in r.json()["data"]:
        if svc["attributes"]["name"].lower() == TARGET_SERVICE_TYPE_NAME.lower():
            return svc["id"]
    raise Exception("Celebration Service not found")

def find_plan_by_date(app_id, secret, svc_id, target_date):
    url = f"{BASE_URL}/service_types/{svc_id}/plans"
    headers = auth_header(app_id, secret)

    while url:
        r = requests.get(url, headers=headers, params={"order": "sort_date"})
        r.raise_for_status()
        data = r.json()

        for plan in data["data"]:
            sd = plan["attributes"]["sort_date"]
            if not sd: continue
            d = datetime.fromisoformat(sd.replace("Z","+00:00")).date().isoformat()
            if d == target_date:
                return plan["id"]

        url = data["links"].get("next")

    return None

def find_next_scheduled_plan(app_id, secret, svc_id, person_id):
    r = requests.get(
        f"{BASE_URL}/service_types/{svc_id}/plans",
        headers=auth_header(app_id, secret),
        params={"order": "sort_date"}
    )
    r.raise_for_status()

    today = datetime.now(timezone.utc).date()

    for plan in r.json()["data"]:
        sd = plan["attributes"]["sort_date"]
        if not sd: continue
        if datetime.fromisoformat(sd.replace("Z","+00:00")).date() < today:
            continue

        pid = plan["id"]
        team = requests.get(
            f"{BASE_URL}/service_types/{svc_id}/plans/{pid}/team_members",
            headers=auth_header(app_id, secret)
        ).json()

        for m in team["data"]:
            if m["relationships"]["person"]["data"]["id"] == person_id:
                return pid

    return None

def fetch_plan_songs_with_meta(app_id, secret, svc_id, plan_id):
    r = requests.get(
        f"{BASE_URL}/service_types/{svc_id}/plans/{plan_id}/items",
        headers=auth_header(app_id, secret),
        params={"include":"arrangement,key,song"}
    )
    r.raise_for_status()

    payload = r.json()
    included = {f'{i["type"]}:{i["id"]}':i for i in payload.get("included",[])}

    songs = []
    for item in payload["data"]:
        if item["attributes"]["item_type"].lower() != "song":
            continue

        arr = included.get(f'arrangements:{item["relationships"]["arrangement"]["data"]["id"]}',{})
        key = included.get(f'keys:{item["relationships"]["key"]["data"]["id"]}',{})

        songs.append({
            "title": item["attributes"]["title"],
            "bpm": arr.get("attributes",{}).get("bpm"),
            "meter": arr.get("attributes",{}).get("meter"),
            "key": key.get("attributes",{}).get("name")
        })

    return songs
