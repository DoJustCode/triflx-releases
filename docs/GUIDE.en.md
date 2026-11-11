# triflX — user guide

triflX shrinks images, GIFs, video, PDF and audio on your Mac. It lives in the menu bar, works in the background and never uploads anything. Guide version: 2.2.

[Русская версия](GUIDE.ru.md) · [Download](../../../releases/latest)

## Contents
1. [Install and first launch](#1-install-and-first-launch)
2. [How it works](#2-how-it-works)
3. [Ways to start compression](#3-ways-to-start-compression)
4. [The result card](#4-the-result-card)
5. [Supported formats](#5-supported-formats)
6. [Settings window, tab by tab](#6-settings-window-tab-by-tab)
7. [Platform presets](#7-platform-presets)
8. [Pipelines and quick-action zones](#8-pipelines-and-quick-action-zones)
9. [Batch processing](#9-batch-processing)
10. [Existing files and background mode](#10-existing-files-and-background-mode)
11. [The “already optimized” mark](#11-the-already-optimized-mark)
12. [Cancel and restore the original](#12-cancel-and-restore-the-original)
13. [Finder menu](#13-finder-menu)
14. [Shortcuts](#14-shortcuts)
15. [Terminal and AI agents](#15-terminal-and-ai-agents)
16. [Built-in ffmpeg converter](#16-built-in-ffmpeg-converter)
17. [Where things are stored](#17-where-things-are-stored)
18. [FAQ](#18-faq)

---

## 1. Install and first launch
1. Download `triflX.dmg` from [Releases](../../../releases/latest), open it and drag triflX to Applications.
2. The app is signed and notarized by Apple. macOS 13+, Apple Silicon and Intel.
3. A welcome screen with tips appears on first launch. There is no Dock icon — look for the menu-bar icon.
4. Updates arrive automatically (Sparkle). Manual check: menu → “Check for Updates…”.

Clicking the icon opens the menu: statistics, clipboard actions, zones, presets, pause, backups, settings.

## 2. How it works
For every file triflX:
1. Copies the original to the backup folder (`~/Library/Application Support/triflX/Backups`).
2. Compresses it. The result is written **only if it is smaller**; for transformations (format, scale, crop, conversion) it is always written.
3. Shows a result card with a “Restore original” button.

Your files stay on disk; nothing is uploaded. Backups are removed after the configured number of days (7 by default).

## 3. Ways to start compression
| Way | What happens |
|---|---|
| **Clipboard** | A screenshot or image copied to the clipboard is replaced with the compressed version. Files copied in Finder (⌘C) too. |
| **Folders** | New files in watched folders are compressed automatically (you choose the folders in settings). |
| **Drag and drop** | Drop files or folders on the menu-bar icon, the “Drop zone”, or the settings window. Hold ⌘ on release for stronger compression. |
| **Finder menu** | Right-click → “Optimize with triflX” ([section 13](#13-finder-menu)). Also the “Optimize in triflX” Service and “Open With”. |
| **Hotkeys** | See the table below. |
| **Shortcuts** | Native triflX actions ([section 14](#14-shortcuts)). |
| **Terminal / AI** | The `triflx` command and MCP ([section 15](#15-terminal-and-ai-agents)). |

Hotkeys (work from any app):

| Keys | Action |
|---|---|
| ⌃⇧C | Optimize the clipboard |
| ⌃⇧A | Strong compression of the clipboard |
| ⌃⇧− | Halve the image on the clipboard |
| ⌃⇧Z | Undo the last optimization (restore original) |
| ⌃⇧= | Show the last result again |
| ⌃O | Optimize files selected in Finder (macOS asks for “Automation” permission the first time) |

## 4. The result card
After compression a card appears in the bottom-right corner: thumbnail, size “before → after”, percentage.
- **Click the thumbnail** to open the before/after comparison (a slider for images, two frames for video and PDF). The thumbnail can be dragged into any app.
- **“Restore original”** is visible right away and restores the file from the backup.
- Action icons: Compare, Presets, Strong compression, “For messengers” (images up to 1280 px, video 720p up to 16 MB), Downscale (75/50/25%), Convert (WebP, JPEG XL, JPEG, PNG, HEIC, AVIF), Fit to size (500 KB / 1 / 2 / 5 MB), Crop (16:9, 4:3, 3:2, 1:1, 9:16; PDF: A4 and square); for video — Mute, Speed (×0.5/1.5/2/4), Make GIF. Also: Copy, Open in external editor, Show in Finder, Share, AirDrop, “Stop watching this folder”.
- Every card operation is computed **from the original**, not from the already-compressed file, so quality losses don't pile up.
- The card stays for the configured time (15 s by default) and **never hides while the pointer is over it**. Bring the last one back with ⌃⇧=. All recent results are in the menu → “Recent results” (with restore later).

## 5. Supported formats
| Kind | Input | How it is compressed |
|---|---|---|
| Images | JPEG, PNG, HEIC, WebP, AVIF, JPEG XL, TIFF, BMP | Re-encoding with tuned quality, custom PNG quantizer, WebP/JPEG XL/AVIF/HEIC output, smart crop, side and size limits |
| GIF | GIF | Frame and palette reduction, optional speed-up |
| Video | MP4, MOV, M4V, MPG, plus MKV, WebM, AVI, TS, FLV, WMV (via built-in ffmpeg) | H.264 or HEVC, resolution/fps/size limits, mute, speed, MP4, GIF |
| PDF | PDF | Image compression inside (macOS filter or a set dpi), page crop |
| Audio | WAV, AIFF, FLAC, MP3, plus OGG, Opus, WMA, APE (via ffmpeg) | AAC in M4A, default or set bitrate |

Animated WebP/APNG and multi-frame files are never flattened to one frame. Corrupt, empty and unsupported files are skipped with a clear message (details in the error log).

## 6. Settings window, tab by tab
Menu → “Settings…” (⌘,). The sidebar has a **settings search**.

### General
- **Result card and cancel.** *Show the card for*: 5 / 15 / 30 s or Never hide. *Delay before compressing a file from a folder*: immediately, 2, 3 (default), 5, 10 s — the “cancel window” ([section 12](#12-cancel-and-restore-the-original)).
- **What to optimize.** Clipboard; TIFF data (usually from design apps — better left alone); new files in folders; pipelines for the clipboard and for drag and drop.
- **Quality.** *Maximum compression / Balanced / High quality* (≈ 0.5 / 0.7 / 0.85 for JPEG-like formats). *Max image size* caps the longest side.
- **Files.** *Result*: replace the file (original in backup) or save “name.min.ext” beside it. Result window, notifications, auto-update check, launch at login. A “Recent” block lists the latest files.

### Clipboard
What to intercept: image data (screenshots, copying from a browser), TIFF, image / video / audio / PDF files from Finder; “also copy the file path with the image data”. **Ignored apps** list — their clipboard is never touched; the quickest way is menu → “Ignore clipboard from …”. CorelDRAW, Illustrator, Figma, Sketch, Affinity and similar are recognized automatically so layers and vectors stay intact.

### Folders
The watched folders. Per folder: enabled, *Result* (as in general / replace / “.min” copy), *Quality*, *Max image size*, *Pipeline*, *Screenshots* (don't sort / “Screenshots” folder / by month / by day), a *Screenshot name* template (`{date}`, `{time}`, `{name}`), and the **“Process existing files…”** button.
How a file counts as “new”: on launch triflX remembers what is already in the folder; a file is new if it has a new name or changed. The file's date doesn't matter, so `cp -p`, unpacked archives and synced files all work. A file must stop growing first, then the cancel-window delay runs.

### Photo & Video
- *Photos → Metadata*: remove all (smaller, more private) / keep all / keep without location. Metadata means EXIF: camera, capture date, lens, and where the photo was taken.
- *Video → Scenario*: **Universal** (1080p, H.264), **For messengers** (720p, up to 16 MB), **Screen recording** (1080p, HEVC), **Maximum quality** (original resolution, HEVC), **Custom** (resolution, HEVC, size limit, always mute). Resolution is only ever reduced.

### Filters
Apply **only to automation** (clipboard and folders); things you drag yourself aren't filtered. Per type (images, video, audio, PDF): minimum and maximum size, minimum resolution (images and video), “skip if more than N files arrive at once”, extensions to leave alone. Defaults: images from 5 KB; video 200 KB–500 MB, max 1 at a time, MKV and M4V left alone; audio up to 100 MB, max 2; PDF up to 100 MB, max 2.

### Advanced
- **“Already optimized” mark** — [section 11](#11-the-already-optimized-mark).
- **Presets**: attachment limit for the “Email” preset (1–100 MB).
- **Background processing of old files** — [section 10](#10-existing-files-and-background-mode).
- **Adaptive compression**: large photos get stronger compression, small ones lighter; heavy PDF pages get a lower dpi. Manual settings win.
- **Images**: smart crop (the frame shifts toward the main subject, using Vision); keep wide colour (Display P3) instead of converting to sRGB.
- **Video**: frame-rate cap (30 / 60 / half / quarter of the source) — 120 fps screen recordings shrink a lot.
- **Audio**: AAC bitrate (macOS default or a set value).
- **Quick-action zones** — [section 8](#8-pipelines-and-quick-action-zones).
- **Compatibility** (auto-conversion, automation only): *Images → JPEG* and *→ PNG* (AVIF, HEIC, WebP, JPEG XL, BMP, TIFF), *Video → MP4* (MOV, MKV, WebM, AVI, FLV, WMV, TS, M4V, MPG…), *Audio → M4A* (OGG, Opus, WMA, APE, MP3). Tick the extensions to convert. WAV/AIFF/FLAC always become AAC.
- **PDF**: image resolution inside PDFs (default 144 dpi or 72–300 dpi).
- **Photos.app**: optimize images copied from Photos; skip if more than N are copied; downscale the longest side to N px.
- **Clipboard file name**: template with `%y %m %d %H %M %S %i` (default “Screenshot”).
- **External editor** per images / video / audio / PDF — a button appears on the card.
- **Hotkeys** — a reference table.

### Storage
Working folder path, backup retention (1–90 days), buttons “Open working folder”, “Backup folder”, “Clean working folder” (doesn't touch files the clipboard or recent results still reference). *Keep creation and modification dates*; **“Pause automatic optimization”** (also in the menu).

### Pipelines
Step sets applied in one pass: *Optimize*, *Strong compression*, *Downscale %*, *Convert to* (WebP, AVIF, JPEG XL, JPEG, PNG, HEIC), *Crop to ratio*, *Remove audio*, *Video speed*, *Video to GIF*, *Video scenario*. The **“Preset”** checkbox puts a pipeline into the presets menus ([section 7](#7-platform-presets)). A pipeline can be assigned to the clipboard, drag and drop, a zone or a specific folder.

### Tools
- **Finder menu** — toggle and hint ([section 13](#13-finder-menu)).
- Hotkey reference; ignored-apps list.
- **Install the triflx command** and **Copy MCP config** ([section 15](#15-terminal-and-ai-agents)).
- **Data**: open the backup folder; **export and import settings** to a file.

## 7. Platform presets
One click fits a file to a platform's requirements. Find them under the card's “Presets” icon, menu → “Preset for Finder selection”, the batch window, and the Shortcuts action “Apply Preset”.

| Preset | Images | Video |
|---|---|---|
| Telegram | longest side up to 2560 px | 720p |
| Instagram — post | crop 4:5, up to 1350 px | 1080p, crop 4:5 |
| Instagram — story | crop 9:16, up to 1920 px | 1080p, crop 9:16 |
| Web | WebP, up to 1920 px | 1080p H.264 |
| Email | up to 2048 px and at most N MB (10 by default, adjustable) | 720p, at most N MB |
| Slack / Discord | up to 1920 px, at most 8 MB | 720p, at most 8 MB |

**Your own presets:** create a pipeline on the “Pipelines” tab and switch on “Preset”.

## 8. Pipelines and quick-action zones
**Quick-action zones** (menu → “Quick-action zones”) are a floating panel of tiles. Drop files on a tile and its pipeline (or “strong compression”) is applied. The tiles are set up in the “Advanced” tab. The separate “Drop zone” does the same with your normal settings.

## 9. Batch processing
With more than five files (or while a batch is running) the batch window opens:
1. **Before starting** choose a preset or pipeline, or set manually: quality, image format, scale, longest side, metadata, strong compression.
2. **While running:** overall progress and a result per file. **Cancel** stops the queue and rolls the current file back to its original.
3. **Summary:** how much was saved, the list of errors, and **“Restore originals”**.
Files arriving mid-run are queued and processed as the next batch with the same settings.

## 10. Existing files and background mode
- **Manually.** “Folders” tab → the folder's “Process existing files…” button. A list opens (subfolders included, age filter, “skip already optimized”), the total size and **“Estimate savings”** — a real test on a few files of each type. Then the batch window.
- **In the background** (Advanced → “Background processing of old files”): *only at night (1–6 AM)*, otherwise only when you're away (5 minutes without input); *older than N days*; *skip files larger than N MB*; *don't run on battery*. Up to 25 files per pass; marked files are skipped; originals stay in backups.

## 11. The “already optimized” mark
After compression (or when a file is already optimal) triflX sets an extended attribute `com.triflx.optimized` holding size, modification date and quality profile. Automation (folders, clipboard, background) skips such files. If the file changes, the mark stops applying. **Manual actions ignore the mark.** Switch it off in “Advanced”. Inspect: `xattr -p com.triflx.optimized file`; remove: `xattr -d com.triflx.optimized file`.

## 12. Cancel and restore the original
- **Before compression (files from folders):** on the “Compressing in N s” card press **Cancel** — the file stays as is and is marked “don't touch”. The delay is set in “General” (0 = immediately).
- **During compression:** the card's **Cancel** stops the work (video export and ffmpeg included), temporary files are removed, the original is unchanged and marked “don't touch”.
- **After compression:** **Restore original** on the card, ⌃⇧Z, or menu → “Recent results”. A restored file is marked too, so automation won't compress it again — handy when you need the full size for print.
- Pause all automation: menu → “Pause automatic optimization”.

## 13. Finder menu
The context menu (right-click) on files and folders: **“Optimize with triflX”** compresses the selection in place (original kept in backup). Folders are expanded; many files open the batch window.
This is a Finder Sync extension. Enable it in “Settings → Tools → Finder menu” (restarts Finder) or “System Settings → General → Login Items & Extensions → Finder Extensions → triflX”. If the item is missing, switch the extension off and on, then run `killall Finder`.

## 14. Shortcuts
In the Shortcuts app look for triflX. Files come in and go out; **originals are not modified**.
- **Optimize Files** — any supported files, choose strength
- **Compress Image** (quality, longest side) · **Convert Image** (WebP, JPEG XL, AVIF, JPEG, PNG, HEIC) · **Resize Image** (%) · **Fit Image to File Size** · **Crop Image** (ratio, smart crop)
- **Compress Video** (universal, messengers, screen recording, maximum) · **Video to GIF** · **Compress PDF**
- **Apply Preset** — a platform preset for a file
- **Optimize Clipboard**
Ready phrases for Siri/Spotlight: “Optimize files with triflX”, “Optimize clipboard with triflX”, “Convert image with triflX”.

## 15. Terminal and AI agents
Install the command: “Settings → Tools → Install the triflx command” (creates a link `~/.local/bin/triflx`; if it isn't found, add `~/.local/bin` to PATH). Or call the binary: `/Applications/triflX.app/Contents/MacOS/triflX`.

```bash
triflx optimize photo.png                    # replace, original kept in backup
triflx optimize --convert webp --copy a.png  # save a.min.webp beside it
triflx optimize --scale 50 --max-size 500KB photo.jpg
triflx optimize --video messenger movie.mov
triflx optimize --mp4 clip.mkv               # MKV/WebM/AVI → MP4
triflx optimize --json *.png                 # JSON output
```

| Option | Meaning |
|---|---|
| `-a`, `--aggressive` | stronger compression |
| `--scale N` | downscale to N % |
| `--convert FMT` | webp, avif, jxl, jpeg, png, heic |
| `--crop W:H` | center-crop (16:9, 1:1, 210:297) |
| `--max-size N` | fit under a size: 500KB, 2MB (images) |
| `--mute` / `--speed X` / `--gif` / `--mp4` | video: mute / speed / to GIF / to MP4 |
| `--metadata strip\|keep\|nogps` | EXIF and location |
| `--video universal\|messenger\|screen\|max`, `--video-limit MB` | video scenario and limit |
| `--quality low\|medium\|high`, `--max-dim N` | quality and side cap |
| `--copy` | keep the original, save “name.min.ext” |
| `--json` | JSON output |

**MCP for AI agents:** `triflx mcp` (stdio). “Copy MCP config” in settings puts a ready snippet on the clipboard. Tool: `optimize_file`.

## 16. Built-in ffmpeg converter
For formats macOS can't read (MKV, WebM, AVI, TS, FLV, WMV, OGG, Opus, WMA, APE) the app carries a separate ffmpeg 7.1.1 program (`Contents/Helpers/ffmpeg`), built without GPL components (**LGPL v2.1+**), signed and notarized with the app. It runs as a separate process and turns the file into MP4 (H.264 via VideoToolbox + AAC) or M4A; the normal pipeline continues from there. Source and build options: see the licence file inside the app (`THIRD-PARTY-NOTICES.txt`) and [ffmpeg.org](https://ffmpeg.org/releases/ffmpeg-7.1.1.tar.xz). Automation converts these formats only if you ticked them under “Compatibility”. Conversion is a format change — the result can be larger than the source.

## 17. Where things are stored
| What | Where |
|---|---|
| Backups | `~/Library/Application Support/triflX/Backups` |
| Clipboard working folder | `~/Library/Application Support/triflX/Clipboard` (cleans itself) |
| Error log (last ~300 lines) | `~/Library/Application Support/triflX/triflx.log` — menu → “Show error log” |
| Settings | `defaults read com.trifl.x` (export and import as a `.plist` in “Tools”) |
The log is never sent anywhere. “Report a problem…” opens a GitHub form; you attach the log yourself.

## 18. FAQ
**A file wasn't compressed — “Already optimal”.** The result wouldn't be smaller; the original is untouched and marked. Try “Strong compression” on the card.
**It compressed too much / I need full size.** “Restore original” on the card or ⌃⇧Z; raise the delay before compression; exclude the folder or type in “Filters”.
**Screenshots aren't compressed.** Check “Watch the clipboard” and that the app isn't in the ignored list. For folders: the folder is enabled and the file finished writing.
**The Finder item is missing.** See [section 13](#13-finder-menu).
**MKV/WebM video isn't processed automatically.** Tick the extension in “Advanced → Compatibility → Video → MP4”.
**How do I pause everything?** Menu → “Pause automatic optimization”, or switch off watching the clipboard / folders.
**Privacy.** Everything happens locally. The only network requests are update checks (Sparkle) and, when you click it, opening a GitHub page.
