"""Generate iRoyalty Studio brand images with code (PIL + numpy). Font: Outfit (SIL OFL)."""
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/usr/share/fonts/truetype/sand-box/google/Outfit/Outfit-VariableFont_wght.ttf"
BG0, BG1 = (14, 14, 36), (34, 28, 82)
GOLD, GOLD2 = (246, 200, 76), (255, 228, 150)
INK = (236, 234, 255)
MONTAGE = "/workspace/unity-asset-store/combo-ladder/preview/ComboLadder_Preview.wav"
OUT = "/workspace/unity-asset-store/site/assets/img/"


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def gradient(w, h, diag=True):
    y, x = np.mgrid[0:h, 0:w]
    t = ((x / w) * 0.6 + (y / h) * 0.4) if diag else y / h
    arr = np.zeros((h, w, 3))
    for c in range(3):
        arr[..., c] = BG0[c] + (BG1[c] - BG0[c]) * t
    return Image.fromarray(arr.astype(np.uint8))


def crown_mark(d, cx, cy, s, glow_img=None):
    """Crown built from five rounded meter bars on a base bar. s = overall width."""
    heights = [0.78, 0.48, 1.0, 0.48, 0.78]
    bw = s / 9.0
    gap = (s - 5 * bw) / 4
    hmax = s * 0.62
    base_h = bw * 0.9
    base_top = cy + hmax / 2 - base_h
    x0 = cx - s / 2
    for k, hh in enumerate(heights):
        x = x0 + k * (bw + gap)
        top = base_top - hmax * hh * 0.82
        d.rounded_rectangle([x, top, x + bw, base_top + bw * 0.2], radius=bw / 2, fill=GOLD)
        # jewel dot on the tall bars
        if hh > 0.7:
            r = bw * 0.42
            d.ellipse([x + bw / 2 - r, top - r * 2.6 - r, x + bw / 2 + r, top - r * 2.6 + r], fill=GOLD2)
    d.rounded_rectangle([x0 - bw * 0.3, base_top, x0 + s + bw * 0.3, base_top + base_h], radius=base_h / 2, fill=GOLD)


def profile(size=512):
    img = gradient(size, size)
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([size * .18, size * .18, size * .82, size * .82], fill=(246, 200, 76, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(size * 0.09))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    d = ImageDraw.Draw(img)
    d.ellipse([size * .06, size * .06, size * .94, size * .94], outline=(246, 200, 76, 90), width=max(2, size // 128))
    crown_mark(d, size / 2, size * 0.47, size * 0.52)
    f = font(int(size * 0.085), 600)
    t = "iRoyalty"
    w = d.textlength(t, font=f)
    d.text((size / 2 - w / 2, size * 0.70), t, font=f, fill=INK)
    return img.convert("RGB")


def waveform_strip(w, h):
    x, sr = sf.read(MONTAGE, always_2d=True)
    m = np.abs(x.mean(axis=1))
    n = w // 6
    seg = np.array_split(m, n)
    env = np.array([s.max() for s in seg])
    env = env / env.max()
    return env


def banner(w=2400, h=600):
    img = gradient(w, h).convert("RGBA")
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    env = waveform_strip(w, h)
    # waveform of the real Combo Ladder preview, fading in from the middle so text stays clean
    for i, v in enumerate(env):
        x = i * 6 + 3
        fx = x / w
        if fx < 0.6:
            continue
        alpha = int(150 * min(1.0, (fx - 0.6) / 0.15))
        hh = max(2, v * h * 0.36)
        d.rounded_rectangle([x - 1.5, h * 0.5 - hh, x + 1.5, h * 0.5 + hh], radius=1.5, fill=(246, 200, 76, alpha))
    img = Image.alpha_composite(img, layer)
    d = ImageDraw.Draw(img)
    crown_mark(d, h * 0.62, h * 0.5, h * 0.62)
    d.text((h * 1.12, h * 0.27), "iRoyalty Studio", font=font(int(h * 0.19), 700), fill=INK)
    d.text((h * 1.14, h * 0.56), "Procedurally synthesized game audio", font=font(int(h * 0.075), 400), fill=GOLD2)
    return img.convert("RGB")


def og(w=1200, h=630):
    img = gradient(w, h).convert("RGBA")
    d = ImageDraw.Draw(img)
    crown_mark(d, w / 2, h * 0.36, h * 0.42)
    f = font(int(h * 0.12), 700)
    t = "iRoyalty Studio"
    d.text((w / 2 - d.textlength(t, font=f) / 2, h * 0.60), t, font=f, fill=INK)
    f2 = font(int(h * 0.05), 400)
    t2 = "Procedurally synthesized game audio"
    d.text((w / 2 - d.textlength(t2, font=f2) / 2, h * 0.78), t2, font=f2, fill=GOLD2)
    return img.convert("RGB")


if __name__ == "__main__":
    profile(512).save(OUT + "iroyalty-profile-512.png", optimize=True)
    profile(64).resize((32, 32), Image.LANCZOS).save(OUT + "favicon-32.png")
    profile(180).save(OUT + "apple-touch-icon.png")
    banner().save(OUT + "iroyalty-banner-2400x600.png", optimize=True)
    og().save(OUT + "og-1200x630.png", optimize=True)
    print("ok")
