import html, json

# ---------- Consistency lines ----------
L = {
 "SON": "the son: an Indonesian man about 28 years old, slim athletic build, warm brown skin, short black hair cut close at the sides, clean-shaven, dark brown eyes, a small dark mole under his left eye, wearing a replica Indonesia home supporter jersey: bright red with a white crossover V-neck collar, white sleeve cuffs and white horizontal brush-stroke streaks sweeping across the front below the chest, a small white number 12 on the front left chest only, a large white number 12 on the back, no logo, no crest and no other text; and black jeans",
 "SON_PAST": "the son one year earlier: the same Indonesian man about 28 years old, slim athletic build, warm brown skin, short black hair cut close at the sides, clean-shaven, dark brown eyes, a small dark mole under his left eye, wearing a plain grey T-shirt and black jeans",
 "BAPAK": "Bapak: an Indonesian man about 62 years old, slim, warm brown weathered skin, short grey hair thinning at the front, a neat grey moustache, deep smile lines, thin black-rimmed glasses, wearing a faded light-blue short-sleeved button shirt over a white undershirt and dark grey trousers",
 "SCARF": "the red scarf: an old knitted football supporter scarf in deep Indonesian flag red, slightly faded with age, with the word INDONESIA knitted in bold white block capital letters along its length, a white band with two thin red stripes near each end, and white tassels, no logos",
 "PLAYERS": "football players seen only from behind or as backlit silhouettes, faces never visible, wearing the red home kit: a bright red shirt with a white crossover V-neck collar, white sleeve cuffs, white horizontal brush-stroke streaks sweeping across the front of the shirt below the chest and a thin white horizontal stripe across the lower back, white shorts and red socks; no logos, no crests, no badges, no names and no numbers",
 "OPP": "opposing players seen only from behind or as backlit silhouettes, faces never visible, wearing plain dark-blue kits with no logos, no crests, no names and no numbers",
 "TROPHY": "a generic golden two-handled cup trophy with no text and no logos",
 "NEIGH": "kampung neighbours: a handful of ordinary Indonesian residents of mixed ages in everyday clothes, men in T-shirts and sarongs, two women in headscarves, a few children, some wearing plain red-and-white accessories",
}
CHAR_NAMES = {"SON":"Son (present)","SON_PAST":"Son (one year earlier)","BAPAK":"Bapak","SCARF":"Red scarf (key object)","PLAYERS":"Players (red)","OPP":"Opponents (blue)","TROPHY":"Trophy","NEIGH":"Neighbours"}

E = {
 "GBK_EXT": "Gelora Bung Karno Main Stadium in Jakarta: a huge oval stadium crowned by one continuous ring-shaped roof canopy that circles the whole bowl and leaves the centre open to the sky, the roof's inner edge lined with bright floodlights; the outside of the bowl wrapped in tall slim vertical white facade panels lit from within; a wide paved plaza with tall trees and lamp posts around it; the glass office towers of the Sudirman skyline behind it",
 "GBK_BOWL": "inside Gelora Bung Karno Main Stadium: a vast oval bowl of steep two-tier stands packed with supporters dressed in red and white, the seats in red, white and grey forming a huge wrapped red-and-white flag pattern around the bowl, one continuous ring-shaped roof canopy overhead with bright LED floodlights along its inner edge, the open centre of the roof showing the night sky, an athletics running track between the stands and a bright green pitch, drifting red flare smoke",
 "GBK_UP": "inside Gelora Bung Karno Main Stadium, in the steep stands: rows of red, white and grey seats packed with supporters dressed in red and white, rising toward one continuous ring-shaped roof canopy with bright LED floodlights along its inner edge, the night sky through the open centre of the roof, drifting red flare smoke",
 "TUNNEL": "the players' tunnel at Gelora Bung Karno: a wide concrete tunnel with smooth grey walls and a single line of white strip lights along the ceiling, opening at the far end onto the bright floodlit pitch and the packed red-and-white stands",
 "WARUNG": "a small roadside warung kopi on a narrow Jakarta kampung street, open to the street at the front under a blue tarpaulin awning: a wooden counter along the right side with glass jars of snacks and strips of plain unbranded coffee sachets hanging above it; a small flat-screen TV on a high wooden shelf on the back wall at the left; two long wooden benches in the middle facing the back wall and the TV, with their backs to the street; a few red plastic stools; one white fluorescent tube light under the awning; the back wall painted pale green with a faded wall calendar; potted plants and parked motorbikes at the street edge",
 "ALLEY": "a narrow Jakarta kampung alley: two-storey houses with clay-tiled roofs and walls painted in pale colours, potted plants by the doors, small red-and-white bunting strung overhead, a concrete gutter along the right side, one street lamp, the warung's blue tarpaulin awning visible at the far end",
 "STREET": "a wide Jakarta avenue at night lined with tall glass office towers and trees, tall street lights and a pedestrian bridge crossing overhead",
}
ENV_NAMES = {"GBK_UP":"GBK stands, looking up","GBK_EXT":"GBK exterior","GBK_BOWL":"GBK stands (bowl)","TUNNEL":"GBK players' tunnel","WARUNG":"Warung kopi","ALLEY":"Kampung alley","STREET":"Jakarta avenue"}

LOOK = {
 "NOW": "Present night: warm, saturated light with strong red and white accents.",
 "PAST": "One year earlier: cold, desaturated blue-grey grade, heavy rain, wet surfaces; the scarf is the only red in the frame.",
 "DAWN": "Dawn: soft golden sunrise light, calm and clear.",
}
STYLE = "Photorealistic cinematic film still, natural skin texture, shallow depth of field, anamorphic lens look, subtle film grain, landscape 16:9 composition, no logos, no watermarks, no captions; the only lettering allowed is the word INDONESIA on the scarf and the number 12 on the son's jersey."
VEND = "Keep all movement natural and realistic. Players' faces are never visible. Nobody sings or lip-syncs."

# plates: id -> (name, location key, view phrase, prompt extra)
PLATES = [
 ("P1","GBK exterior A — aerial, night","GBK_EXT","Aerial view from above and to one side at night,","the stadium glowing red and white from inside, the plaza busy with tiny figures. No people close to camera."),
 ("P2","GBK exterior B — plaza, night","GBK_EXT","At ground level on the plaza at night, facing the stadium facade,","lamp posts and trees framing the shot, the plaza empty."),
 ("P3","GBK exterior C — aerial, dawn","GBK_EXT","Aerial view from above and to one side at dawn,","the stadium empty and quiet, golden sunrise light on the ring roof, the Sudirman towers catching the light."),
 ("P4","GBK stands A — inside the crowd","GBK_BOWL","View A — inside the supporters' stand, high up in the middle of the steep rows of red, white and grey seats, surrounded on every side by other supporters standing close together; the pitch is far below and only visible in the distance; no running track, advertising boards or pitch-side area near the camera,","the nearest rows of seats empty for this plate, the rest of the bowl full."),
 ("P5","GBK stands B — wide from upper tier","GBK_BOWL","View B — wide view across the bowl from high in the upper tier, showing the far stand, the pitch and the whole ring roof,",""),
 ("P6","GBK stands C — pitch level, centre","GBK_BOWL","View C — standing on the grass near the centre circle at pitch level, looking across the pitch toward the far stand,","the far touchline lined with plain dark LED boards showing no text, the athletics track behind them, the stand rising beyond; open grass in the foreground with no stairs, benches, tunnel or equipment."),
 ("P7","GBK tunnel","TUNNEL","Looking down the tunnel toward the pitch from inside,","the tunnel empty."),
 ("P8","Warung A — from the street (present)","WARUNG","View A — from the street looking into the warung, the benches in the middle with their backs to the camera, the TV on the back wall at upper left,","at night, dry street, warm light, nobody present."),
 ("P9","Warung A — rain (one year earlier)","WARUNG","View A — from the street looking into the warung, the benches in the middle with their backs to the camera, the TV on the back wall at upper left,","at night in heavy rain, cold blue-grey light, water streaming off the tarpaulin, nobody present. Generate with P8 attached: 'the same warung as the attached image, one year earlier in heavy rain'."),
 ("P10","Warung B — from the TV wall (present)","WARUNG","View B — from the back wall beside the TV, looking out over the two benches toward the open front and the street,","at night, warm light, the counter on the left of frame, nobody present. Generate with P8 attached: 'the same warung as the attached image, seen from the back wall looking out to the street'."),
 ("P11","Kampung alley","ALLEY","Looking down the alley toward the warung at the far end,","at night, warm lamp light, nobody present."),
 ("P13","Warung B — from the TV wall, rain (one year earlier)","WARUNG","View B — from the back wall beside the TV, looking out over the two benches toward the open front and the street,","at night in heavy rain, cold blue-grey light, rain falling in the street beyond the awning, nobody present. Generate with P10 and P9 attached."),
 ("P12","Jakarta avenue","STREET","At street level in the middle of the avenue,","at night, the road empty."),
]

# ---------- Scenes ----------
# (start, end, lyric, chars, plate, look, priority, image_body, video_body, audio, note)
exec(open('/home/claude/juara_data/v3S.py').read())
LBL=lambda i: LABELS[i-1]

def fmt(t):
    m=int(t//60); s=t-60*m
    return f"{m}:{s:04.1f}"

SHORT = {"SON":"the son","SON_PAST":"the son one year earlier","BAPAK":"Bapak","SCARF":"the red scarf","PLAYERS":"football players","OPP":"opposing players","TROPHY":"a trophy","NEIGH":"kampung neighbours"}
def line(k):
    v=L[k]; n=SHORT[k]
    d=v.split(": ",1)[1] if v.startswith(n+": ") else v
    return f"{n} ({d})" if d!=v else f"{n} ({v})"
def expand(txt):
    for k in L:
        txt=txt.replace("{"+k+"}",line(k))
    return txt

PL = {p[0]:p for p in PLATES}


def needs_sheet(chars):
    return any(c in chars for c in ("SON","SON_PAST","BAPAK","SCARF","TROPHY"))
PLATE_ATTACH = {"P1":"your real GBK photo","P2":"P1 + your real GBK photo","P3":"P1 + your real GBK photo","P4":"P1 + your real GBK photo","P5":"P1 + your real GBK photo","P6":"P1 + your real GBK photo","P7":"P1","P8":"nothing","P9":"P8","P10":"P8","P11":"P8","P12":"nothing","P13":"P10 + P9"}
def attach_html(i,sc):
    st,en,lyr,chars,plate,look,pri,ib,vb,aud,note=sc
    items=[]
    if needs_sheet(chars): items.append("Character sheet")
    if "SON" in chars and ib.startswith("Seen from behind"): items.append("Son back view")
    pid = plate[0] if isinstance(plate,tuple) else plate
    if pid: items.append(f"Plate {pid} ({PL[pid][1]})")
    img = " + ".join(f"<b>{esc(x)}</b>" for x in items) if items else "<b>nothing</b> (one-off location)"
    if not pid and items: img += " only — no plate: the stadium stays a soft blur behind him" if "Tight chest-up shot on an 85mm telephoto lens" in ib else " only (one-off location)"
    order = " — character sheet first" if needs_sheet(chars) and plate else ""
    reuse = REUSE.get(LBL(i))
    rhtml = f'<span>Also attach: <b>the {esc(reuse)} first-frame image</b> (same setup — keeps faces, light and place consistent)</span>' if reuse else ''
    return f'<div class="attach"><span class="al">Attach</span><span>Image: {img}{order}</span>{rhtml}<span>Video: <b>the {LBL(i)} first-frame image</b></span></div>'

REUSE = {"Sc07-B":"Sc08","Sc20":"Sc12","Sc21":"Sc11-A","Sc22":"Sc10-A","Sc24":"Sc14","Sc25":"Sc04",
 "Sc30":"Sc10","Sc31":"Sc15","Sc33":"Sc31","Sc34":"Sc15","Sc35":"Sc34","Sc36":"Sc35","Sc37":"Sc36",
 "Sc38":"Sc37","Sc39":"Sc38","Sc40":"Sc33","Sc41":"Sc40","Sc32":"Sc29"}

def img_prompt(i,sc):
    st,en,lyr,chars,plate,look,pri,ib,vb,aud,note=sc
    parts=[f"({LBL(i)})"]
    if needs_sheet(chars) and plate: parts.append("Match all characters exactly to the attached character reference image, and match the setting exactly to the attached location reference image.")
    elif needs_sheet(chars): parts.append("Match all characters exactly to the attached character reference image.")
    elif plate: parts.append("Match the setting exactly to the attached location reference image.")
    parts.append(expand(ib))
    if plate:
        pid,view=(plate if isinstance(plate,tuple) else (plate,PL[plate][3]))
        p=PL[pid]; parts.append(view+" "+E[p[2]]+".")
    parts.append(LOOK[look])
    parts.append(STYLE)
    return " ".join(parts)

def vid_prompt(i,sc):
    st,en,lyr,chars,plate,look,pri,ib,vb,aud,note=sc
    extra = " Players' faces are never visible." if ("PLAYERS" in chars or "OPP" in chars) else ""
    return f"({LBL(i)}) {vb} One continuous shot with no cuts or scene changes. Keep the setting exactly as in the first frame: do not add, extend or reshape buildings, roofs, stands or streets. Keep all movement natural and realistic.{extra} Nobody sings or lip-syncs. Audio: {aud}; ambience only, no music, no singing."

def action(d):
    if d<9.0: return ("Trim", f"keep first {d:.2f}s at 1.0×")
    if d<=11.1: return ("Speed", f"{10/d:.2f}×")
    return ("Hold", f"1.0× + {d-10:.2f}s freeze")

def plate_prompt(p):
    pid,name,loc,view,extra=p
    return f"Location reference plate, no characters. {view} {E[loc]}. {extra} {STYLE}".replace("  "," ")

CHAR_SHEET = ("Photorealistic character reference sheet on a plain light-grey studio background, even soft light, labelled zones but no text: "
 "left, " + L["SON"] + ", shown full body front view and three-quarter view, wearing " + L["SCARF"] + " around his neck; "
 "centre-left, the same man in his flashback outfit: " + L["SON_PAST"] + ", full body front view; "
 "centre-right, " + L["BAPAK"] + ", full body front view and a head-and-shoulders close-up; "
 "right, a close-up of " + L["SCARF"] + " laid flat, and " + L["TROPHY"] + ". "
 "Landscape 16:9, no logos, no watermarks, no captions; the only lettering allowed is the word INDONESIA on the scarf and the number 12 on the son's jersey.")

def esc(s): return html.escape(s, quote=True)

blocks=[]
def copyblock(kind,label,text,cid):
    return f'<div class="pr {kind}"><div class="prh"><span class="prl">{esc(label)}</span><button class="cp" type="button" data-t="{cid}">Copy</button></div><pre id="{cid}">{esc(text)}</pre></div>'

out=[]
cid=0
def nid():
    global cid; cid+=1; return f"c{cid}"

# scenes html
scene_html=[]
rows=[]
for i,sc in enumerate(S,1):
    st,en,lyr,chars,plate,look,pri,ib,vb,aud,note=sc
    d=en-st
    act,setting=action(d)
    who=", ".join(CHAR_NAMES[c] for c in chars) if chars else "none"
    pid = plate[0] if isinstance(plate,tuple) else plate
    loc = (f"{ENV_NAMES[PL[pid][2]]} — plate {pid} ({PL[pid][1]})" if pid else "one-off location, no plate")
    lookname={"NOW":"Present night","PAST":"One year earlier","DAWN":"Dawn"}[look]
    pri_html='<span class="tag pri">Priority</span>' if pri else ''
    scene_html.append(f'''<article class="sc look-{look.lower()}" id="{LBL(i).lower()}">
<header class="sch"><span class="badge">{LBL(i)}</span><span class="tc">{fmt(st)} – {fmt(en)}</span><span class="dur">{d:.2f}s</span><span class="tag look">{lookname}</span><span class="tag act">{act} {setting}</span>{pri_html}</header>
<p class="lyr">{esc(lyr)}</p>
<dl class="meta"><div><dt>On screen</dt><dd>{esc(who)}</dd></div><div><dt>Location</dt><dd>{esc(loc)}</dd></div></dl>
{attach_html(i,sc)}
{copyblock("img","First-frame image prompt",img_prompt(i,sc),nid())}
{copyblock("vid","Video prompt",vid_prompt(i,sc),nid())}
{f'<p class="note">{esc(note)}</p>' if note else ''}
</article>''')
    rows.append(f"<tr><td>{LBL(i)}</td><td>{fmt(st)} – {fmt(en)}</td><td>{d:.2f}s</td><td>{act}</td><td>{setting}</td><td>{'LRC' if '(' not in lyr[:1] else 'LRC / interlude split'}</td></tr>")

cons=[]
for k in ["SON","SON_PAST","BAPAK","SCARF","PLAYERS","OPP","TROPHY","NEIGH"]:
    cons.append(copyblock("con",CHAR_NAMES[k],L[k],nid()))
envs=[copyblock("con",ENV_NAMES[k],v,nid()) for k,v in E.items()]
plates=[f'<div class="attach"><span class="al">Attach</span><span>{esc(p[0])}: <b>{esc(PLATE_ATTACH[p[0]])}</b></span></div>'+copyblock("plate",f"{p[0]} · {p[1]}",plate_prompt(p),nid()) for p in PLATES]

n_trim=sum(1 for s in S if s[1]-s[0]<9); n_speed=sum(1 for s in S if 9<=s[1]-s[0]<=11.1); n_hold=sum(1 for s in S if s[1]-s[0]>11.1)
pri_list=", ".join(f"{LBL(i)}" for i,s in enumerate(S,1) if s[6])

page = open('/home/claude/juara_template.html').read()
page = (page.replace("%%CHARSHEET%%", '<div class="attach"><span class="al">Attach</span><span>Character sheet: <b>nothing</b> (or your current sheet when editing it)</span></div>'+copyblock("plate","Character reference sheet",CHAR_SHEET,nid()))
            .replace("%%PLATES%%","\n".join(plates))
            .replace("%%CONS%%","\n".join(cons))
            .replace("%%ENVS%%","\n".join(envs))
            .replace("%%SCENES%%","\n".join(scene_html))
            .replace("%%ROWS%%","\n".join(rows))
            .replace("%%NSC%%",str(len(S)))
            .replace("%%NTRIM%%",str(n_trim)).replace("%%NSPEED%%",str(n_speed)).replace("%%NHOLD%%",str(n_hold))
            .replace("%%PRI%%",pri_list))
open('/home/claude/juara-scene-breakdown.html','w').write(page)
print(len(S), n_trim, n_speed, n_hold, len(page))
