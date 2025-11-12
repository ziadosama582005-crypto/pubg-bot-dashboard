import requests

def get_pubg_name_from_midas(player_id: str):
    """يجلب الاسم الحقيقي من موقع ميداس أو Tencent الرسمي"""
    
    # الروابط الثلاثة (رئيسي + احتياطي + Tencent)
    urls = [
        "https://www.midasbuy.com/ot/api/v1/pubgm/checkPlayer",  # الرئيسي
        "https://corsproxy.io/?" + "https://www.midasbuy.com/ot/api/v1/pubgm/checkPlayer",  # عبر بروكسي
        f"https://www.pubgmobile.com/en-US/api/playerInfo?playerId={player_id}"  # Tencent الرسمي
    ]

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

    for url in urls:
        try:
            # إذا كان الرابط الأخير (Tencent) نرسل GET وليس POST
            if "pubgmobile.com" in url:
                response = requests.get(url, headers=headers, timeout=10)
            else:
                response = requests.post(url, json=payload, headers=headers, timeout=10)

            # ✅ حالة النجاح من Tencent API
            if "pubgmobile.com" in url and response.status_code == 200:
                data = response.json()
                if "data" in data and "name" in data["data"]:
                    return {
                        "success": True,
                        "name": data["data"]["name"],
                        "id": data["data"]["id"],
                        "source": "Tencent Official"
                    }

            # ✅ حالة النجاح من Midas API
            elif response.status_code == 200:
                data = response.json()
                if data.get("code") == "SUCCESS":
                    return {
                        "success": True,
                        "name": data["data"]["roleName"],
                        "id": data["data"]["roleId"],
                        "source": url
                    }

        except Exception as e:
            continue

    # إذا فشل الجميع
    return {
        "success": False,
        "error": "⚠️ تعذر الوصول إلى بيانات اللاعب حالياً — أعد المحاولة لاحقاً."
    }
