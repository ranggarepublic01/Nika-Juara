"""Render the vertical (9:16) Shorts / TikTok cuts of the JUARA! lyric video.

Reuses the main renderer's frame drawing (render.py) at 1080x1920 with vertical framing,
and lays the lyrics out for phone screens, clear of the YouTube Shorts and TikTok buttons.

  python3 edit/shorts.py            # all six -> edit/out/shorts/JUARA_short_N.mp4
  python3 edit/shorts.py 2 5        # only Shorts 2 and 5
"""
import subprocess, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import render as R

R.W, R.H = 1080, 1920
R.WORK = R.EDIT / "work" / "shorts"
OUTDIR = R.OUT / "shorts"
W, H, FPS = R.W, R.H, R.FPS

# (number, start, end, hook line)
SHORTS = [
 (1, 14.0, 35.6, "INDONESIA JUARA ASEAN 2026!"),
 (2, 84.8, 132.1, "Setahun lalu, TV-nya kita matikan..."),
 (3, 123.6, 161.0, "Detik terakhir di GBK..."),
 (4, 175.6, 222.6, "Sementara itu, di warung kampung..."),
 (5, 266.2, 312.4, "Syal merah Bapak akhirnya pulang"),
 (6, 312.4, 346.0, "Berikutnya: Piala Asia 2027"),
]
CTA = "Lagu lengkap di channel Nika Music"

# vertical framing: where the subject sits in each artwork (x, y as 0..1 of the image)
FOCUS = {"A1": (.49, .45), "A2": (.50, .55), "A4": (.46, .50), "A5": (.50, .45), "A6": (.57, .42),
         "A7": (.52, .45), "A9": (.56, .50), "A10": (.50, .50)}

def vertical_segments(t0, t1):
    out = []
    for s in R.SEGMENTS:
        a, b = max(s["t0"], t0), min(s["t1"], t1)
        if b <= a: continue
        assert s["kind"] == "still", f"Short {t0}-{t1} would include clip {s['src']}"
        fx, fy = FOCUS[s["src"]]
        v = dict(s)
        z_end = 1.10 if s["src"] in ("A4", "A9") else 1.06  # the quiet scenes push in a bit more
        v["keys"] = [(s["t0"], 1.00, fx, fy), (s["t1"], z_end, fx, fy)]
        out.append(v)
    return out

# ---------------------------------------------------------------- vertical lyrics
c, ats, text_w = R.c, R.ats, R.text_w
OFF, GOLD, RED, CHAR, BLUE = R.OFF, R.GOLD, R.RED, R.CHAR, R.BLUE
SAFE_W = 860  # usable text width: margins 70 left, 150 right (TikTok / Shorts buttons)
CX = 70 + SAFE_W / 2

def build_ass_v(path, s0, s1, hook):
    st = [
     ("Verse", 108, OFF, OFF, CHAR, CHAR, 7, 0, 2, 560),
     ("Chorus", 140, OFF, OFF, CHAR, CHAR, 8, 0, 2, 600),
     ("Big", 170, OFF, OFF, CHAR, RED, 7, 9, 5, 0),
     ("Bridge", 96, OFF, OFF, OFF, CHAR, 0, 0, 2, 560),
     ("Title", 300, RED, RED, OFF, CHAR, 11, 11, 5, 0),
     ("Hook", 88, OFF, OFF, RED, CHAR, 20, 0, 8, 290),
    ]
    head = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "ScaledBorderAndShadow: yes", "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"]
    for name, fs, p1, p2, oc, bc, ol, sh, al, mv in st:
        bs = 3 if name == "Hook" else 1  # the hook sits on a solid red box
        head.append(f"Style: {name},Anton,{fs},{c(p1)},{c(p2)},{c(oc)},{c(bc)},0,0,0,0,100,100,0,0,{bs},{ol},{sh},{al},70,150,{mv},1")
    ev = ["", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    def add(layer, a, b, style, text):
        a, b = max(a, s0), min(b, s1)
        if b - a > 0.05: ev.append(f"Dialogue: {layer},{ats(a - s0)},{ats(b - s0)},{style},,0,0,0,,{text}")

    # soft gradient behind the lower text area (y 1000..1500), same strip method as the main video
    NS, Y0, Y1 = 30, 980, 1560
    for k in range(NS):
        ya, yb = Y0 + (Y1 - Y0) * k / NS, Y0 + (Y1 - Y0) * (k + 1) / NS + 1
        mid = 1 - abs((k + 0.5) / NS - 0.5) * 2  # strongest in the middle of the band
        alpha = 255 - round(255 * 0.45 * R.ease(mid * 1.6))
        add(0, s0, s1, "Verse", f"{{\\an7\\pos(0,0)\\p1\\bord0\\shad0\\1c{c(CHAR)}\\1a&H{alpha:02X}&}}m 0 {ya:.0f} l {W} {ya:.0f} l {W} {yb:.0f} l 0 {yb:.0f}{{\\p0}}")

    for n, a, b, k, words in R.CUES:
        if b <= s0 or a >= s1: continue
        if k in ("verse", "flashback", "chorus"):
            style = "Chorus" if k == "chorus" else "Verse"
            if k == "flashback": pre = f"{{\\fad(400,400)\\1c{c(BLUE)}}}"
            elif k == "chorus": pre = f"{{\\fad(150,150)\\1c{c(GOLD)}\\fscx110\\fscy110\\t(0,150,\\fscx100\\fscy100)}}"
            else: pre = f"{{\\fad(250,200)\\1c{c(GOLD)}}}"
            parts = [pre, f"{{\\k{max(0, round((words[0][0] - max(a, s0)) * 100))}}}"]
            for j, (tw, word) in enumerate(words):
                nxt = words[j + 1][0] if j + 1 < len(words) else min(b, tw + 0.9)
                dur = max(1, round((nxt - max(tw, s0)) * 100)) if nxt > s0 else 1
                if k == "chorus" and word.lower().strip("!,.") in ("juara", "bapak"):
                    parts.append(f"{{\\kf{dur}\\2c{c(GOLD)}}}{word}{{\\2c{c(OFF)}}} ")
                else:
                    parts.append(f"{{\\kf{dur}}}{word} ")
            add(1, a, b, style, "".join(parts).rstrip())
        elif k == "bridge":
            text = " ".join(w for _, w in words)
            add(1, a, b, "Bridge", f"{{\\fad(800,800)\\fsp3\\bord7\\blur9\\3c{c(OFF)}\\3a&HA0&\\1a&HFF&}}{text}")
            add(2, a, b, "Bridge", f"{{\\fad(800,800)\\fsp3}}{text}")
        elif k == "juara":
            for j, (tw, word) in enumerate(words):
                end = words[j + 1][0] if j + 1 < len(words) else b
                add(2, tw, end, "Title", f"{{\\an5\\pos({CX:.0f},900)\\fscx122\\fscy122\\t(0,150,\\fscx100\\fscy100)}}{word.upper()}")
        elif k in ("chant", "asia"):
            # one word per row, stacked, so it stays big on a narrow screen
            fs = 190 if k == "chant" else 200
            ups = [w.upper() for _, w in words]
            y = 1200 - (len(ups) - 1) * fs * 0.55  # below the faces and the scarf
            col = f"\\1c{c(GOLD)}\\4c{c(CHAR)}" if k == "asia" else ""
            for (tw, _), u in zip(words, ups):
                f = fs * min(1.0, SAFE_W / text_w(u, fs))
                add(2, tw, b, "Big", f"{{\\an5\\pos({CX:.0f},{y:.0f})\\fs{f:.0f}{col}\\fscx140\\fscy140\\t(0,120,\\fscx100\\fscy100)\\fad(0,200)}}{u}")
                y += fs * 1.1

    add(3, s0 + 0.15, s0 + 3.6, "Hook", f"{{\\fad(150,300)}}{hook}")
    add(3, s1 - 3.0, s1, "Hook", f"{{\\fad(300,0)\\fs72}}{CTA}")
    path.write_text("\n".join(head + ev) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- render
def render_short(num, s0, s1, hook):
    g0, g1 = round(s0 * FPS), round(s1 * FPS)
    jobs = [(i, s, max(round(s["t0"] * FPS), g0), min(round(s["t1"] * FPS), g1)) for i, s in enumerate(vertical_segments(s0, s1))]
    jobs = [(num * 100 + i, s, a, b) for i, s, a, b in jobs if b > a]
    with ProcessPoolExecutor(3) as ex:
        parts = list(ex.map(R.render_seg, jobs))
    lst = R.WORK / f"short{num}_list.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    ass = R.WORK / f"short{num}.ass"
    build_ass_v(ass, g0 / FPS, g1 / FPS, hook)
    out = OUTDIR / f"JUARA_short_{num}.mp4"
    dur = (g1 - g0) / FPS
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-ss", f"{g0 / FPS:.3f}", "-t", f"{dur:.3f}", "-i", str(R.SONG),
                    "-vf", f"subtitles={ass}:fontsdir={R.FONT.parent},fade=t=out:st={dur - 0.6:.2f}:d=0.6",
                    "-af", f"afade=t=in:d=0.25,afade=t=out:st={dur - 1.2:.2f}:d=1.2",
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(out)], check=True)
    return out

def main():
    R.WORK.mkdir(parents=True, exist_ok=True); OUTDIR.mkdir(parents=True, exist_ok=True)
    pick = {int(a) for a in sys.argv[1:]}
    for num, s0, s1, hook in SHORTS:
        if pick and num not in pick: continue
        print(render_short(num, s0, s1, hook), flush=True)

if __name__ == "__main__":
    main()
