"""Builds an invented demo library for website screenshots (silent audio,
abstract cover art). Run inside the app image (it has ffmpeg and Pillow)."""
import random, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

random.seed(7)
LIB, BOX = Path(sys.argv[1]), Path(sys.argv[2])

SERIES = {
    "Night Signal":        ((20, 24, 70), (255, 94, 98)),
    "The Long Wave":       ((10, 60, 90), (90, 220, 200)),
    "Studio Nine Sessions":((60, 20, 80), (255, 180, 60)),
    "Harbor Lights":       ((15, 30, 50), (120, 170, 255)),
    "Field Notes":         ((30, 70, 40), (210, 240, 120)),
    "Low Tide":            ((250, 120, 90), (255, 220, 150)),
    "Northern Lines":      ((25, 25, 35), (160, 140, 255)),
    "The Quiet Hour":      ((235, 230, 220), (150, 170, 190)),
    "Parallax":            ((5, 5, 15), (0, 200, 255)),
    "Common Ground":       ((120, 40, 30), (255, 160, 110)),
}
TITLES = {
    "Night Signal": ["The Last Train Home", "Static on Channel Four", "A Caller from Nowhere", "The Lighthouse Keeper", "Two A.M. Confessions", "Frequencies", "The Long Drive", "Signals Crossed"],
    "The Long Wave": ["How Radio Learned to Talk", "The Ocean Floor", "Cities After Dark", "The Archive", "Maps We Never Drew", "Under the Ice"],
    "Studio Nine Sessions": ["Live from the Basement", "Acoustic Mornings", "The Piano Room", "Late Set", "Strings Attached", "Encore"],
    "Harbor Lights": ["Fog Warning", "The Captain's Daughter", "Low Water", "A Ship Called Mercy", "Port of Call", "The Last Ferry"],
    "Field Notes": ["What Bees Remember", "The Sound of a Forest", "Weather, Explained", "Small Wonders", "Rivers Run Backwards"],
    "Low Tide": ["Everyone's a Critic", "The Wrong Wedding", "Office Hours", "Vacation, Sort Of", "The Big Move", "Leftovers"],
    "Northern Lines": ["Night Train to Tromsø", "Midnight Sun", "Islands", "The Coast Road", "Snow Country"],
    "The Quiet Hour": ["On Slowing Down", "Letters", "The Art of Doing Nothing", "Morning Pages", "Small Rooms"],
    "Parallax": ["First Contact", "The Second Moon", "Dead Reckoning", "Signal Lost", "Orbit", "Homecoming"],
    "Common Ground": ["A Farmer and a Poet", "The Night Shift", "Neighbors", "Starting Over", "Kitchen Table"],
}

def cover(path, dark, light, seed):
    rnd = random.Random(seed)
    size = 900
    img = Image.new("RGB", (size, size), dark)
    d = ImageDraw.Draw(img)
    for i in range(size):               # gentle diagonal gradient
        t = i / size
        c = tuple(int(dark[k] + (light[k] - dark[k]) * t * 0.55) for k in range(3))
        d.line([(0, i), (size, i)], fill=c)
    glow = Image.new("RGB", (size, size), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    for _ in range(3):
        r = rnd.randint(180, 380)
        x, y = rnd.randint(100, 800), rnd.randint(100, 800)
        g.ellipse([x - r, y - r, x + r, y + r], fill=light)
    glow = glow.filter(ImageFilter.GaussianBlur(110))
    img = Image.blend(img, Image.composite(glow, img, glow.convert("L")), 0.75)
    d = ImageDraw.Draw(img)
    for k in range(rnd.randint(3, 6)):  # a few fine arcs, like waves
        r = 160 + k * 70
        d.arc([size / 2 - r, size * 0.62 - r, size / 2 + r, size * 0.62 + r], 200, 340,
              fill=tuple(min(255, c + 40) for c in light), width=4)
    img.save(path, "JPEG", quality=88)

def tone(path, minutes, tags):
    meta = sum((["-metadata", f"{k}={v}"] for k, v in tags.items()), [])
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i",
                    "anullsrc=r=8000:cl=mono", "-t", str(minutes * 60), "-c:a", "libmp3lame",
                    "-b:a", "8k", *meta, str(path)], check=True)

for n, (series, (dark, light)) in enumerate(SERIES.items()):
    folder = LIB / series
    folder.mkdir(parents=True, exist_ok=True)
    cover(folder / "cover.jpg", dark, light, n)
    year = random.choice([2022, 2023, 2024])
    month = random.randint(1, 4)
    for i, title in enumerate(TITLES[series], 1):
        day = 1 + (i * 7 + n) % 27
        m = month + (i * 7 + n) // 27
        date = f"{year}-{m:02d}-{day:02d}"
        tone(folder / f"{series} - {date} - {title}.mp3", random.choice([24, 28, 29, 42, 45, 52, 58]),
             {"title": title, "artist": series, "album": series, "date": date, "track": str(i)})
    print("made", series)

# A few messy uploads waiting in the inbox (to show the guesses).
for name, minutes in [("Night_Signal_24_05_02_009_Radio_Silence.mp3", 31),
                      ("Parallax - Episode 7 - (Event Horizon).mp3", 44),
                      ("the.long.wave.2024.05.14.the.deep.end.mp3", 49)]:
    tone(BOX / name, minutes, {})
print("inbox ready")
