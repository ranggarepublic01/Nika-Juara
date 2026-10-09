"""Build the JUARA! illustrated lyric video plan page and the on-screen lyric SRT.

Reads the final Suno LRC, writes:
  claude/juara-lyric-video/juara-lyric-video.html
  lyrics/JUARA_lyric-video.srt
Run from the repo root: python3 claude/juara-lyric-video/build_lyric_video.py
"""
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LRC = ROOT / "lyrics/JUARA_final_suno.lrc"
OUT_HTML = ROOT / "claude/juara-lyric-video/juara-lyric-video.html"
OUT_SRT = ROOT / "lyrics/JUARA_lyric-video.srt"
SONG_END = 357.56

# ---------- LRC ----------
def secs(ts):
    m, s = ts.split(":")
    return int(m) * 60 + float(s)

LINES = []  # [(start, [(t, word), ...])]
for raw in LRC.read_text(encoding="utf-8").splitlines():
    m = re.match(r"\[(\d+:\d+\.\d+)\](.*)", raw.strip())
    if not m:
        continue
    words = [(secs(t), w.strip()) for t, w in re.findall(r"<(\d+:\d+\.\d+)>([^<]*)", m.group(2))]
    LINES.append((secs(m.group(1)), words))

# On-screen spelling fixes (LRC line number, 1-based -> text). Suno phonetics stay out of the video.
FIX = {10: "entah kapan tiba...", 11: "Senin malam, GBK penuh lagi"}

# Line style per LRC line number
def kind(n):
    if n == 1: return "hidden"
    if n in (2, 3, 19, 20, 21, 22, 33, 34, 35, 36, 49, 50): return "chant"
    if n in (4, 15, 17, 29, 31, 41, 43, 45, 47): return "juara"
    if n in (5, 16, 18, 30, 32, 42, 44, 46, 48): return "chorus"
    if 6 <= n <= 10: return "flashback"
    if 37 <= n <= 40: return "bridge"
    if n in (51, 52): return "asia"
    return "verse"

LEAD = 0.20   # text appears this long before the first sung word
HOLD = {"verse": 1.6, "flashback": 1.6, "chorus": 1.4, "juara": 1.0, "chant": 1.0, "bridge": 2.2, "asia": 1.6}

CUES = []  # (n, in, out, text, kind, words)
for i, (st, words) in enumerate(LINES):
    n = i + 1
    k = kind(n)
    if k == "hidden":
        continue
    text = FIX.get(n, " ".join(w for _, w in words))
    t_in = max(0.0, words[0][0] - LEAD)
    nxt = LINES[i + 1][1][0][0] - LEAD if i + 1 < len(LINES) else SONG_END
    hold = 3.0 if n == len(LINES) else HOLD[k]
    t_out = min(nxt - 0.05, words[-1][0] + hold)
    CUES.append((n, t_in, t_out, text, k, words))

def srt_ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

OUT_SRT.write_text("\n".join(f"{j}\n{srt_ts(a)} --> {srt_ts(b)}\n{t}\n" for j, (_, a, b, t, _, _) in enumerate(CUES, 1)), encoding="utf-8")

def fmt(t):
    m = int(t // 60); s = t - 60 * m
    return f"{m}:{s:04.1f}"

# ---------- Art direction ----------
STYLE = ("Bold Indonesian screen-printed poster and hand-painted street-mural illustration: flat simplified shapes with confident "
 "hand-cut edges, a strict limited palette of flag red, warm off-white, deep night indigo, charcoal black and small touches of gold, "
 "visible halftone dots, dry-brush texture and rough paper grain, light drawn as flat bright shapes and rays, strong silhouettes, "
 "people drawn with simplified but expressive faces. Not photorealistic, not a 3D render, not anime. Landscape 16:9. "
 "Do not draw any words, titles, lyrics, numbers, logos, crests, badges, emblems, watermarks or captions; the only lettering "
 "allowed is the word INDONESIA on the scarf and the number 12 on the son's jersey.")
COMPOSE = ("Keep the main subject inside the centre third of the width. Keep a calm, darker band across the lower middle of the "
 "frame (from about 55% to 85% of the height) with no faces or important detail, for big lyric text.")

L = {
 "SON": "the son: an Indonesian man about 28 years old, slim athletic build, warm brown skin, short black hair cut close at the sides, clean-shaven, a small dark mole under his left eye, wearing a plain bright red football supporter jersey with a white V-neck collar and white sleeve cuffs, a small white number 12 on the front left chest and a large white number 12 on the back, no logo and no other text, and black jeans",
 "SON_PAST": "the son one year earlier: the same Indonesian man about 28 years old, short black hair, a small dark mole under his left eye, wearing a plain grey T-shirt and black jeans",
 "BAPAK": "Bapak: an Indonesian man about 62 years old, slim, warm brown weathered skin, short grey hair thinning at the front, a neat grey moustache, deep smile lines, thin black-rimmed glasses, wearing a faded light-blue short-sleeved button shirt over a white undershirt and dark grey trousers",
 "SCARF": "the red scarf: an old knitted football supporter scarf in deep flag red, slightly faded, with the word INDONESIA knitted in bold white block capitals along its length, a white band with two thin red stripes near each end, and white tassels, no logos",
 "NEIGH": "kampung neighbours: ordinary Indonesian residents of mixed ages in everyday clothes, men in T-shirts and sarongs, two women in headscarves, a few children, some with plain red-and-white accessories",
}
GBK = {
 "GBK_EXT": "Gelora Bung Karno Main Stadium in Jakarta, matching the attached photo: a wide, low oval bowl under one continuous ring-shaped roof made of many narrow radial ribbed panels in pale silver-grey that slope gently outward to a thin overhanging edge, leaving a large open oval in the centre lined with a white steel lattice ring; under the roof edge, a facade of slim white concrete columns in a repeating pattern of diagonal V-shaped braces over four horizontal floor bands, with dark openings between them; a wide paved plaza around the bowl with tall lamp posts topped by ring-shaped lamps; dense tropical trees around the plaza; a tight cluster of tall glass office towers of the Sudirman business district standing directly behind the stadium",
 "GBK_IN": "inside Gelora Bung Karno Main Stadium, matching the attached photo: a steep oval bowl with two tiers of seats laid out in big blocks of red, white and grey that form a red-and-white flag pattern around the bowl; a red-orange athletics running track with white lane lines circling a bright striped green pitch; the underside of the ring roof showing a web of radial steel trusses, with a white steel lattice ring and floodlights along its inner edge; the open oval in the centre of the roof showing the sky, with a few tall towers rising beyond the far rim",
}
GBK_NAMES = {"GBK_EXT": "GBK outside (with photo 1)", "GBK_IN": "GBK inside (with photo 2)"}
PHOTO_NOTE = "The attached photo of the stadium is only an architecture reference: copy its shape and structure, not its daylight, colours or photographic look; it is night in this artwork."

NAMES = {"SON": "Son", "SON_PAST": "Son (one year earlier)", "BAPAK": "Bapak", "SCARF": "Red scarf", "NEIGH": "Neighbours"}
SHORT = {"SON": "the son", "SON_PAST": "the son one year earlier", "BAPAK": "Bapak", "SCARF": "the red scarf", "NEIGH": "kampung neighbours"}

def expand(t):
    for k, v in L.items():
        d = v.split(": ", 1)[1]
        t = t.replace("{" + k + "}", f"{SHORT[k]} ({d})")
    for k, v in GBK.items():
        t = t.replace("{" + k + "}", v)
    return t

SHEET = ("Character reference sheet on a plain warm off-white paper background, in the illustration style described below, no text labels: "
 "left, " + L["SON"] + ", full body front view and back view, wearing " + L["SCARF"] + " around his neck; "
 "centre-left, " + L["SON_PAST"] + ", full body front view; "
 "centre-right, " + L["BAPAK"] + ", full body front view and a head-and-shoulders close-up; "
 "right, " + L["SCARF"] + ", laid flat. " + STYLE)

LOOK_PAST = "Palette for this artwork only: cold blue-grey and indigo, everything desaturated, the red scarf the only warm colour in the frame."

PREFIX_CH = "Match all characters exactly to the attached character sheet, and match the illustration style, palette and texture of the attached style reference exactly."
PREFIX_ST = "Match the illustration style, palette and texture of the attached style reference exactly."
VEO_END = " One continuous shot with no cuts. Keep the illustration style, characters and setting exactly as in the first frame; do not add buildings, roofs or stands. No text appears. Nobody sings or lip-syncs."

# Artworks: id, title, chars, attach, body, extra look, veo motion, note
ART = [
 ("A1", "Garuda over the ring", [], "GBK photo 1 (aerial, outside)",
  "Redraw the stadium in the attached photo in the illustration style below, from the same raised viewpoint to one side, at night. {GBK_EXT}. The open oval in the centre glows red and white from the floodlights inside; red flare smoke rises out of it and curls upward into the wings of a huge stylised Garuda eagle that spreads across the night sky above the stadium, in front of the towers. The eagle is built from flat red, gold and white shapes, facing left, beak open; it is a mythical bird, not the national coat of arms: no shield on its chest, no emblem, no banner. The towers are flat indigo silhouettes with a few lit windows. The facade glows softly but stays darker than the roof and the sky; the plaza and trees below are in deep shadow, dotted with tiny supporters in red.",
  "", "The red smoke drifts slowly upward and the eagle's wing tips ripple gently; floodlight rays pulse softly. The camera holds still.",
  "Style anchor. Make this one first; it is attached to every artwork after it. Check the roof: radial ribs, thin outer edge, open oval centre, towers directly behind."),
 ("A2", "Wall of scarves", ["SON", "SCARF"], "Character sheet + A1 + GBK photo 2 (inside the bowl)",
  "High in the upper tier at night, the camera just behind and above the supporters, looking down across their backs toward the pitch and the far stand, {GBK_IN}. Rows of supporters in red and white seen from behind, every one holding a red-and-white scarf stretched taut above their head with both arms; the far stand is packed and its scarves are raised too; the floodlights on the roof's inner edge are drawn as white starbursts and the sky through the open oval is dark night; red flare smoke in flat curling shapes. In the nearest row, in the centre of the frame, {SON} is seen from behind holding {SCARF} up in both fists, the large 12 on his back. No face is visible; everyone faces the pitch.",
  "", "The raised scarves pump up and down together; flare smoke drifts. The camera holds still.",
  "Used twice: the opening chant and the post-chorus chant. Check the red-orange track around the pitch and the red, white and grey seat blocks."),
 ("A3", "The walk to GBK", ["SON", "SCARF"], "Character sheet + A1 + GBK photo 1 (aerial, outside)",
  "At ground level on the wide stadium plaza at night, the camera a few steps behind {SON}, who walks away from us toward the glowing stadium, {SCARF} around his neck with its ends hanging down his back, the large 12 on his back; around him a river of supporters in red and white walks the same way, some carrying a huge plain red-and-white flag between them, some raising fists. Ahead, the stadium from the attached photo seen from the plaza at ground level: the facade of slim white concrete columns with diagonal V-shaped braces over four floor bands, lit warm white from within; the pale ribbed ring roof overhanging above it with its thin edge, red smoke rising from the open centre into the night sky; tall lamp posts with ring-shaped lamps and dark tropical trees along the plaza; the Sudirman towers rising behind the roof as indigo silhouettes.",
  "", "The supporters walk slowly forward and the big flag ripples; the camera follows at walking pace at the same height and does not rise or tilt.",
  "Carries the 49-second instrumental, so it gets two camera moves in the edit. Check the V-braced columns under the roof edge."),
 ("A4", "A year ago", ["BAPAK", "SON_PAST", "SCARF"], "Character sheet + A1",
  "Night in heavy rain, inside a small roadside warung kopi on a narrow Jakarta kampung street, the camera at the back wall beside the switched-off TV, looking out toward the open front and the street: {BAPAK} sits on the front wooden bench facing us, slowly folding {SCARF} on his lap, the INDONESIA lettering showing on the fold, his eyes on the scarf; beside him {SON_PAST} sits with his head lowered and his elbows on his knees. Behind them the blue tarpaulin awning streams with rain and the wet street shines under one street lamp. The wooden counter with glass jars of snacks runs along the left side; one white fluorescent tube hangs under the awning; the dark side edge of the TV on its shelf is just visible at the far left edge of the frame.",
  LOOK_PAST, "Rain streams off the awning; Bapak's hands slowly fold the scarf once more. The camera holds still.",
  "Flashback. Used twice: verse 1 and the start of the bridge."),
 ("A5", "The same scarf", ["SON", "SCARF"], "Character sheet + A1",
  "{SON} stands in his row in the packed stand facing us, holding {SCARF} stretched between his fists high above his head, the INDONESIA lettering facing us, his eyes lifted to it, jaw set. Behind him the rows of the stand rise away as flat abstract shapes: red, white and grey seat blocks, red and white supporters and warm red flare glow, with no readable architecture. A few supporters at the edges of the frame, cut off and simplified, look the same way he does.",
  "", "The scarf trembles slightly in his fists; the flare glow behind him flickers. The camera holds still.",
  "Pre-chorus. The edit builds tension on it, then breaks on \"meledak\"."),
 ("A6", "JUARA!", ["SON", "SCARF"], "Character sheet + A1",
  "{SON} mid-jump in the stand facing us, mouth wide open in a shout of joy, his right fist thumped against his chest over the small 12, his left fist raised high swinging {SCARF}; around him supporters leap with arms up, simplified and partly cut off by the frame, against flat blocks of red, white and grey seats; above them in the night sky at the top of the frame, fireworks burst in flat red and gold starbursts and red-and-white confetti falls.",
  "", "Confetti falls and fireworks burst in the sky; the scarf swings. The camera holds still.",
  "First chorus. The chest thump sits on \"Garuda di dada\"."),
 ("A7", "The warung erupts", ["BAPAK", "NEIGH"], "Character sheet + A1 + A4",
  "Match the warung's layout to the attached A4 image (the same warung, now on a dry night in warm light; ignore A4's cold blue colours). Night inside the same warung kopi, the camera at the back wall beside the TV, looking out toward the open front and the dry street: {BAPAK} and {NEIGH} leap up in front of the wooden benches with both arms in the air, faces lit by the TV's glow from the left of the frame, eyes on the TV just beside the camera; Bapak laughs with his glasses slipping down his nose; a red plastic stool tips over; coffee glasses on the counter on the left. Warm fluorescent light under the blue tarpaulin awning, motorbikes parked at the street edge. Bapak has no scarf: his son has it at the stadium.",
  "Palette for this artwork: warm night, the same limited palette, warm TV glow on the faces.",
  "Everyone jumps and cheers; the stool rocks. The camera holds still.",
  "A4 is attached only for the room layout; A1 sets the style. Covers pre-chorus 2 and chorus 2."),
 ("A8", "The ride home", ["SON", "SCARF"], "Character sheet + A1",
  "A wide Jakarta avenue at night lined with tall glass towers and trees, a pedestrian bridge crossing overhead behind: a convoy of motorbikes rides toward the camera, every rider in a helmet, some passengers waving plain red-and-white flags; in the middle of the convoy {SON} rides one motorbike in a helmet with the visor open, {SCARF} flying out behind him; fireworks burst in flat red and gold shapes in the sky between the towers; headlights drawn as flat white rays.",
  "", "The convoy rolls slowly toward the camera, flags waving, scarf flying; fireworks burst in the sky already in frame. The camera holds still.",
  "Ayo chant, guitar solo and piano breakdown. Everyone on a motorbike wears a helmet."),
 ("A9", "The scarf comes home", ["SON", "BAPAK", "SCARF"], "Character sheet + A1 + A4",
  "Match the warung's layout to the attached A4 image (the same warung, now on a dry night in warm light; ignore A4's cold blue colours). Night under the blue tarpaulin awning of the same warung, side-on medium two-shot: {SON} stands facing {BAPAK}, gently wrapping {SCARF} around his father's neck; Bapak's hands rise to touch it, his eyes wet behind his glasses, a small trembling smile; the son's helmet rests on the bench; his motorbike is parked at the street edge behind them. Warm fluorescent light, a quiet street, far-off fireworks in the sky above the rooftops.",
  "Palette for this artwork: warm and tender, the red scarf the brightest thing in the frame.",
  "The son finishes the wrap; Bapak's hands close over the scarf. The camera holds still.",
  "Emotional peak. From here on the scarf stays around Bapak's neck."),
 ("A10", "Kampung juara", ["SON", "BAPAK", "SCARF", "NEIGH"], "Character sheet + A1",
  "A narrow Jakarta kampung alley at night packed with {NEIGH} facing us, arms over each other's shoulders, a child on a man's shoulders waving a small plain red-and-white flag; in the centre {SON} and {BAPAK}, who wears {SCARF}, stand side by side raising their fists high together. Two-storey houses with clay-tiled roofs, small red-and-white bunting strung overhead, the warung's blue tarpaulin awning at the far end behind them. In the upper left, a big plain red-and-white flag on a tall bamboo pole flies above the rooftops; fireworks burst in the night sky.",
  "", "Everyone sways and jumps; the flag on the bamboo pole waves; fireworks burst. The camera holds still.",
  "Final chorus to the end card. The flag sits upper left so the outro can tilt up to it."),
]
ART_BY = {a[0]: a for a in ART}

def art_prompt(a):
    aid, title, chars, attach, body, look, veo, note = a
    pre = "" if aid == "A1" else (PREFIX_CH if chars else PREFIX_ST) + " "
    if "GBK photo" in attach:
        pre += PHOTO_NOTE + " "
    return pre + expand(body) + (" " + look if look else "") + " " + COMPOSE + " " + STYLE

# Edit timeline: (start, end, artwork, lyrics summary, move)
TL = [
 (0.0, 22.3, "A1", "Title · vocalise", "Push 100→112% toward the eagle's head. Red smoke overlay drifting up, soft floodlight flare. Title card 0:01.0–0:10.0."),
 (22.3, 35.7, "A2", "Ayo, ayo, Garuda! ×2 · Juara! Juara! · Garuda di dada", "Start at 105% framed on the son. 3% scale pulse on each \"Garuda!\" (0:23.7, 0:27.3) and each \"Juara!\" (0:29.7, 0:31.5); slow upward drift between pulses."),
 (35.7, 84.8, "A3", "(instrumental)", "Move 1, 0:35.7–1:00.0: push 100→115% toward the son. Move 2, 1:00.0–1:24.8: at 115%, slow pan up from the son to the glowing roof and smoke. Facade light flicker overlay. Optional credit card \"NIKA MUSIC · BANGKIT\" 0:40–0:48."),
 (84.8, 102.6, "A4", "Verse 1: Setahun lalu … entah kapan tiba", "Hard cut. Rain overlay. Start at 110% on both of them, push to 118% on Bapak's hands and the scarf by \"melipat syal merahnya\" (1:33.4)."),
 (102.6, 132.2, "A5", "Pre-chorus: Senin malam … Lalu meledak", "Push 100→115% until 1:57.0. 1:57.0–2:04.2: hold, vignette up, background softened (tension). On \"meledak\" (2:04.2): 2-frame white flash, jump to 120%, 4-frame shake, sparks/confetti overlay to 2:12.2."),
 (132.2, 146.7, "A6", "Chorus 1", "Punch scale 108→100% on each \"Juara!\" (2:12.2, 2:13.9, 2:19.4, 2:21.2). Confetti overlay, light flare."),
 (146.7, 175.6, "A2", "Ayo ×4 · angklung interlude", "Start tight at 125% on the son, 3% pulse on each \"Garuda!\" (2:28.1, 2:31.7, 2:35.2, 2:38.7). From 2:40 slow pull back to 100%, fireworks overlay."),
 (175.6, 189.7, "A1", "Verse 2: Gajah Perang … Langit Jakarta merah putih semua", "Start at 118% on the skyline side, slow pan across to the stadium and eagle, ending at 108%."),
 (189.7, 222.8, "A7", "Pre-chorus 2 · Chorus 2", "3:09.7–3:16.5: dark (exposure about −60%, desaturated, slight blur), slow push. On \"meledak\" (3:16.5): flash to full colour, shake. Pulses on each \"Juara!\" (3:28.0, 3:29.8, 3:35.1, 3:36.8); slow push toward Bapak on \"Bilang ke Bapak\" (3:38.6)."),
 (222.8, 266.2, "A8", "Ayo ×4 · guitar solo · piano breakdown", "At 112%, slow drift right to left with a light-streak overlay; pulses on each \"Garuda!\" (3:43.6, 3:47.2, 3:50.6, 3:54.2). When the drums drop out for the piano (around 4:16): slow push to 125% on the son, fireworks overlay fades out, colour cools slightly."),
 (266.2, 280.2, "A4", "Bridge: Untuk yang menangis … setia menunggu", "Hard cut back to the rain. Crop to Bapak and the folded scarf only (about 135%), push to 140%. Rain overlay."),
 (280.2, 298.5, "A9", "Bridge: Malam ini kita pulang … akhirnya bahagia", "Push 100→110%, warm glow bloom. Hold still from \"bahagia\" (4:53.0) to the cut."),
 (298.5, SONG_END, "A10", "Final chorus ×2 · Ayo · Asia, kami siap / datang · outro", "4:58.5–5:12.6 wide at 100%, pulses on each \"Juara!\". 5:12.6–5:27.3 at 115% on father and son, pulses. 5:27.3–5:39.0 ease back to 105%; hits on \"Asia\" (5:32.4, 5:36.1). 5:39.0–5:57.6 slow tilt up to the flag; dim to about 50% from 5:42 for the end card."),
]

def art_uses(aid):
    return [(s, e) for s, e, a, _, _ in TL if a == aid]

# ---------- HTML ----------
def esc(s): return html.escape(s, quote=True)
cid = 0
def copyblock(kind, label, text):
    global cid; cid += 1
    return (f'<div class="pr {kind}"><div class="prh"><span class="prl">{esc(label)}</span>'
            f'<button class="cp" type="button" data-t="c{cid}">Copy</button></div><pre id="c{cid}">{esc(text)}</pre></div>')

cards = []
for a in ART:
    aid, title, chars, attach, body, look, veo, note = a
    uses = art_uses(aid)
    use_txt = " · ".join(f"{fmt(s)} – {fmt(e)}" for s, e in uses)
    total = sum(e - s for s, e in uses)
    who = ", ".join(NAMES[c] for c in chars) if chars else "none"
    lyr = " / ".join(t[3] for t in TL if t[2] == aid)
    past = " look-past" if look == LOOK_PAST else ""
    attach_html = " + ".join(f"<b>{esc(x.strip())}</b>" for x in attach.split("+"))
    order = " — character sheet first" if chars else ""
    if "GBK photo" in attach and chars: order = " — character sheet, then A1 (style), then the GBK photo (architecture)"
    if "A4" in attach: order = " — character sheet, then A1 (style), then A4 (room)"
    cards.append(f'''<article class="sc{past}" id="{aid.lower()}">
<header class="sch"><span class="badge">{aid}</span><h3>{esc(title)}</h3><span class="dur">{total:.1f}s on screen</span></header>
<p class="lyr">{esc(lyr)}</p>
<dl class="meta"><div><dt>On screen</dt><dd>{esc(use_txt)}</dd></div><div><dt>Characters</dt><dd>{esc(who)}</dd></div></dl>
<div class="attach"><span class="al">Attach</span><span>{attach_html}{order}</span></div>
{copyblock("img", "Gemini image prompt", art_prompt(a))}
<details class="veo"><summary>Optional Veo motion prompt</summary>{copyblock("vid", "Veo prompt (first frame = this artwork)", veo + VEO_END)}</details>
<p class="note">{esc(note)}</p>
</article>''')

rows = []
for s, e, a, lyr, move in TL:
    rows.append(f'<tr><td class="tcell">{fmt(s)} – {fmt(e)}</td><td class="num">{e - s:.1f}s</td>'
                f'<td><a href="#{a.lower()}">{a}</a> {esc(ART_BY[a][1])}</td><td class="wrapcell">{esc(lyr)}</td><td class="wrapcell">{esc(move)}</td></tr>')

KIND_NAME = {"chant": "Chant", "juara": "JUARA", "chorus": "Chorus line", "flashback": "Verse (flashback)", "bridge": "Bridge", "asia": "Asia", "verse": "Verse"}
lrows = []
for j, (n, a, b, t, k, words) in enumerate(CUES, 1):
    wt = " · ".join(f"{esc(w)} <span class=\"wt\">{fmt(tw)}</span>" for tw, w in words) if k in ("chant", "juara", "asia") else ""
    lrows.append(f'<tr><td class="num">{j}</td><td class="tcell">{fmt(a)}</td><td class="tcell">{fmt(b)}</td>'
                 f'<td><span class="k k-{k}">{KIND_NAME[k]}</span></td><td class="wrapcell">{esc(t)}</td><td class="wrapcell cues">{wt}</td></tr>')

cons = "\n".join(copyblock("con", NAMES[k], L[k]) for k in L)
gbk = "\n".join(copyblock("con", GBK_NAMES[k], v) for k, v in GBK.items())

page = (Path(__file__).with_name("lyric_template.html").read_text(encoding="utf-8")
  .replace("%%STYLE%%", copyblock("con", "Style line (already inside every prompt)", STYLE))
  .replace("%%COMPOSE%%", copyblock("con", "Composition line (already inside every prompt)", COMPOSE))
  .replace("%%SHEET%%", copyblock("plate", "Character sheet (illustrated)", SHEET))
  .replace("%%CONS%%", cons)
  .replace("%%GBK%%", gbk)
  .replace("%%CARDS%%", "\n".join(cards))
  .replace("%%ROWS%%", "\n".join(rows))
  .replace("%%LROWS%%", "\n".join(lrows))
  .replace("%%NCUES%%", str(len(CUES))))
OUT_HTML.write_text(page, encoding="utf-8")

# sanity: timeline is continuous and covers the song
for (s1, e1, *_), (s2, *_) in zip(TL, TL[1:]):
    assert abs(e1 - s2) < 1e-6, (e1, s2)
assert TL[0][0] == 0 and TL[-1][1] == SONG_END
for _, a, b, *_ in CUES:
    assert b > a, (a, b)
print(len(ART), "artworks,", len(TL), "segments,", len(CUES), "lyric cues,", len(page), "bytes")
