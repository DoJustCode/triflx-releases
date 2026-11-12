# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions are numbered `major.minor.patch`. [Русская версия](CHANGELOG.md)

## [2.3.0] — 2026-11-12

### Added
- **Try**: a window that compares one image in 15 variants (quality 70/80/90 for the original format, WebP, AVIF, JPEG XL, lossless modes) with real sizes and a before/after slider. A card button, the menu, the Finder menu, ⌃⇧V, `triflx try`.
- **Profiles by source**: rules by folder, app (clipboard), screenshots, source site and part of the name (format, quality, scale, metadata, size limit, “leave alone”).
- **“Fit into N MB”** for images, video and PDF: quality, scale, a resolution ladder and dpi are chosen for you; a note when the target is unreachable. The card, presets (25 MB email, 10 MB Telegram, custom), the batch window, Shortcuts, `--max-size`.
- **Statistics**: total, month, week, today, breakdowns by type, source and folder, a top-savings ranking, a switch and reset; the week total in the menu; `triflx stats`.
- **Dropping files on the menu-bar icon** opens the batch window with one-time settings (⌥ — compress right away, ⌘ — strong compression).
- **Configurable hotkeys**, including “optimize the Finder selection”, OCR (⌃⇧T), “Try” (⌃⇧V); a hint about Finder access.
- **History and rollback of originals**: “don’t keep”, “N days” and “up to a size limit” modes; auto-cleanup; the History & originals window (24 hours, 7 days, selective); used space and “Clear now”.
- **Safe preview** before replacing a file (Replace / Keep original / Save a “.min” copy), off by default.
- **Processing protection**: lists of names, paths and types (`.git`, Xcode, `node_modules`, Adobe caches, Photos libraries, system folders, iCloud files not yet downloaded); automation skips them, manual actions warn; `--force` in the terminal.
- **Watermark**: text or image, position, size, opacity, font, shadow, margin, preview; separate for automation, presets and manual actions.
- **Documents**: HEIC/RAW → JPEG/PNG, PDF → images, images → PDF, merge and split PDF; `triflx convert`.
- **Background removal** (macOS 14+) and **size templates** (marketplace, Instagram, story, Open Graph and your own; “Fit”, “Fill”, “Smart crop”).
- **Text recognition (OCR)** for images, screenshots and PDFs: clipboard or `.txt`, language choice, an “on clipboard screenshots” option; `triflx ocr`.
- A **“triflX…”** submenu in the Finder menu; seven new Shortcuts actions (Fit File to Size, Resize to Template, Remove Background, Recognize Text, PDF to Images, Images to PDF, Merge PDFs).
- Terminal and MCP: `--template`, `--remove-bg`, `--lossless`, `--quality 1..100`, `--watermark`, `--force`, commands `ocr`, `remove-bg`, `try`, `stats`, `convert`, `selftest`.
- Eight new Settings tabs (searchable), Russian and English strings for everything new, 90 built-in checks (`triflx selftest`).

### Changed
- A video size limit is now reached by stepping the resolution down rather than by cutting the duration.
- Backups: three modes instead of “keep N days” (the setting was migrated automatically).

## [2.2.0] — 2026-11-11

### Added
- **Built-in ffmpeg converter** (LGPL): MKV, WebM, AVI, TS, FLV, WMV, OGG, Opus, WMA, APE.
- **Finder menu**: “Optimize with triflX” and “Preset for selection”.
- **Cancel** for compression: a button on the card before it starts (the pause before auto-processing is configurable) and during compression; the original is not changed.
- **Platform presets** (Telegram, Instagram, web, email, Slack/Discord and your own).
- **Before/after comparison** on the card; a **batch window** with settings, progress, cancel and “restore originals”.
- The **“already optimized” mark**, **processing of existing files** and a night-time background mode.
- A “Recent results” menu, a configurable card display time.

### Fixed
- Folder watching: detecting new files, files renamed by the screenshot sorter.
- Thread-safe settings for background threads.

## [2.1.0] — 2026-11-11

### Added
- Compatibility auto-conversion (AVIF/HEIC/WebP → JPEG/PNG, MOV etc. → MP4), quick-action zones, the `--mp4` option.

### Fixed
- Atomic file writes, names that don’t overwrite, corrupt files, TIFF and BMP, CLI and MCP parameter validation, clipboard handling, GIF.

## [2.0.0] — 2026-11-11

### Added
- The first triflX release: an Xcode project, native Shortcuts actions (App Intents), all of Trifl 1.4’s functionality (clipboard, folders, filters, video, GIF, PDF, audio, WebP, AVIF, JPEG XL, metadata, hotkeys, Sparkle updates, Russian and English UI).
- A universal build (Apple Silicon and Intel), signing and notarization, the `triflx` command and an MCP server.

[2.3.0]: https://github.com/DoJustCode/triflx-releases/releases/tag/v2.3.0
[2.2.0]: https://github.com/DoJustCode/triflx-releases/releases/tag/v2.2.0
[2.1.0]: https://github.com/DoJustCode/triflx-releases/releases/tag/v2.1.0
[2.0.0]: https://github.com/DoJustCode/triflx-releases/releases/tag/v2.0.0
