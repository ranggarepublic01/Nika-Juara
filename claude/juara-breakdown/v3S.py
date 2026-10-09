import json
C=json.load(open('/home/claude/juara_data/v2_S.json'))
def fix(p): return tuple(p) if isinstance(p,list) else p
FRONT_TXT=" Tight chest-up shot on an 85mm telephoto lens at eye level, very shallow depth of field: he is sharp, and everything behind him melts into soft out-of-focus blobs of red and white supporters and warm red flare glow, with no readable architecture, no roof, no sky and no pitch. Only one or two other supporters appear, cut off at the edges of the frame and softly blurred, facing the same way he does."
def K(n, st, en, lyr=None, ib=None, vb=None, note=None, pri=None, plate="KEEP"):
    o=C[n-1]
    return (st,en, lyr if lyr is not None else o[2], o[3], fix(o[4]) if plate=="KEEP" else plate, o[5],
            o[6] if pri is None else pri, ib if ib is not None else o[7], vb if vb is not None else o[8], o[9],
            note if note is not None else o[10])
def N(st,en,lyr,chars,plate,look,pri,ib,vb,aud,note):
    return (st,en,lyr,chars,plate,look,pri,ib,vb,aud,note)
MADE="Already made — retimed only. "
NEW="NEW — not made yet. "
SC12_VB="Beat 1 (about 3.1s): he stays frozen, the scarf pressed to his mouth, eyes wide and fixed just past the camera, barely breathing. Beat 2 (about 3.4s): his eyes go even wider, then he throws both fists up into the air with the scarf, shouting with joy; his arms stay inside the frame. Beat 3 (about 3.5s): he laughs and shakes his raised fists, while the blurred supporters behind him jump and wave. The camera holds still at the same framing."
S=[]; LABELS=[]
def add(lbl, sc): LABELS.append(lbl); S.append(sc)
add("Sc01", K(1, 0.00, 11.10, note=MADE+"Slow to 0.90× to reach the vocalise."))
add("Sc02", K(2, 11.10, 16.80, note=MADE+"Trim keeps his look-back grin."))
add("Sc03", K(3, 16.80, 22.27, note=MADE+"Cut just before the first \"Ayo\"."))
add("Sc04", K(4, 22.27, 29.70, note=MADE))
add("Sc05", K(5, 29.70, 35.70, note=MADE+"\"Juara! Juara! / Garuda di dada\"."))
add("Sc06", K(6, 35.70, 45.70, note=MADE))
add("Sc07", K(7, 45.70, 55.70, note=MADE))
add("Sc07-A", N(55.70, 65.30, "(instrumental — anthem moment)", ["PLAYERS","OPP"], "P5", "NOW", True,
  "Seen from high in the upper tier: the whole far stand is standing still, supporters holding red-and-white scarves taut above their heads; far below on the pitch, tiny {PLAYERS} and {OPP} stand in two straight lines facing the stand for the national anthem, all figures far too small to show faces.",
  "One slow action: the scarves stay raised and almost still; a giant red-and-white flag ripples gently across the stand; the players stand motionless in their lines. The camera holds still.",
  "a vast stadium falling quiet, wind, a single drum beat",
  NEW+"The quiet before kickoff. Speed 1.04×."))
add("Sc07-B", N(65.30, 74.82, "(instrumental — anthem moment)", ["SON","SCARF"], None, "NOW", True,
  "{SON} stands still in his row facing the camera, his right hand pressed flat on his chest over his heart, {SCARF} around his neck, eyes glistening, looking just past the camera toward the pitch."+FRONT_TXT,
  "Beat 1 (about 4s): he stands still, hand on his heart, breathing slowly. Beat 2 (about 3.5s): his eyes fill with tears and he swallows hard. Beat 3 (about 2.5s): he lifts his chin, proud. The camera holds still.",
  "a quiet stadium, wind, distant drums",
  NEW+"Anthem: hand on heart. Speed 1.05×. Sc08 (eyes closed) follows naturally."))
add("Sc08", K(8, 74.82, 84.82, vb="Beat 1 (about 4s): slow push-in toward his face. Beat 2 (about 2.6s): he closes his eyes for a moment and breathes out. Beat 3 (about 3.4s): he stays still, eyes closed.", note=MADE+"Now plays the full 10s. Hard cut to the flashback after this clip."))
add("Sc09", K(9, 84.82, 91.87, note=MADE))
add("Sc10", K(10, 91.87, 102.55, note=MADE+"Speed 0.94×. \"Nanti juga menang\" at 1:35.5 lands on the nod."))
add("Sc10-A", N(102.55, 109.68, "Senin malam, Ge-Be-Ka penuh lagi", [], "P5", "NOW", True,
  "The packed far stand seen from high in the upper tier: every seat full of supporters in red and white, scarves and small flags raised, red flare smoke drifting, the ring roof floodlights blazing above.",
  "One flowing action: the whole stand sways and waves scarves; flare smoke drifts slowly. The camera holds still, drifting only very slightly.",
  "a huge crowd roaring, drums",
  NEW+"\"GBK penuh lagi\": the full stadium, before Sc11 picks up \"Syal yang sama\"."))
add("Sc11", K(11, 109.68, 117.00, note=MADE+"Lands on \"Syal yang sama kini di tanganku sendiri\"."))
add("Sc11-A", N(117.00, 120.60, "Detik terakhir, napas kita tertahan", ["BAPAK","NEIGH"], "P10", "NOW", True,
  "Seen from beside the TV, facing them: {BAPAK} sits frozen on the edge of the front bench, both hands clasped in front of his mouth, eyes fixed on the TV just beside the camera, its glow on his glasses; {NEIGH} around him frozen too.",
  "Beat 1 (about 3.6s): nobody moves; Bapak grips his hands tighter and holds his breath. Beat 2 (about 6.4s): he stays frozen, eyes wide. The camera holds still.",
  "a tense hush, a clock ticking, a muffled TV crowd with no clear words",
  NEW+"Short cutaway: the same last seconds at home. Trim to 3.6s."))
add("Sc12", K(12, 120.60, 132.18, vb=SC12_VB, note=MADE+"At 1.0× his fists go up on \"Lalu meledak\" (2:03.9); hold the last frame 1.6s."))
add("Sc13", K(13, 132.18, 139.40, note=MADE+"Chest thump on \"Garuda di dada\" (2:15.5)."))
add("Sc14", K(14, 139.40, 146.74, note=MADE))
add("Sc15", K(15, 146.74, 153.92, note=MADE+"Now 7.2s on the \"Ayo\" chant."))
add("Sc16", K(16, 153.92, 164.80, note="Nusantara montage 1 of 2. One-off location, no plate. The screen stays out of frame; only its glow shows. Speed 0.92×."))
add("Sc17", K(17, 164.80, 175.59, note="Nusantara montage 2 of 2. Speed 0.93×."))
add("Sc18", K(18, 175.59, 182.60))
add("Sc19", K(19, 182.60, 189.67))
add("Sc20", N(189.67, 192.90, "Detik terakhir, napas kita tertahan", ["SON","SCARF"], None, "NOW", False,
  "{SON} frozen in tension in his row, facing the camera, both hands gripping {SCARF} against his chin, eyes wide and fixed just past the camera."+FRONT_TXT,
  "Beat 1 (about 3.2s): he holds his breath, eyes wide. Beat 2 (about 6.8s): he stays frozen. The camera holds still.",
  "a tense hush across the stadium",
  "Short: trim to 3.2s. Cut to the warung for the eruption."))
add("Sc21", K(20, 192.90, 202.90, note="Bapak frozen, then the warung erupts on \"Lalu meledak\" (3:16.3), 3.4s into the clip."))
add("Sc22", N(202.90, 207.99, "(build)", [], "P5", "NOW", False,
  "The far stand erupting: thousands of supporters jumping with scarves twirling overhead, red flare smoke billowing, the ring roof floodlights blazing.",
  "One flowing action: the whole stand jumps and waves scarves; flare smoke billows. The camera holds still.",
  "a huge roar, drums",
  "Trim to 5.1s."))
add("Sc23", K(21, 207.99, 215.08))
add("Sc24", K(22, 215.08, 222.84, lyr="Juara! Juara! / Bilang ke Bapak, kita juara!",
  ib="{SON} in his row facing the camera, tears of joy on his face, kissing {SCARF} and then lifting it high with both hands."+FRONT_TXT,
  vb="Beat 1 (about 3s): he presses the scarf to his lips, eyes closed, tears running. Beat 2 (about 3.5s): he lifts the scarf high above his head with both hands, laughing. Beat 3 (about 3.5s): he looks up at it, beaming. The camera holds still.",
  note="Celebration, no phone."))
add("Sc25", K(23, 222.84, 229.43, lyr="Ayo, ayo, Garuda! (x4)"))
add("Sc26", K(24, 229.43, 239.43))
add("Sc27", K(25, 239.43, 249.43))
add("Sc28", K(26, 249.43, 256.00, note="Nusantara montage, highland town."))
add("Sc29", K(27, 256.00, 266.19, vb="Beat 1 (about 6s): he rides slowly away from the camera down the alley toward the warung. Beat 2 (about 4s): he slows and stops a short way before the warung, one foot down, still. The camera holds still throughout.", note="Speed 0.98×."))
add("Sc30", K(28, 266.19, 273.23))
add("Sc31", K(29, 273.23, 280.22))
add("Sc32", K(30, 280.22, 287.86))
add("Sc33", K(31, 287.86, 298.54, vb="Beat 1 (about 4s): the son wraps the scarf around his father's neck. Beat 2 (about 3s): Bapak touches it with both hands, his eyes wet. Beat 3 (about 3s): they embrace and hold still.", note="Emotional peak. Speed 0.94×: the embrace lands as \"bahagia\" ends."))
add("Sc34", K(32, 298.54, 305.45, note="Final chorus, first pass. Chest thump on \"Garuda di dada\" (5:01.8). From here Bapak always wears the scarf."))
add("Sc35", K(33, 305.45, 312.63, note="Son points at Bapak on \"Bilang ke Bapak\" (5:09.1)."))
add("Sc36", K(34, 312.63, 319.62))
add("Sc37", K(35, 319.62, 327.34, note="His smile lands on the last \"Bilang ke Bapak, kita juara!\" (5:23.3)."))
add("Sc38", K(36, 327.34, 332.43, note="Trim to 5.1s."))
add("Sc39", K(37, 332.43, 339.00, lyr="Asia, kami siap! / Asia, kami datang!",
  vb="Beat 1 (about 1.5s): on \"Asia, kami siap!\" father and son raise their fists high together. Beat 2 (about 2.1s): the whole alley jumps. Beat 3 (about 1.5s): on \"Asia, kami datang!\" everyone points forward past the camera. Beat 4 (about 4.9s): they cheer and jump. The camera holds still.",
  note="Fists on \"Asia, kami siap!\" (5:32.4), points on \"kami datang\" (5:36.1)."))
add("Sc40", K(38, 339.00, 347.50, note="Dawn, quiet after the party."))
add("Sc41", K(41, 347.50, 357.56, note="Last image and end card (5:47.5–5:57.6, right third). Speed 0.99×."))
