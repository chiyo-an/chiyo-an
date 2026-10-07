from svg import BLUE, GRAY, reveal, save, text

NAME = "CHIYO"
LOCATION = "Incheon, KR"
ROLE = "Frontend Developer"
parts = reveal(text(28, 82, NAME, 60, extra='font-weight="700" letter-spacing="-3"'), .15)
parts += reveal(text(30, 118, ROLE, 20), .3)
for i, (label, value) in enumerate([
    ("Based in", LOCATION),
    ("Focus", "Frontend / UI Engineering"),
    ("Stack", "Next.js / React / TypeScript"),
    ("Building", "Products & Web Experiences"),
]):
    parts += reveal(text(30, 166+i*26, label, 12, GRAY) + text(132, 166+i*26, value, 12), .45+i*.12)
parts += reveal(text(30, 290, "Founder · Pixel Hive Studio", 11, GRAY), 1)
save("info-card.svg", 550, 310, "CHIYO, Frontend Developer. Incheon, KR. Frontend and UI Engineering. Founder of Pixel Hive Studio.", parts)
save("info-card-mobile.svg", 440, 310, "CHIYO, Frontend Developer in Incheon. Founder of Pixel Hive Studio.", parts)
