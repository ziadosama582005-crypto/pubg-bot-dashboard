import requests

def get_pubg_name_from_midas(player_id: str):
    """يجلب الاسم الحقيقي من موقع ميداس الرسمي"""
    url = "https://www.midasbuy.com/ot/api/v1/pubgm/checkPlayer"
    payload = {
        "appId": "1450015065",
        "playerId": str(player_id),
        "serverId": "null",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.midasbuy.com",
        "Referer": "https://www.midasbuy.com/",
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "SUCCESS":
                return {
                    "success": True,
                    "name": data["data"]["roleName"],
                    "id": data["data"]["roleId"],
                }
            else:
                return {"success": False, "error": data.get("msg", "Unknown error")}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
