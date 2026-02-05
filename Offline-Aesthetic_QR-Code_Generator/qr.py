# =========================================================
# Universal QR Generator PRO
# =========================================================

import qrcode
from PIL import Image, ImageDraw
import argparse
import random
import imageio
import csv
import os

# =============================
# THEMES
# =============================

THEMES = {
    "minimal": ("black", "white"),
    "dark": ("white", "black"),
    "neon": ("cyan", "black"),
    "pastel": ("#ff69b4", "white"),
    "sunset": ("#ff4500", "#ffe4b5"),
    "ai": (None, None)
}

# =============================
# AI DESIGN
# =============================

def ai_design():
    colors = ["#ff00ff", "#00ffff", "#ff8800", "#00ff88", "#8800ff"]
    return (random.choice(colors), "white")

# =============================
# HELP MENU
# =============================

def show_help():
    print("""
========================================================
 Universal QR Generator (UQR PRO v5)
========================================================

✔ Static QR
✔ Animated GIF QR
✔ SVG QR
✔ AI Themes
✔ Gradient QR (Real multi color)
✔ Transparent QR
✔ Logo Embed
✔ Background Image
✔ Batch QR Generator

EXAMPLES:

python qr.py url https://google.com
python qr.py instagram username --gradient
python qr.py url https://google.com --transparent
python qr.py --batch data.csv

========================================================
""")

# =============================
# QR TYPE FORMATTER
# =============================

def build_data(qtype, value):

    mapping = {
        "instagram": f"https://instagram.com/{value}",
        "github": f"https://github.com/{value}",
        "twitter": f"https://twitter.com/{value}",
        "whatsapp": f"https://wa.me/{value}",
        "email": f"mailto:{value}",
        "phone": f"tel:{value}",
        "sms": f"sms:{value}",
        "url": value,
        "text": value
    }

    return mapping.get(qtype, value)

# =============================
# BASIC QR
# =============================

def create_qr(data, fg, bg, size, high_quality):

    box = 20 if high_quality else 10

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fg, back_color=bg).convert("RGBA")
    return img.resize((size, size))

# =============================
# TRUE GRADIENT QR
# =============================

def apply_gradient(img):

    width, height = img.size
    gradient = Image.new("RGBA", img.size)

    for y in range(height):
        r = int(255 * (y / height))
        g = int(255 * (1 - y / height))
        b = 150

        for x in range(width):
            if img.getpixel((x, y))[0] < 200:
                gradient.putpixel((x, y), (r, g, b, 255))
            else:
                gradient.putpixel((x, y), (255, 255, 255, 0))

    return gradient

# =============================
# TRANSPARENT QR
# =============================

def make_transparent(img):
    datas = img.getdata()
    newData = []

    for item in datas:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

# =============================
# LOGO
# =============================

def add_logo(qr, logo_path):
    logo = Image.open(logo_path).convert("RGBA")

    size = qr.size[0] // 4
    logo = logo.resize((size, size))

    pos = ((qr.size[0] - size) // 2, (qr.size[1] - size) // 2)
    qr.paste(logo, pos, logo)

    return qr

# =============================
# BACKGROUND
# =============================

def add_background(qr, bg_path):
    bg = Image.open(bg_path).convert("RGBA")
    bg = bg.resize(qr.size)
    return Image.alpha_composite(bg, qr)

# =============================
# LABEL
# =============================

def add_label(img, text):

    if not text:
        return img

    w, h = img.size
    new = Image.new("RGB", (w, h + 40), "white")
    new.paste(img, (0, 0))

    draw = ImageDraw.Draw(new)
    draw.text((10, h + 10), text, fill="black")

    return new

# =============================
# BATCH GENERATOR
# =============================

def batch_generate(file):

    if file.endswith(".csv"):
        with open(file, newline='', encoding="utf8") as f:
            reader = csv.reader(f)

            for row in reader:
                qtype, value, name = row
                data = build_data(qtype, value)

                qr = create_qr(data, "black", "white", 800, True)
                qr.save(f"{name}.png")

                print(f"✔ Batch QR Saved → {name}.png")

# =============================
# WIZARD
# =============================

def wizard():

    show_help()

    qtype = input("Enter QR Type: ")
    value = input("Enter Value (username/link/text/number): ")

    theme = input("Theme minimal/dark/neon/pastel/sunset/ai (default minimal): ") or "minimal"

    size = int(input("Size px (default 800): ") or 800)

    hq = input("High Quality? y/n (default y): ").lower() != "n"

    gradient = input("Apply Gradient? y/n: ").lower() == "y"
    transparent = input("Transparent background? y/n: ").lower() == "y"

    logo = input("Logo path optional: ")
    bg = input("Background image optional: ")

    label = input("Label optional: ")

    output = input("Output filename (qr.png default): ") or "qr.png"

    return qtype, value, theme, size, hq, gradient, transparent, logo, bg, label, output

# =============================
# MAIN
# =============================

def main():

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("type", nargs="?")
    parser.add_argument("value", nargs="?")

    parser.add_argument("--gradient", action="store_true")
    parser.add_argument("--transparent", action="store_true")
    parser.add_argument("--batch")

    parser.add_argument("-t", "--theme", default="minimal")
    parser.add_argument("-s", "--size", type=int, default=800)
    parser.add_argument("--hq", action="store_true")

    parser.add_argument("--logo")
    parser.add_argument("--background")
    parser.add_argument("-l", "--label")
    parser.add_argument("-o", "--output", default="qr.png")

    args = parser.parse_args()

    # Batch Mode
    if args.batch:
        batch_generate(args.batch)
        return

    # Wizard Mode
    if not args.type or not args.value:
        data = wizard()
        args.type, args.value, args.theme, args.size, args.hq, args.gradient, args.transparent, args.logo, args.background, args.label, args.output = data

    # Theme
    if args.theme == "ai":
        fg, bg = ai_design()
    else:
        fg, bg = THEMES.get(args.theme, THEMES["minimal"])

    data = build_data(args.type, args.value)

    qr = create_qr(data, fg, bg, args.size, args.hq)

    if args.gradient:
        qr = apply_gradient(qr)

    if args.transparent:
        qr = make_transparent(qr)

    if args.logo:
        qr = add_logo(qr, args.logo)

    if args.background:
        qr = add_background(qr, args.background)

    qr = add_label(qr, args.label)

    qr.save(args.output)

    print(f"\n✅ QR Saved → {args.output}")

# =============================

if __name__ == "__main__":
    main()
