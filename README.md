# Maktab Quiz Bot — 1-bosqich

Ro'yxatdan o'tish, profil, reyting, adminlar uchun sinf statistikasi.

## Ishga tushirish (kompyuterda)
1. `pip install -r requirements.txt`
2. `.env.example` faylini `.env` deb nusxalang va ichini to'ldiring.
3. `python main.py`

## Render'da
- GitHub'ga yuklang (`.env` yuklanmaydi, `.gitignore` himoya qiladi).
- Build command: `pip install -r requirements.txt`
- Start command: `python main.py`
- Environment bo'limiga `BOT_TOKEN`, `DATABASE_URL`, `ADMIN_IDS` qo'shing.
- Ma'lumotlar Neon/Supabase bazasida saqlanadi, shuning uchun bot qayta ishga tushsa ham yo'qolmaydi.
- Bepul "Web Service" 15 daqiqa so'rov bo'lmasa uxlab qoladi. Uxlamasligi uchun
  UptimeRobot kabi xizmat bilan bot havolasini har 5 daqiqada tekshirtiring
  yoki pullik "Background Worker" ishlating.

## Admin panel
- `ADMIN_IDS` (.env) dagilar — asosiy adminlar. Ular boshqa adminlarni panelning ichidan qo'sha va o'chira oladi.
- Adminlarga pastda **🛠 Admin panel** tugmasi chiqadi.
- Fanlar ro'yxati `config.py` dagi `SUBJECTS` da, sinf harflari `handlers/start.py` dagi `SECTIONS` da.
- Ko'plab savol yuklash formati (har bir savol bitta qatorda):
  `savol | variant1 | variant2 | variant3 | variant4 | to'g'ri javob (1-4)`
