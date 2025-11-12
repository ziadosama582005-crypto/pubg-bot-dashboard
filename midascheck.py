import requests

def get_pubg_name_from_midas(player_id: str):
    """يجلب الاسم الحقيقي من موقع ميداس الرسمي أو من مصدر احتياطي"""
    
    # قائمة الروابط الممكنة (الأصلي + الاحتياطي)
    urls = [
        "https://corsproxy.io/?" + "https://www.midasbuy.com/ot/api/v1/pubgm/checkPlayer",
        "https://corsproxy.io/?" + "https://www.midasbuy.com/ot/api/v1/player/checkPlayer"
    ]

    # نفس البيانات المطلوبة في كل API
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

    # نحاول مع كل رابط بالتتابع
    for url in urls:
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == "SUCCESS":
                    return {
                        "success": True,
                        "name": data["data"]["roleName"],
                        "id": data["data"]["roleId"],
                        "source": url
                    }
                else:
                    # إذا الرد فشل من السيرفر، نجرب الرابط التالي
                    continue
            else:
                # إذا كود HTTP غير 200، نجرب الرابط التالي
                continue

        except Exception as e:
            # إذا حصلت مشكلة بالاتصال ننتقل للرابط التالي
            continue

    # إذا فشل جميع الروابط
    return {
        "success": False,
        "error": "تعذر الوصول إلى بيانات اللاعب حالياً — أعد المحاولة لاحقاً.",
    }
