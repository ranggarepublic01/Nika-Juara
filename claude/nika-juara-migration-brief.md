# Nika Music — JUARA! Migration Brief

*Handover from the 7–9 Oct 2026 session. Read this first, then `claude/nika-music-album-plan.md` (same project). Rawa is in Jakarta (UTC+7); replies in English, short and practical.*

---

## 1. Where things stand (9 Oct, 15:10)

**Decision pending — the next session starts here.** Rawa stopped the photoreal Veo music video at Sc23 of 45. Reason, in his words: the audience lived the real FIFA ASEAN Cup final and its euphoria, and the photoreal AI footage "feels like a poor imitation of the real event"; the forced visuals damage a very good song. Veo also struggles with crowds and stadium geometry.

Options discussed (last message from Claude, not yet answered):

1. **Recommended now: an illustrated lyric video.** Big animated red-and-white lyrics plus 8–10 illustrated artworks in one consistent style (e.g. Indonesian mural / poster art: the scarf, Garuda, stadium silhouette, the warung at night), with slow motion and light effects. This is Nika's proven format (Garuda Calling lyric video, 194k views). It can be released fast while the win is fresh.
2. **Later, if the song performs: an animated (anime / painted) official music video** of the same father-and-son story. A stylised world isn't compared with the real night, and AI is far more consistent in stylised looks.
3. **Rejected: slideshow of real match photos from the internet.** Copyright (agency / PSSI photos), YouTube "reused content" rejection risk for YPP, and real players' faces (Rawa decided against using real players). The legitimate variant is supporters sending their own photos with permission, credited.

Clips already made (Sc01–Sc23) are not wasted: the intimate ones (Bapak folding the scarf, the warung, the son with the scarf) can be cut into Shorts.

**Next step:** ask Rawa which direction. If option 1, deliver the lyric-video plan: an art direction, 8–10 artwork prompts for Gemini in one style, each mapped to song sections and timings from the final LRC, plus a lyric animation spec.

---

## 2. Channel and goal

- **Nika Music**: Rawa's YouTube channel of Suno songs, on hiatus since 30 May 2025; lost YPP.
- 2024: "Garuda Calling" (Timnas Indonesia anthem) went viral and got the channel into YPP. Lifetime ~299k views, 3.3k subs; 86.5% Indonesia, 85% male, 25–44. Recommendations + Browse bring ~59% of traffic; 91% of watch time is from non-subscribers.
- **YPP gap is watch hours**, not subscribers: 4,000 public hours in 12 months ≈ 160k long-form views at ~1:31 average view.
- **Plan: comeback concept album "BANGKIT"** (fall → rebuild → ASEAN champions → Asian Cup), released as singles through to the AFC Asian Cup 2027 (Group F: Japan 11 Jan, Qatar 16 Jan, Thailand 20 Jan, all 23:00 WIB). Full tracklist and release order are in `claude/nika-music-album-plan.md`.
- Indonesia won the FIFA ASEAN Cup 2026 final vs Thailand at GBK on 5 Oct 2026.

---

## 3. Single 1 — JUARA! (song is final)

- **Final take:** "Juara - The Masterpiece (Final) (Remastered) FIx FIX FIX USE THIS", **5:57.6**, Suno Pro, v6 mini.
- **Style used:** Arena rock with arena-sized reverb tails; recurring brass, distorted guitar, and angklung riff over orchestral strings, piano, choir, stomp-claps, and taiko; gritty, raspy male baritone-tenor lead with warm operatic mezzo-soprano counter-vocal; driving 128 bpm, singable anthem with a key-change finale.
- **Structure (from the final LRC):** vocalise intro 0:11.7 → "Ayo, ayo, Garuda" 0:22.3 → "Juara / Garuda di dada" 0:29.7 → long instrumental → verse 1 1:24.8 (warung, a year ago) → pre-chorus 1:42.6 → chorus 2:12.2 → "Ayo" ×4 2:26.7 → verse 2 2:55.6 → pre-chorus 2 3:09.7 → chorus 3:28.0 → "Ayo" ×4 3:42.8 → long instrumental → bridge (female) 4:26.2 → final chorus ×2 4:58.5 → "Ayo" 5:27.3 → "Asia, kami siap!" 5:32.4 → "Asia, kami datang!" 5:36.1 → outro to 5:57.6.
- **The SRT and LRC files are not in the project.** Ask Rawa to attach the final SRT + LRC (and the song file if assembling video) in the new session.

### Lyric / Suno rules learned (keep for the next album tracks)

- Bahasa Indonesia first; chorus = short chant, verses = concrete everyday images (warung TV, syal, Bapak), the style of current Indonesian hits.
- Spell abbreviations as Indonesian letter sounds in Suno's lyrics box (GBK → Ge-Be-Ka, TV → Ti-Vi, PSSI → Pe-Es-Es-I); normal spelling on screen.
- "Ayo" at the very start of a song can be sung as "eyo"; write "Ah-yo" there.
- Forcing "the riff plays the chorus melody" did not work; use normal structure tags.
- Hook within the first 20 s for retention.
- Fix single bad sections with Replace Section rather than rerolling.

### Rights rules

- Songs made on Suno's free plan are non-commercial; subscribing later does not license them retroactively. Garuda Calling was made on v3.5 free, so it will be remade with the same lyrics (Rawa's own) and fresh music on Pro — no Cover / Remaster / Inspo of free-plan songs.
- Rawa subscribed to Suno Pro on 8 Oct 2026 (shared with Quacklings Batch 2).

---

## 4. The photoreal video attempt (paused)

- **Story:** a father (Bapak, alive) and son, one old red INDONESIA scarf. A year ago at the kampung warung they switched off the TV after the World Cup exit; Bapak folded his scarf and said "nanti juga menang". Tonight the son carries the scarf into GBK for the final; Bapak watches at the same warung. After the win the son rides home and wraps the scarf around his father's neck. Dawn ending.
- **Breakdown artifact:** "JUARA! Scene Breakdown", https://claude.ai/artifact/Lu9iy5xLb3KnTK2ccqp6qh — 45 scenes (incl. Sc07-A, Sc07-B, Sc10-A, Sc11-A), plates P1–P13, attach boxes, reuse-reference notes, speed/trim table. Read it with the Artifact tool (`action: "read"`), not WebFetch.
- **Made:** Sc01–Sc23 (Sc10-A was refused by Veo; plan was a still with a slow CapCut zoom).
- **Open, never answered:** whether the son wears the patterned replica jersey (would mean redoing Sc02, 03, 05) or stays in the plain red one.
- The breakdown's source files (`juara_build.py`, `juara_template.html`, `v3S.py`, `v2_S.json`) are saved in the project under `claude/juara-breakdown/` if the page ever needs rebuilding.

### Visual lessons (apply to any AI video for this channel)

- **Crowds and stadium architecture are the image model's weak spot.** Face-on stand shots only worked as tight telephoto close-ups with a blurred background.
- **Veo invents what it can't see:** rising / orbiting / reveal camera moves grew new roofs. End every video prompt with: "One continuous shot with no cuts or scene changes. Keep the setting exactly as in the first frame: do not add, extend or reshape buildings, roofs, stands or streets." Prefer "the camera holds still".
- **Check every prompt for spatial logic** (where the camera is, which way people face, where the pitch / TV / street is) before giving it to Rawa. Sc02 and Sc12 failed on this.
- **Show what to attach for every image**, character sheet first. Without it the son's face drifted.
- **Reuse earlier first frames as references** for scenes that return to the same setup (Rawa's discovery on Sc21).
- **Veo refusals:** dense realistic crowds with flares were refused even with a calm prompt ("I can't generate that video"). The trigger is likely the image, not the wording.
- No logos, crests or sponsor marks; players only as silhouettes from behind; only lettering allowed: INDONESIA on the scarf and 12 on the son's jersey (12 = "pemain ke-12", the supporters).

---

## 5. Other album items still open

- Garuda Calling: Reborn — same lyrics, fresh Pro generation (English original + Bahasa version).
- Catalogue → Shorts: old songs are fixed-image lyric videos; Shorts need motion.
- Between-tournament songs (supporter anthems, tributes) to stop the post-event cliff.
- Old free-plan videos stay up but get monetization switched off once YPP returns.

---

## 6. How Rawa likes to work

- Consult before big structural decisions; short multiple-choice check-ins are welcome.
- Copy-friendly prompts: each prompt in its own code block.
- Locked decisions are carried forward and not reopened unless he raises them.
- Feedback loop: Claude writes → Rawa generates → reports what worked/drifted → Claude adjusts.
