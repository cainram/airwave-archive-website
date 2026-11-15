"""Ten distinct abstract covers for the invented demo series, each a nod to
old-time radio. Drawn at double size, then scaled down for smooth edges."""
import math, random, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
N = 1800          # drawing size; saved at 900

def gradient(top, bottom, size=N):
    img = Image.new("RGB", (size, size), top)
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / (size - 1)
        d.line([(0, y), (size, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img

def glow(img, xy, r, colour, blur, strength=0.8):
    layer = Image.new("RGB", img.size, (0, 0, 0))
    ImageDraw.Draw(layer).ellipse([xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r], fill=colour)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    mask = layer.convert("L").point(lambda v: int(v * strength))
    return Image.composite(layer, img, mask)

def save(img, name):
    img.resize((900, 900), Image.LANCZOS).save(OUT / f"{name}.jpg", "JPEG", quality=90)

# 1. Night Signal: a glowing tuning dial with a red needle.
img = gradient((14, 16, 38), (40, 22, 52))
img = glow(img, (900, 1150), 520, (255, 150, 90), 260, 0.55)
d = ImageDraw.Draw(img)
cx, cy, R = 900, 1250, 760
d.arc([cx - R, cy - R, cx + R, cy + R], 200, 340, fill=(255, 214, 170), width=6)
for k in range(41):
    a = math.radians(200 + k * 140 / 40)
    long = k % 5 == 0
    r1, r2 = R - (70 if long else 36), R - 6
    d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a)), (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
           fill=(255, 214, 170), width=6 if long else 3)
a = math.radians(256)
d.line([(cx, cy), (cx + (R + 40) * math.cos(a), cy + (R + 40) * math.sin(a))], fill=(255, 70, 70), width=10)
d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(255, 70, 70))
save(img, "Night Signal")

# 2. The Long Wave: stacked sine waves, like an oscilloscope.
img = gradient((6, 34, 44), (4, 18, 26))
d = ImageDraw.Draw(img)
for row in range(14):
    y0 = 300 + row * 92
    amp = 30 + 90 * math.sin(math.pi * row / 13)
    freq = 2.2 + row * 0.12
    pts = [(x, y0 + amp * math.sin(2 * math.pi * freq * x / N + row * 0.6) * math.sin(math.pi * x / N)) for x in range(0, N + 1, 6)]
    shade = 120 + int(120 * math.sin(math.pi * row / 13))
    d.line(pts, fill=(60, shade, min(255, shade + 30)), width=5)
save(img.filter(ImageFilter.GaussianBlur(0.6)), "The Long Wave")

# 3. Studio Nine Sessions: a 1940s studio microphone, as simple shapes.
img = gradient((52, 22, 60), (28, 12, 34))
img = glow(img, (900, 800), 600, (255, 170, 60), 300, 0.45)
d = ImageDraw.Draw(img)
d.rounded_rectangle([640, 300, 1160, 1120], radius=260, fill=(240, 196, 110))
for y in range(400, 1040, 34):
    d.line([(700, y), (1100, y)], fill=(150, 100, 50), width=8)
d.rounded_rectangle([620, 650, 1180, 760], radius=30, fill=(200, 150, 80))
d.rectangle([870, 1120, 930, 1450], fill=(200, 150, 80))
d.rounded_rectangle([640, 1440, 1160, 1500], radius=30, fill=(200, 150, 80))
save(img, "Studio Nine Sessions")

# 4. Harbor Lights: a lighthouse beam over a dark sea.
img = gradient((10, 20, 44), (30, 52, 92))
beam = Image.new("L", (N, N), 0)
ImageDraw.Draw(beam).polygon([(520, 700), (N + 400, 250), (N + 400, 1050)], fill=200)
beam = beam.filter(ImageFilter.GaussianBlur(60))
img = Image.composite(Image.new("RGB", (N, N), (255, 236, 180)), img, beam.point(lambda v: int(v * 0.55)))
d = ImageDraw.Draw(img)
d.rectangle([0, 1250, N, N], fill=(8, 16, 34))
for k in range(9):
    y = 1300 + k * 52
    d.line([(0, y), (N, y)], fill=(30 + k * 4, 56 + k * 4, 96 + k * 3), width=4)
d.polygon([(470, 1250), (570, 1250), (545, 760), (495, 760)], fill=(225, 225, 230))
d.rectangle([480, 700, 560, 760], fill=(255, 220, 140))
d.polygon([(470, 700), (570, 700), (520, 640)], fill=(200, 60, 60))
img = glow(img, (520, 730), 70, (255, 230, 150), 40, 0.9)
save(img, "Harbor Lights")

# 5. Field Notes: topographic contour lines.
img = gradient((226, 236, 200), (190, 214, 160))
d = ImageDraw.Draw(img)
rnd = random.Random(5)
for cx, cy, n in [(650, 700, 13), (1250, 1200, 10)]:
    for k in range(n, 0, -1):
        r = k * 52
        pts = []
        for s in range(0, 361, 4):
            a = math.radians(s)
            wob = 1 + 0.12 * math.sin(3 * a + k) + 0.06 * math.sin(5 * a + cx)
            pts.append((cx + r * wob * math.cos(a), cy + r * 0.82 * wob * math.sin(a)))
        d.line(pts, fill=(60, 110, 60) if k % 4 else (30, 80, 40), width=5 if k % 4 else 8)
save(img, "Field Notes")

# 6. Low Tide: a retro poster, a big sun setting over striped waves.
img = Image.new("RGB", (N, N), (255, 226, 190))
d = ImageDraw.Draw(img)
d.ellipse([400, 520, 1400, 1520], fill=(250, 110, 80))
d.rectangle([0, 1020, N, N], fill=(255, 226, 190))
colours = [(250, 140, 100), (244, 170, 120), (236, 196, 150), (226, 214, 180)]
for k in range(8):
    y = 1060 + k * 92
    pts = [(x, y + 18 * math.sin(2 * math.pi * x / 360 + k)) for x in range(0, N + 1, 8)]
    d.line(pts, fill=colours[k % 4], width=40)
save(img, "Low Tide")

# 7. Northern Lines: aurora curtains over one horizon line.
img = gradient((6, 8, 24), (24, 18, 60))
rnd = random.Random(7)
d = ImageDraw.Draw(img)
for _ in range(220):
    x, y, s = rnd.randint(0, N), rnd.randint(0, 900), rnd.choice([2, 3, 4])
    d.ellipse([x, y, x + s, y + s], fill=(220, 220, 255))
from PIL import ImageChops
for width, blur in ((190, 70), (46, 18)):           # a wide soft glow, then a brighter core
    aur = Image.new("RGB", (N, N), (0, 0, 0))
    a = ImageDraw.Draw(aur)
    for k, col in enumerate([(70, 255, 160), (110, 150, 255), (200, 110, 255)]):
        pts = [(x, 560 + k * 170 + 150 * math.sin(x / 240 + k * 1.9)) for x in range(-40, N + 41, 8)]
        a.line(pts, fill=col, width=width)
    img = ImageChops.screen(img, aur.filter(ImageFilter.GaussianBlur(blur)))
d = ImageDraw.Draw(img)
d.rectangle([0, 1380, N, N], fill=(8, 8, 20))
d.line([(0, 1380), (N, 1380)], fill=(170, 160, 255), width=4)
save(img, "Northern Lines")

# 8. The Quiet Hour: almost empty, a small moon and a hairline horizon.
img = gradient((238, 234, 226), (214, 210, 204))
d = ImageDraw.Draw(img)
d.ellipse([1180, 430, 1330, 580], fill=(150, 160, 175))
d.line([(260, 1240), (N - 260, 1240)], fill=(140, 140, 150), width=4)
save(img, "The Quiet Hour")

# 9. Parallax: a ringed planet in a field of stars.
img = gradient((2, 4, 14), (6, 20, 40))
d = ImageDraw.Draw(img)
rnd = random.Random(9)
for _ in range(300):
    x, y, s = rnd.randint(0, N), rnd.randint(0, N), rnd.choice([2, 3, 3, 5])
    d.ellipse([x, y, x + s, y + s], fill=(200, 230, 255))
img = glow(img, (900, 900), 420, (0, 160, 255), 180, 0.5)
planet = gradient((40, 220, 255), (0, 60, 120))
mask = Image.new("L", (N, N), 0)
ImageDraw.Draw(mask).ellipse([620, 620, 1180, 1180], fill=255)
ring = Image.new("L", (N, N), 0)
r = ImageDraw.Draw(ring)
r.ellipse([300, 800, 1500, 1000], outline=255, width=26)
back = ring.copy(); ImageDraw.Draw(back).rectangle([0, 0, N, 900], fill=0)
front = ring.copy(); ImageDraw.Draw(front).rectangle([0, 900, N, N], fill=0)
img = Image.composite(Image.new("RGB", (N, N), (170, 230, 255)), img, back)
img = Image.composite(planet, img, mask)
img = Image.composite(Image.new("RGB", (N, N), (170, 230, 255)), img, front)
save(img, "Parallax")

# 10. Common Ground: two overlapping circles, like a conversation.
img = Image.new("RGB", (N, N), (248, 238, 226))
left = Image.new("L", (N, N), 0); ImageDraw.Draw(left).ellipse([300, 500, 1100, 1300], fill=255)
right = Image.new("L", (N, N), 0); ImageDraw.Draw(right).ellipse([700, 500, 1500, 1300], fill=255)
img = Image.composite(Image.new("RGB", (N, N), (226, 96, 70)), img, left)
img = Image.composite(Image.new("RGB", (N, N), (246, 170, 90)), img, right)
both = Image.new("L", (N, N), 0); both.paste(255, mask=Image.composite(left, Image.new("L", (N, N), 0), right))
img = Image.composite(Image.new("RGB", (N, N), (150, 46, 40)), img, both)
save(img, "Common Ground")
print("ok")
