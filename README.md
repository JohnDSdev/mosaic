# Mosaic Notes

A single-file, local-first notes app with a simple OneNote-like hierarchy:

**Notebooks → Sections → Pages**

The exact same `index.html` is embedded in the Android WebView app and can also be opened directly from disk in a modern desktop browser.

## Features

- notebook / section / page hierarchy
- per-item accent colors
- rich-text pages: bold, italic, bullets, numbered lists, links, checklists
- URLs pasted into the editor become links
- embedded images (resized locally before storage)
- sandboxed HTML embeds
- search
- offline-first local storage
- encrypted Cloudinary sync using AES-256-GCM
- random 256-bit recovery key; Cloudinary cloud name is never treated as a secret
- immutable numbered Cloudinary snapshots to avoid silent overwrites
- conflict preservation: conflicting page edits are kept as a separate `(... sync conflict)` page
- full JSON export/import
- Android backup export through the system file picker

## Cloudinary setup

Create an **unsigned** upload preset named:

`mosaic_notes`

The preset must permit request-supplied `public_id` values and must not overwrite existing assets. Mosaic uploads small encrypted JSON snapshots through Cloudinary's `raw/upload` endpoint.

Recommended preset limits:

- unsigned
- overwrite disabled
- allow request-supplied public IDs (`disallow_public_id` must be off)
- limit maximum file size to something reasonable for your notes
- if you restrict formats, allow JSON/raw uploads

The cloud name and preset name are public identifiers. Privacy comes from the randomly generated vault key, not from hiding Cloudinary identifiers.

## Desktop website

Just open `index.html` directly in a modern browser. No server is required.

For the most reliable local persistence, use the same file path and browser profile each time. The app prefers IndexedDB and falls back to localStorage.

## Android APK with GitHub Actions

Push this repository to GitHub and open **Actions → Build Android APK → Run workflow**. The workflow uploads an installable debug APK named `mosaic-notes-apk`.

The Android app is intentionally a thin native WebView shell around the exact same single-file web app, plus native file saving/opening support.

## Security notes

Cloudinary receives encrypted snapshots. Snapshot contents use AES-GCM with a fresh nonce and a random 256-bit vault key. The cloud name is not part of the encryption secret.

An unsigned Cloudinary preset cannot authenticate who is uploading, so someone who discovers the cloud name and preset could potentially consume upload quota. This architecture protects note confidentiality and avoids overwriting existing snapshots, but it cannot prevent upload spam without a server-side authenticated component.

HTML embeds are rendered in sandboxed iframes with scripts/forms allowed but without same-origin access to the parent app.
