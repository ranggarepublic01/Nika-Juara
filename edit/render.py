"""Render the JUARA! illustrated lyric video.

Stills are drawn frame by frame (camera moves, beat pulses, flashes, rain, confetti),
Veo clips are fitted to their slots, then lyrics (ASS, Anton) and the song are added.

  python3 edit/render.py                 # full video -> edit/out/JUARA_lyric_video.mp4
  python3 edit/render.py --from 84 --to 150 --name preview   # a time range only
"""
import argparse, math, random, re, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "assets"
EDIT = ROOT / "edit"
WORK = EDIT / "work"
OUT = EDIT / "out"
FONT = EDIT / "fonts" / "Anton-Regular.ttf"
LRC = ROOT / "lyrics" / "JUARA_final_suno.lrc"
SONG = A / "JUARA.mp3"
W, H, FPS = 1920, 1080, 24
SONG_END = 357.6

# ---------------------------------------------------------------- lyrics (from the LRC)
def secs(ts):
    m, s = ts.split(":"); return int(m) * 60 + float(s)

LINES = []
for raw in LRC.read_text(encoding="utf-8").splitlines():
    m = re.match(r"\[(\d+:\d+\.\d+)\](.*)", raw.strip())
    if m:
        LINES.append([(secs(t), w.strip()) for t, w in re.findall(r"<(\d+:\d+\.\d+)>([^<]*)", m.group(2))])
FIX = {10: "entah kapan tiba...", 11: "Senin malam, GBK penuh lagi"}

def kind(n):
    if n == 1: return "hidden"
    if n in (2, 3, 19, 20, 21, 22, 33, 34, 35, 36, 49, 50): return "chant"
    if n in (4, 15, 17, 29, 31, 41, 43, 45, 47): return "juara"
    if n in (5, 16, 18, 30, 32, 42, 44, 46, 48): return "chorus"
    if 6 <= n <= 10: return "flashback"
    if 37 <= n <= 40: return "bridge"
    if n in (51, 52): return "asia"
    return "verse"

LEAD = 0.20
HOLD = {"verse": 1.6, "flashback": 1.6, "chorus": 1.4, "juara": 1.0, "chant": 1.0, "bridge": 2.2, "asia": 1.6}
CUES = []
for i, words in enumerate(LINES):
    n = i + 1; k = kind(n)
    if k == "hidden": continue
    if n in FIX:  # keep timings, swap the on-screen spelling word by word
        fixed = FIX[n].split(" ")
        words = [(t, fixed[j]) for j, (t, _) in enumerate(words)]
    t_in = max(0.0, words[0][0] - LEAD)
    nxt = LINES[i + 1][0][0] - LEAD if i + 1 < len(LINES) else SONG_END
    hold = 3.0 if n == len(LINES) else HOLD[k]
    CUES.append((n, t_in, min(nxt - 0.05, words[-1][0] + hold), k, words))

# ---------------------------------------------------------------- timeline
def wt(n, j):  # LRC word time
    return LINES[n - 1][j][0]

JUARA_HITS = [w[0] for c in CUES if c[3] == "juara" for w in c[4]]
GARUDA_HITS = [w[0] for c in CUES if c[3] == "chant" for w in c[4] if w[1].lower().startswith("garuda")]

def hits(lo, hi, ts): return [t for t in ts if lo <= t < hi]

# Still segment: camera keys (t, zoom, cx, cy), pulses (t, amp), flashes, fx windows
SEGMENTS = [
 dict(kind="clip", src="M1", t0=0.0, t1=11.1),
 dict(kind="still", src="A1", t0=11.1, t1=22.3, keys=[(11.1, 1.00, .50, .40), (22.3, 1.12, .49, .22)]),
 dict(kind="still", src="A2", t0=22.3, t1=35.7, keys=[(22.3, 1.05, .50, .60), (35.7, 1.08, .50, .54)],
      pulses=[(t, .03) for t in hits(22.3, 29.6, GARUDA_HITS)] + [(t, .06) for t in hits(29.6, 35.7, JUARA_HITS)], flashes=[29.70]),
 dict(kind="clip", src="M3", t0=35.7, t1=46.0),
 dict(kind="clip", src="M4", t0=46.0, t1=56.0),
 dict(kind="clip", src="M5", t0=56.0, t1=66.0),
 dict(kind="clip", src="M6", t0=66.0, t1=76.0),
 dict(kind="still", src="A3", t0=76.0, t1=84.8, keys=[(76.0, 1.00, .50, .50), (84.8, 1.12, .50, .58)]),
 dict(kind="still", src="A4", t0=84.8, t1=102.6, keys=[(84.8, 1.10, .45, .50), (wt(8, 4), 1.18, .38, .56), (102.6, 1.20, .38, .56)], rain=True),
 dict(kind="still", src="A5", t0=102.6, t1=132.2,
      keys=[(102.6, 1.00, .50, .45), (117.0, 1.15, .50, .42), (wt(14, 1) - 0.01, 1.16, .50, .42), (wt(14, 1), 1.20, .50, .42), (132.2, 1.22, .50, .42)],
      vignette=(117.0, wt(14, 1)), flashes=[wt(14, 1)], shakes=[wt(14, 1)], confetti=(wt(14, 1), 132.2)),
 dict(kind="still", src="A6", t0=132.2, t1=146.7, keys=[(132.2, 1.02, .58, .40), (146.7, 1.06, .58, .38)],
      pulses=[(t, .08) for t in hits(132.0, 146.7, JUARA_HITS)], flashes=[wt(15, 0)], confetti=(132.2, 146.7)),
 dict(kind="still", src="A2", t0=146.7, t1=165.6, keys=[(146.7, 1.25, .50, .55), (160.0, 1.25, .50, .55), (165.6, 1.00, .50, .50)],
      pulses=[(t, .03) for t in hits(146.7, 160.0, GARUDA_HITS)]),
 dict(kind="clip", src="M7", t0=165.6, t1=175.6),
 dict(kind="still", src="A1", t0=175.6, t1=189.7, keys=[(175.6, 1.18, .22, .25), (189.7, 1.08, .50, .35)]),
 dict(kind="still", src="A7", t0=189.7, t1=222.8,
      keys=[(189.7, 1.00, .50, .45), (wt(28, 1), 1.06, .52, .42), (wt(32, 0), 1.08, .52, .42), (222.8, 1.16, .53, .36)],
      dark=(189.7, wt(28, 1)), flashes=[wt(28, 1), wt(29, 0)], shakes=[wt(28, 1)],
      pulses=[(t, .06) for t in hits(207.0, 222.8, JUARA_HITS)], confetti=(207.9, 222.8)),
 dict(kind="still", src="A8", t0=222.8, t1=236.2, keys=[(222.8, 1.12, .58, .50), (236.2, 1.12, .44, .50)],
      pulses=[(t, .03) for t in hits(222.8, 236.2, GARUDA_HITS)]),
 dict(kind="clip", src="M8", t0=236.2, t1=246.2),
 dict(kind="clip", src="M9", t0=246.2, t1=256.2),
 dict(kind="clip", src="M10", t0=256.2, t1=266.2),
 dict(kind="still", src="A4", t0=266.2, t1=280.2, keys=[(266.2, 1.35, .37, .45), (280.2, 1.40, .37, .48)], rain=True),
 dict(kind="still", src="A9", t0=280.2, t1=298.5, keys=[(280.2, 1.00, .53, .47), (wt(40, 4), 1.10, .53, .45), (298.5, 1.10, .53, .45)], bloom=True),
 dict(kind="still", src="A10", t0=298.5, t1=SONG_END,
      keys=[(298.5, 1.00, .50, .50), (312.4, 1.00, .50, .50), (312.9, 1.15, .50, .46), (327.3, 1.15, .50, .46), (328.5, 1.05, .50, .50),
            (339.0, 1.05, .50, .50), (352.0, 1.30, .28, .18), (SONG_END, 1.32, .27, .17)],
      pulses=[(t, .06) for t in hits(298.0, 327.3, JUARA_HITS)] + [(t, .03) for t in hits(327.3, 332.0, GARUDA_HITS)] + [(wt(51, 0), .08), (wt(52, 0), .08)],
      flashes=[wt(41, 0), wt(45, 0)], confetti=(298.5, 339.0), endcard=(342.0, 344.0)),
]

# ---------------------------------------------------------------- frame drawing
def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)

def cam_at(keys, t):
    if t <= keys[0][0]: return keys[0][1:]
    for (ta, *a), (tb, *b) in zip(keys, keys[1:]):
        if t <= tb:
            u = ease((t - ta) / (tb - ta)) if tb > ta else 1.0
            return tuple(x + (y - x) * u for x, y in zip(a, b))
    return keys[-1][1:]

def decay(t, t0, tau):
    return math.exp(-(t - t0) / tau) if t >= t0 else 0.0

def make_vignette():
    y, x = np.mgrid[0:H, 0:W]
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return np.clip((r - 0.45) / 0.75, 0, 1) ** 1.5  # 0 centre .. 1 corners

def rain_layer(seed):
    rnd = random.Random(seed); im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for _ in range(420):
        x, y, L = rnd.uniform(-100, W), rnd.uniform(0, H), rnd.uniform(25, 70)
        d.line([(x, y), (x + L * 0.18, y + L)], fill=(200, 215, 235, rnd.randint(40, 95)), width=2)
    return im

CONF_COLS = [(200, 16, 46), (244, 239, 230), (242, 179, 61)]
def confetti_layer(t, t0, seed=7):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(110):
        x0, born, sp = rnd.uniform(0, W), rnd.uniform(-6, 30), rnd.uniform(70, 150)
        age = (t - t0) - born
        if age < 0: continue
        y = -30 + (age * sp) % (H + 60)
        x = x0 + 40 * math.sin(age * rnd.uniform(1, 3) + x0)
        s = rnd.uniform(6, 13); col = rnd.choice(CONF_COLS)
        ang = age * rnd.uniform(2, 6)
        dx, dy = s * math.cos(ang), s * 0.45 * abs(math.sin(ang)) + 2
        d.polygon([(x - dx, y - dy), (x + dx, y - dy), (x + dx, y + dy), (x - dx, y + dy)], fill=col + (210,))
    return im

PAPER = None
def paper():
    global PAPER
    if PAPER is None:
        rng = np.random.default_rng(3)
        n = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
        img = Image.fromarray(np.uint8(np.clip(128 + n * 40, 0, 255))).resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.8))
        a = np.asarray(img, dtype=np.float32) / 255.0
        PAPER = (a - a.mean()) * 0.10  # +-~5% luminance, static: compresses well
    return PAPER

def render_still(seg, f0, f1, path):
    src = Image.open(A / f"{seg['src']}.jpg").convert("RGB")
    SW, SH = src.size
    bloom_src = None
    if seg.get("bloom"):
        glow = ImageEnhance.Brightness(src.filter(ImageFilter.GaussianBlur(SW / 90))).enhance(1.25)
        bloom_src = Image.blend(src, glow, 0.22)
    vig = make_vignette() if seg.get("vignette") or seg.get("dark") else None
    rains = [rain_layer(s) for s in range(12)] if seg.get("rain") else None
    pap = paper()
    w0 = min(SW, SH * 16 / 9); h0 = w0 * 9 / 16
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", str(path)], stdin=subprocess.PIPE)
    shake_rng = random.Random(11)
    for fi in range(f0, f1):
        t = fi / FPS
        z, cx, cy = cam_at(seg["keys"], t)
        for tp, amp in seg.get("pulses", []):
            z *= 1 + amp * decay(t, tp, 0.14)
        w, h = w0 / z, h0 / z
        x = min(max(cx * SW - w / 2, 0), SW - w); y = min(max(cy * SH - h / 2, 0), SH - h)
        for ts in seg.get("shakes", []):
            if 0 <= t - ts < 4 / FPS:
                x += shake_rng.uniform(-1, 1) * w * 0.006; y += shake_rng.uniform(-1, 1) * h * 0.006
        base = bloom_src if bloom_src is not None else src
        fr = base.transform((W, H), Image.EXTENT, (x, y, x + w, y + h), Image.BICUBIC)
        if seg.get("dark") and seg["dark"][0] <= t < seg["dark"][1]:
            fr = ImageEnhance.Color(fr).enhance(0.45); fr = ImageEnhance.Brightness(fr).enhance(0.42)
            fr = fr.filter(ImageFilter.GaussianBlur(2))
        if seg.get("rain"):
            fr = Image.alpha_composite(fr.convert("RGBA"), rains[fi % len(rains)].transform(
                (W, H), Image.AFFINE, (1, 0, 0, 0, 1, -((fi * 37) % H)), Image.NEAREST)).convert("RGB")
        if seg.get("confetti") and seg["confetti"][0] <= t < seg["confetti"][1]:
            fr = Image.alpha_composite(fr.convert("RGBA"), confetti_layer(t, seg["confetti"][0])).convert("RGB")
        arr = np.asarray(fr, dtype=np.float32) / 255.0
        if vig is not None:
            k = 0.0
            if seg.get("vignette"):
                a, b = seg["vignette"]; k = ease((t - a) / max(0.01, b - a) * 1.5) if a <= t < b else 0.0
            if seg.get("dark") and seg["dark"][0] <= t < seg["dark"][1]: k = 0.8
            if k: arr *= (1 - 0.75 * k * vig)[..., None]
        if seg.get("endcard"):
            a, b = seg["endcard"]; arr *= 1 - 0.5 * ease((t - a) / (b - a))
        arr += pap[..., None]
        fl = max([decay(t, tf, 0.05) for tf in seg.get("flashes", []) if t >= tf] or [0])
        if fl > 0.02: arr = arr + (1 - arr) * fl * 0.9
        ff.stdin.write(np.uint8(np.clip(arr, 0, 1) * 255 + 0.5).tobytes())
    ff.stdin.close(); ff.wait()
    assert ff.returncode == 0, path

def render_clip(seg, f0, f1, path):
    n = f1 - f0
    dur = seg["t1"] - seg["t0"]
    src_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(A / f"{seg['src']}.mp4")]))
    k = dur / src_dur if 0.88 <= src_dur / dur <= 1.12 else 1.0  # stretch to fit, else trim
    off = (f0 / FPS - seg["t0"]) / k  # when rendering a partial range
    vf = (f"setpts=(PTS-STARTPTS)*{k:.5f},fps={FPS},scale={W}:{H}:flags=lanczos,format=rgb24")
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, off):.3f}", "-i", str(A / f"{seg['src']}.mp4"), "-an", "-vf", vf + ",tpad=stop_mode=clone:stop_duration=3",
                        "-frames:v", str(n), "-f", "rawvideo", "-"], capture_output=True, check=True)
    frames = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W, 3)
    pap = paper()
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", str(path)], stdin=subprocess.PIPE)
    for i in range(n):
        arr = frames[min(i, len(frames) - 1)].astype(np.float32) / 255.0 + pap[..., None]
        ff.stdin.write(np.uint8(np.clip(arr, 0, 1) * 255 + 0.5).tobytes())
    ff.stdin.close(); ff.wait()
    assert ff.returncode == 0, path

def render_seg(job):
    i, seg, f0, f1 = job
    path = WORK / f"seg{i:02d}_{seg['src']}_{f0}.mp4"
    src = A / (f"{seg['src']}.jpg" if seg["kind"] == "still" else f"{seg['src']}.mp4")
    if path.exists() and path.stat().st_mtime > max(src.stat().st_mtime, Path(__file__).stat().st_mtime):
        return path  # cached: neither the asset nor the renderer changed
    (render_still if seg["kind"] == "still" else render_clip)(seg, f0, f1, path)
    return path

# ---------------------------------------------------------------- lyrics as ASS
def c(hexrgb, a=0):
    r, g, b = hexrgb[0:2], hexrgb[2:4], hexrgb[4:6]; return f"&H{a:02X}{b}{g}{r}".upper()
OFF, GOLD, RED, CHAR, BLUE = "F4EFE6", "F2B33D", "C8102E", "1A1416", "BFD3E6"
PIL_RATIO = None
def text_w(s, fs):
    global PIL_RATIO
    if PIL_RATIO is None:
        a, d = ImageFont.truetype(str(FONT), 100).getmetrics(); PIL_RATIO = 100 / (a + d)
    return 0.86 * ImageFont.truetype(str(FONT), max(1, round(fs * PIL_RATIO))).getlength(s)  # libass draws ~0.86x Pillow's width

def ats(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def build_ass(path):
    st = [
     ("Verse", 110, OFF, OFF, CHAR, CHAR, 7, 0, 2, 110),
     ("Chorus", 160, OFF, OFF, CHAR, CHAR, 9, 0, 2, 170),
     ("Big", 220, OFF, OFF, CHAR, RED, 8, 10, 5, 0),
     ("Bridge", 96, OFF, OFF, OFF, CHAR, 0, 0, 2, 120),
     ("Title", 440, RED, RED, OFF, CHAR, 12, 12, 5, 0),
    ]
    head = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"]
    for name, fs, p1, p2, oc, bc, ol, sh, al, mv in st:
        head.append(f"Style: {name},Anton,{fs},{c(p1)},{c(p2)},{c(oc)},{c(bc)},0,0,0,0,100,100,0,0,1,{ol},{sh},{al},80,80,{mv},1")
    ev = ["", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    def add(layer, a, b, style, text): ev.append(f"Dialogue: {layer},{ats(a)},{ats(b)},{style},,0,0,0,,{text}")

    # soft backdrop behind lower-band text (merged per block)
    blocks = []
    for n, a, b, k, words in CUES:
        if k in ("verse", "flashback", "chorus", "bridge"):
            if blocks and a - blocks[-1][1] < 1.2: blocks[-1][1] = b
            else: blocks.append([a, b])
    blocks.insert(0, [1.0, 10.0])  # title
    NS, Y0 = 40, 560  # gradient from transparent at Y0 to ~50% charcoal at the bottom, drawn as thin strips
    for a, b in blocks:
        for k in range(NS):
            ya, yb = Y0 + (H - Y0) * k / NS, Y0 + (H - Y0) * (k + 1) / NS + 1
            alpha = 255 - round(255 * 0.5 * ease((k + 0.5) / NS))
            add(0, a - 0.3, b + 0.3, "Verse", f"{{\\an7\\pos(0,0)\\p1\\bord0\\shad0\\1c{c(CHAR)}\\1a&H{alpha:02X}&\\fad(300,300)}}m 0 {ya:.0f} l {W} {ya:.0f} l {W} {yb:.0f} l 0 {yb:.0f}{{\\p0}}")

    # title
    add(2, 1.0, 10.0, "Title", f"{{\\an5\\pos(960,690)\\fad(150,500)\\fscx118\\fscy118\\t(0,180,\\fscx100\\fscy100)\\t(180,9000,\\fscx105\\fscy105)}}JUARA!")
    add(2, 1.0, 10.0, "Verse", f"{{\\an5\\pos(960,470)\\fs64\\fsp12\\bord5\\fad(300,500)}}NIKA MUSIC")

    # end screen message, upper half (the lower half stays free for YouTube end-screen elements)
    E0, E1 = 342.8, SONG_END - 0.1
    add(2, E0, E1, "Verse", f"{{\\an5\\pos(960,190)\\fs70\\fsp6\\bord5\\fad(600,400)}}Terima kasih sudah menonton")
    add(2, E0 + 0.6, E1, "Title", f"{{\\an5\\pos(960,355)\\fs300\\fad(200,400)\\fscx115\\fscy115\\t(0,200,\\fscx100\\fscy100)}}JUARA!")
    add(2, E0 + 1.2, E1, "Verse", f"{{\\an5\\pos(960,515)\\fs62\\fsp14\\1c{c(GOLD)}\\bord5\\fad(600,400)}}persembahan NIKA MUSIC")

    for n, a, b, k, words in CUES:
        if k in ("verse", "flashback", "chorus"):
            style = "Chorus" if k == "chorus" else "Verse"
            pre = f"{{\\fad(250,200)}}" if k != "flashback" else f"{{\\fad(500,500)\\1c{c(BLUE)}}}"
            parts = [pre, f"{{\\k{round((words[0][0] - a) * 100)}}}"]
            if k != "flashback" and k != "chorus": parts[0] = f"{{\\fad(250,200)\\1c{c(GOLD)}}}"
            if k == "chorus": parts[0] = f"{{\\fad(150,150)\\1c{c(GOLD)}\\fscx110\\fscy110\\t(0,150,\\fscx100\\fscy100)}}"
            for j, (tw, word) in enumerate(words):
                nxt = words[j + 1][0] if j + 1 < len(words) else min(b, tw + 0.9)
                dur = round((nxt - tw) * 100)
                if k == "chorus" and re.sub(r"\W", "", word.lower()) in ("juara", "bapak"):
                    parts.append(f"{{\\kf{dur}\\2c{c(GOLD)}}}{word}{{\\2c{c(OFF)}}} ")
                else:
                    parts.append(f"{{\\kf{dur}}}{word} ")
            fs = {"Verse": 110, "Chorus": 160}[style]
            fit = min(1.0, 1700 / text_w(" ".join(w for _, w in words), fs))
            if fit < 1.0: parts[0] = parts[0][:-1] + f"\\fs{int(fs * fit)}}}"
            add(1, a, b, style, "".join(parts).rstrip())
        elif k == "bridge":
            text = " ".join(w for _, w in words)
            fsb = int(96 * min(1.0, 1600 / (text_w(text, 96) * 1.06)))
            text = f"{{\\fs{fsb}}}" + text
            add(1, a, b, "Bridge", f"{{\\fad(800,800)\\fsp4\\bord7\\blur9\\3c{c(OFF)}\\3a&HA0&\\1a&HFF&}}{text}")
            add(2, a, b, "Bridge", f"{{\\fad(800,800)\\fsp4}}{text}")
        elif k == "juara":
            for j, (tw, word) in enumerate(words):
                end = words[j + 1][0] if j + 1 < len(words) else b
                add(2, tw, end, "Title", f"{{\\an5\\pos(960,540)\\fs400\\fscx122\\fscy122\\t(0,150,\\fscx100\\fscy100)}}{word.upper()}")
        elif k in ("chant", "asia"):
            fs = 220 if k == "chant" else 280
            ups = [w.upper() for _, w in words]
            sp = text_w(" ", fs)
            widths = [text_w(u, fs) for u in ups]
            x = 960 - (sum(widths) + sp * (len(ups) - 1)) / 2
            for (tw, _), u, wd in zip(words, ups, widths):
                xc = x + wd / 2; x += wd + sp
                col = f"\\1c{c(GOLD)}\\4c{c(CHAR)}" if k == "asia" else ""
                add(2, tw, b, "Big", f"{{\\an5\\pos({xc:.0f},540)\\fs{fs}{col}\\fscx140\\fscy140\\t(0,120,\\fscx100\\fscy100)\\fad(0,200)}}{u}")
    path.write_text("\n".join(head + ev) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="t_from", type=float, default=0.0)
    ap.add_argument("--to", dest="t_to", type=float, default=SONG_END)
    ap.add_argument("--name", default="JUARA_lyric_video")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--jobs", type=int, default=3)
    args = ap.parse_args()
    WORK.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
    g0, g1 = round(args.t_from * FPS), round(args.t_to * FPS)
    jobs = []
    for i, s in enumerate(SEGMENTS):
        f0, f1 = max(round(s["t0"] * FPS), g0), min(round(s["t1"] * FPS), g1)
        if f1 > f0: jobs.append((i, s, f0, f1))
    with ProcessPoolExecutor(args.jobs) as ex:
        parts = list(ex.map(render_seg, jobs))
    lst = WORK / f"{args.name}_list.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    ass = WORK / "lyrics.ass"; build_ass(ass)
    out = OUT / f"{args.name}.mp4"
    t0 = g0 / FPS; dur = (g1 - g0) / FPS
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", str(SONG),
                    "-vf", f"setpts=PTS-STARTPTS+{t0}/TB,subtitles={ass}:fontsdir={FONT.parent},setpts=PTS-STARTPTS",
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", str(args.crf), "-pix_fmt", "yuv420p",
                    "-r", str(FPS), "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", str(out)], check=True)
    print(out)

if __name__ == "__main__":
    main()
