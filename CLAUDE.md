# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static single-page showcase website for perler bead (拼豆) artwork. No build tools, no frameworks — pure HTML/CSS/JS served via GitHub Pages.

## Repository structure

```
/
├── index.html       # Entire application (CSS in <style>, JS in <script>)
├── posts.json       # {_meta: {aboutText, profileName, profileBio, profileAvatar, exportedAt}, posts: [...]}
├── images/          # Legacy image storage (not needed when using drag-and-drop)
├── music/           # Background music .mp3 files
└── README.md        # Deployment and usage instructions (Chinese)
```

## Architecture (index.html)

**Theming** — 5 themes (sakura, mint, sky, lavender, peach) implemented via CSS custom properties on `:root`. Theme switching toggles `[data-theme]` on `<body>`, which remaps all `--accent`, `--bg`, `--card-bg`, etc. variables.

**Data flow** — `loadPosts()` checks localStorage (`pindou_posts` key) first, falls back to `fetch('posts.json')`. Supports two JSON formats:
- New: `{_meta: {aboutText, ...}, posts: [...]}` — meta is synced to `settings`
- Old: `[...]` — plain array, still supported for backward compatibility

Export always produces the new format with `_meta` containing `aboutText`, `profileName`, `profileBio`, `profileAvatar` from settings. `syncMeta()` merges `_meta` fields from loaded JSON into settings — used both on initial load and when importing.

**Admin mode** — Triggered by clicking the header title 5 times within 2 seconds (`ADMIN_CLICKS = 5`). No visible hints are shown to visitors. Toggles `isAdmin` flag, which reveals: FAB new-post button, export button, per-post edit/delete buttons, about/profile edit buttons, and a slide-out admin panel overlay. Avatar becomes clickable in admin mode.

**Image handling** — Images are dragged into a drop zone in the post editor. `handleDroppedFiles()` reads files via FileReader, resizes them (max 800px, JPEG quality 0.75) via `<canvas>`, and stores as data URLs in `droppedImages[]`. On save, `droppedImages[].dataUrl` becomes the post's `images[]` array. `renderPostCard()` detects `data:` prefix vs filename paths.

**Post rendering** — `renderPostCard()` builds HTML strings. Image grid is always 4 columns (`grid-template-columns: repeat(4, 1fr)`), each cell square (`aspect-ratio: 1`). Extra images wrap to new rows. Responsive: drops to 3 columns on mobile.

**Profile section** — Sidebar card with square avatar (64px), name, and bio. Avatar uses drag-and-drop zone (same `resizeImage()` pipeline). All profile fields stored in `settings`, synced via `_meta` in posts.json.

**About section** — Editable in admin mode via sidebar pencil button. Text stored in `settings.aboutText`, persisted to localStorage, and exported in `posts.json` `_meta.aboutText`.

**Music player** — Floating button at bottom-right. First click loads track and shows panel; subsequent clicks toggle play/pause. Tracks defined in `musicPlaylist` array (hardcoded default, overridable via localStorage `pindou_playlist`).

## Key localStorage keys

| Key | Content |
|-----|---------|
| `pindou_posts` | JSON — either a posts array (old) or full `{_meta, posts}` object (new) |
| `pindou_settings` | `{theme, musicPlaying, currentTrack, aboutText, profileName, profileBio, profileAvatar}` |
| `pindou_playlist` | Custom music track list `[{name, src}]` |

## Common tasks

**Add a new theme** — Add a `[data-theme="name"]` block in CSS remapping the color variables, then add a `.theme-dot.name` swatch in the sidebar HTML with matching `data-theme` attribute.

**Modify the post data schema** — Update `savePost()` (form→object mapping), `renderPostCard()` (object→HTML rendering), and the `posts.json` example file. Tags are split from comma-separated string to array on save.

**Test locally** — Open `index.html` directly in a browser or serve via `python -m http.server`. `posts.json` is loaded via `fetch()`, which works with `file://` in most browsers.

**Deploy** — Push to GitHub, enable Pages on main branch, root directory. Site is at `https://<username>.github.io/<repo>/`.
