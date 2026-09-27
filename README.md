# osint-cli

Linux terminal uchun oddiy OSINT vositasi (ta'lim loyihasi).

## Imkoniyatlari

- **`ip`** — sizning o'zingizning public IP manzilingiz, davlat, shahar va ISP ma'lumotini ko'rsatadi (ipapi.co API orqali).
- **`username`** — berilgan username 15 ta mashhur platformada (GitHub, Instagram, Telegram, YouTube va h.k.) ochiq ravishda mavjudligini tekshiradi.
- **`phone`** — telefon raqamining davlati va operatorini ko'rsatadi (Google'ning `libphonenumber` kutubxonasi asosida, offline ma'lumotlar bazasidan — hech qanday joylashuvni kuzatmaydi).

## O'rnatish

```bash
git clone <sizning-repo-manzilingiz>
cd osint-cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Foydalanish

```bash
# O'z IP manzilingizni ko'rish
python3 main.py ip

# Username qidirish
python3 main.py username john_doe

# Telefon raqami haqida ma'lumot
python3 main.py phone +998901234567
```

Global buyruq sifatida ishlatish uchun (ixtiyoriy):

```bash
chmod +x main.py
sudo ln -s "$(pwd)/main.py" /usr/local/bin/osint-cli
osint-cli ip
```

## GitHub'ga joylash

```bash
cd osint-cli
git init
git add .
git commit -m "osint-cli: birinchi versiya"
git branch -M main
git remote add origin https://github.com/<username>/osint-cli.git
git push -u origin main
```

## Muhim eslatma

Bu vosita faqat **ochiq (public)** ma'lumotlar bilan ishlaydi:
- `phone` buyrug'i raqamni jismoniy kuzatmaydi — faqat davlat kodi va operator nomini offline bazadan aniqlaydi.
- `username` buyrug'i faqat profil sahifasi mavjudligini (HTTP status kod orqali) tekshiradi, hech qanday shaxsiy ma'lumotni yig'maydi.
- `ip` buyrug'i faqat dasturni ishga tushirgan kompyuterning o'z IP manzilini ko'rsatadi.

Vositani boshqa odamlarning roziligisiz kuzatish yoki maxfiyligini buzish uchun ishlatmang — bu ta'lim maqsadidagi loyiha.

## Litsenziya

MIT
