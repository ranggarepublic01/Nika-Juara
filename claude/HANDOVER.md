# Nika Music – handover (11 Oct 2026)

Read this first, then `claude/nika-music-album-plan.md`. Rawa is in Jakarta (WIB, UTC+7); replies in English, short and practical, every prompt in its own code block. Consult before big structural decisions; short multiple-choice check-ins are welcome. Locked decisions stay locked unless Rawa reopens them.

## Where things stand
- **Album "COMEBACK"** (renamed from BANGKIT on 11 Oct): 11 tracks, one story thread (Bapak, his son and the old red INDONESIA scarf), illustrated poster / street-mural look, released as singles up to the AFC Asian Cup 2027. Goal: YPP back (4,000 public watch hours in 12 months).
- **#5 JUARA!: published Sat 10 Oct, 14:00 WIB.** 1080p lyric video, 6 Shorts (YouTube and TikTok, one a day 10–15 Oct), metadata done. Still to do on YouTube: change "BANGKIT" to "COMEBACK" in the description and tags. Rawa will share the 48-hour and 7-day numbers.
- **#4 Garuda Calling: Reborn: in progress, target Sat 24 Oct.** Direction: slow rock/metal power ballad with a children's choir (variation D). Final candidate "Reborn v4" (5:04) is made; **its outro needs rework** (Replace Section prompt is ready). Then: Bahasa Indonesia version (31 Oct, a singable adaptation to the new melody), lyric video, Shorts, metadata.

## Files
| File | What it is |
|---|---|
| `claude/nika-music-album-plan.md` | Album plan: tracklist, release dates, sound, Suno rules, video pipeline, release kit |
| `claude/garuda-calling-reborn/suno.md` | Garuda Calling: Reborn Suno package: variations A–D, the sequence-style experiment, the v4 final candidate and the outro rework |
| `claude/garuda-calling-reborn/garuda-calling-original-lyrics.txt` | Original lyrics (EN + literal ID meaning) |
| `claude/juara-lyric-video/` | JUARA! lyric video plan (artwork prompts, motion clips, edit timeline, lyric spec) and its page builder |
| `claude/juara-youtube-metadata.md`, `claude/juara-shorts-metadata.md` | Title, description, tags, thumbnail prompts, Shorts and TikTok captions |
| `edit/render.py`, `edit/shorts.py` | Renderers for the 16:9 lyric video and the 9:16 Shorts (ffmpeg + Pillow + libass, Anton font in `edit/fonts/`). JUARA!-specific timeline for now; needs a per-song config before the next song |
| `assets/` | JUARA! artworks (A1–A10), Veo clips (M1–M10), song MP3 |
| `lyrics/` | JUARA! final Suno LRC/SRT and the on-screen SRT |
| `release/` | Finished JUARA! video (v3, 1080p HEVC) and the 6 Shorts |
| `claude/nika-juara-migration-brief.md` | The 9 Oct handover from the photoreal attempt (historical) |

## What Rawa needs to send for the next steps
- Garuda Calling: Reborn final take (after the outro rework): MP3 + SRT + LRC with word timings.
- Later: the artworks and Veo clips for its lyric video, uploaded to `assets/` (or a new song folder) named by prompt code.

## Working notes
- Suno Pro, model v6 mini, no Persona: the vocal is locked by the style string. Lyric tags beat the style box. Max Mode for final takes.
- Images: Gemini only, one model per album, full-size downloads. Veo only for instrumentals, never looped.
- Rendering needs ffmpeg with libass, Python 3 with Pillow and numpy. Finished videos go out as HEVC under 100 MB (GitHub limit); the chat takes files up to 30 MB.
