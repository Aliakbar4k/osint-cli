#!/usr/bin/env python3
"""
osint-cli — ta'lim maqsadidagi terminal vositasi.

Uch funksiya:
  ip       - foydalanuvchining o'z (public) IP manzili va joylashuvini ko'rsatadi
  username - berilgan username ochiq (public) platformalarda mavjudligini tekshiradi
  phone    - telefon raqamining davlati va operatorini aniqlaydi (libphonenumber orqali)

Faqat ochiq/public ma'lumotlar va rasmiy API'lar bilan ishlaydi.
Boshqa odamlarning maxfiy ma'lumotini kuzatish uchun mo'ljallanmagan.
"""

import argparse
import sys

import requests
import phonenumbers
from phonenumbers import geocoder, carrier

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) osint-cli/1.0 (educational)"

GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"

_BANNER_FONT = {
    "C": [" ### ", "#   #", "#    ", "#    ", "#   #", " ### "],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "B": ["#### ", "#   #", "#### ", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#### ", "#    ", "#    ", "#####"],
    "R": ["#### ", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
}


def print_banner() -> None:
    """Ishga tushganda katta CYBERY yozuvini chiqaradi."""
    text = "CYBERY"
    rows = ["  ".join(_BANNER_FONT[ch][i] for ch in text) for i in range(6)]
    banner = "\n".join(rows)
    print(f"{GREEN}{BOLD}{banner}{RESET}")
    print(f"{GREEN}         OSINT terminal vositasi — ta'lim maqsadida{RESET}\n")

USERNAME_SITES = {
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Twitter/X": "https://x.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Telegram": "https://t.me/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Facebook": "https://www.facebook.com/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Medium": "https://medium.com/@{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
}


def get_my_ip() -> None:
    """Foydalanuvchining o'z public IP manzili va geo-ma'lumotini chiqaradi."""
    try:
        r = requests.get("https://ipapi.co/json/", timeout=6)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        print(f"Xatolik: IP ma'lumotini olib bo'lmadi ({e})", file=sys.stderr)
        sys.exit(1)

    print(f"IP manzil : {data.get('ip', 'nomaʼlum')}")
    print(f"Davlat    : {data.get('country_name', 'nomaʼlum')}")
    print(f"Shahar    : {data.get('city', 'nomaʼlum')}")
    print(f"Region    : {data.get('region', 'nomaʼlum')}")
    print(f"ISP       : {data.get('org', 'nomaʼlum')}")
    print(f"ASN       : {data.get('asn', 'nomaʼlum')}")
    print(f"Timezone  : {data.get('timezone', 'nomaʼlum')}")


def search_username(username: str) -> None:
    """Berilgan username ochiq platformalarda mavjudligini tekshiradi (public OSINT)."""
    print(f"'{username}' uchun {len(USERNAME_SITES)} ta platformada qidirilmoqda...\n")
    headers = {"User-Agent": USER_AGENT}
    found = []

    for site, url_tpl in USERNAME_SITES.items():
        url = url_tpl.format(username)
        try:
            r = requests.get(url, headers=headers, timeout=6, allow_redirects=True)
            exists = r.status_code == 200
        except requests.RequestException:
            exists = None

        if exists is True:
            print(f"[+] {site:<12} -> topildi     {url}")
            found.append((site, url))
        elif exists is False:
            print(f"[-] {site:<12} -> topilmadi")
        else:
            print(f"[?] {site:<12} -> tekshirib bo'lmadi (tarmoq xatosi)")

    print(f"\nJami topilgan: {len(found)}/{len(USERNAME_SITES)}")
    print("Eslatma: ba'zi saytlar har doim 200-kod qaytarishi mumkin (JS render),")
    print("shuning uchun natija 100% aniq emas — qo'lda tekshirib ko'ring.")


def check_phone(number: str) -> None:
    """Telefon raqamining davlati va operatorini ko'rsatadi (kuzatuv emas)."""
    try:
        parsed = phonenumbers.parse(number, None)
    except phonenumbers.NumberParseException as e:
        print(f"Xatolik: raqam formati noto'g'ri ({e})", file=sys.stderr)
        print("Xalqaro formatda kiriting, masalan: +998901234567", file=sys.stderr)
        sys.exit(1)

    valid = phonenumbers.is_valid_number(parsed)
    location = geocoder.description_for_number(parsed, "uz") or geocoder.description_for_number(parsed, "en")
    operator = carrier.name_for_number(parsed, "en")
    region_code = phonenumbers.region_code_for_number(parsed)
    formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    print(f"Raqam        : {formatted}")
    print(f"Yaroqli      : {'Ha' if valid else 'Yo\u02bbq'}")
    print(f"Davlat kodi  : {region_code or 'nomaʼlum'}")
    print(f"Joylashuv    : {location or 'nomaʼlum'}")
    print(f"Operator     : {operator or 'nomaʼlum (yoki portlangan raqam bo\u02bblishi mumkin)'}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="osint-cli",
        description="Ta'lim maqsadidagi OSINT terminal vositasi: IP, username, telefon.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("ip", help="O'zingizning public IP manzilingiz va joylashuvni ko'rsatadi")

    p_user = sub.add_parser("username", help="Username orqali ochiq profillarni qidiradi")
    p_user.add_argument("username", help="Qidiriladigan username")

    p_phone = sub.add_parser("phone", help="Telefon raqamining davlati va operatorini ko'rsatadi")
    p_phone.add_argument("number", help="Xalqaro formatda, masalan +998901234567")

    args = parser.parse_args()

    print_banner()

    if args.command == "ip":
        get_my_ip()
    elif args.command == "username":
        search_username(args.username)
    elif args.command == "phone":
        check_phone(args.number)


if __name__ == "__main__":
    main()
