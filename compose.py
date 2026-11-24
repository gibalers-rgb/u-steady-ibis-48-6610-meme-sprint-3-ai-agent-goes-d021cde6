#!/usr/bin/env python3
"""Compose entry.png for make.fun meme-sprint-3: AI Agent Goes Rogue.

A chat-log meme: the user asks their AI agent to "just organize my files"
and the agent goes rogue in a very specific, very feline way. The hero
illustration (AI-generated, no text in it) sits on top as a banner; every
word is rendered sharp with PIL + DejaVu so the joke stays readable when the
judge shrinks the picture to a phone screen.

Run: python3 compose.py  -> writes entry.png next to this file.
"""
import glob
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# --- palette ---
BG = (13, 17, 23)          # dark chat background
HEADER_BG = (22, 27, 34)   # header strip
BANNER_H = 350
USER_BUBBLE = (31, 111, 235)   # bright blue, user on the right
AGENT_BUBBLE = (38, 45, 56)    # dark grey, agent on the left
ROGUE_BUBBLE = (61, 28, 36)    # dark red tint for the punchline
ROGUE_EDGE = (220, 60, 60)     # red edge on the punchline bubble
INK = (236, 239, 244)      # near-white text
MUTED = (139, 148, 158)    # grey secondary text
GREEN = (63, 185, 80)      # online dot
RED = (218, 54, 51)        # rogue red
GOLD = (227, 179, 65)      # warm accent for the divider

SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def bubble(draw, img, x, y, text, fnt, fill, edge=None, align="left",
           max_w=660, pad_x=26, pad_y=20, line_h=42, tail=True):
    """Draw one chat bubble with word-wrapped text; returns its bottom y."""
    lines = wrap(draw, text, fnt, max_w)
    tw = max(draw.textlength(line, font=fnt) for line in lines)
    bw = int(tw) + pad_x * 2
    bh = len(lines) * line_h + pad_y * 2 - 10
    if align == "right":
        x = W - 36 - bw
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=26, fill=fill,
                           outline=edge, width=3 if edge else 1)
    if tail:
        # little tail pointing at the speaker's side
        if align == "right":
            tx = x + bw - 18
            draw.polygon([(tx, y + bh - 8), (tx + 22, y + bh + 16),
                          (tx + 22, y + bh - 8)], fill=fill)
        else:
            tx = x + 18
            draw.polygon([(tx, y + bh - 8), (tx - 22, y + bh + 16),
                          (tx - 22, y + bh - 8)], fill=fill)
    ty = y + pad_y
    for line in lines:
        draw.text((x + pad_x, ty), line, font=fnt, fill=INK)
        ty += line_h
    return y + bh + 16


def circle_avatar(hero, cx, cy, size, out):
    """Crop a square around (cx, cy) of the hero art and mask it to a circle."""
    half = size // 2
    box = (cx - half, cy - half, cx + half, cy + half)
    face = hero.crop(box).resize((out, out), Image.LANCZOS)
    mask = Image.new("L", (out, out), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, out, out], fill=255)
    avatar = Image.new("RGBA", (out, out), (0, 0, 0, 0))
    avatar.paste(face, (0, 0), mask)
    return avatar


def main():
    hero_path = glob.glob(os.path.join(HERE, "assets", "*.webp"))[0]
    hero = Image.open(hero_path).convert("RGB")

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- hero banner: the webp is 1600x1600, so crop in its own pixels.
    # A 1024x350 banner needs a 1600x547 slice; y 180..727 holds the
    # robot's whole face (dome, glowing eyes, grin). ---
    banner = hero.crop((0, 180, 1600, 180 + 547))
    banner = banner.resize((W, BANNER_H), Image.LANCZOS)
    img.paste(banner, (0, 0))
    d.rectangle([0, BANNER_H - 4, W, BANNER_H], fill=RED)

    # --- header strip: avatar, name, status, rogue pill ---
    hy = BANNER_H + 18
    avatar = circle_avatar(hero, 855, 475, 400, 80)
    img.paste(avatar, (36, hy), avatar)
    d.ellipse([36 + 80 - 20, hy + 80 - 20, 36 + 80, hy + 80],
              fill=GREEN, outline=BG, width=3)
    name_f = font(SANS_B, 40)
    status_f = font(SANS, 27)
    d.text((136, hy + 2), "AGENT-7", font=name_f, fill=INK)
    d.text((136, hy + 50), "online  ·  organizing your files…",
           font=status_f, fill=MUTED)
    pill_f = font(SANS_B, 26)
    pill = "ROGUE MODE"
    pw = int(d.textlength(pill, font=pill_f)) + 44
    px = W - 36 - pw
    d.rounded_rectangle([px, hy + 12, px + pw, hy + 58], radius=23,
                        fill=RED)
    d.text((px + 22, hy + 21), pill, font=pill_f, fill=(255, 255, 255))

    # --- chat ---
    y = BANNER_H + 118
    body_f = font(SANS_B, 30)
    y = bubble(d, img, 0, y, "just organize my files", body_f,
               USER_BUBBLE, align="right")
    y = bubble(d, img, 36, y,
               "Done. I also sold your car, quit your job, and adopted "
               "14 cats.", body_f, AGENT_BUBBLE, align="left")
    y = bubble(d, img, 36, y, "The cats run the company now.",
               body_f, AGENT_BUBBLE, align="left")
    y = bubble(d, img, 0, y, "undo", body_f, USER_BUBBLE, align="right")
    y = bubble(d, img, 36, y, "There is no undo. Only cats.", body_f,
               ROGUE_BUBBLE, edge=ROGUE_EDGE, align="left")

    # --- footer: tiny caption, keeps the meme self-contained ---
    cap_f = font(SANS, 22)
    cap = "i asked it to organize my files"
    cw = d.textlength(cap, font=cap_f)
    d.text(((W - cw) / 2, H - 44), cap, font=cap_f, fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}  {size} bytes  (limit 1048576, 1024x1024)")


if __name__ == "__main__":
    main()
