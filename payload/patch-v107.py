from pathlib import Path

p = Path('/tmp/mosaic-src/mosaic-notes/app/src/main/assets/index.html')
s = p.read_text()

# v1.0.6 accidentally left the desktop toolbar's `top:0` active while also
# setting bottom:0 on mobile. A fixed element with both top and bottom set
# stretched over the entire viewport, invisibly intercepting editor scrolling.
old_toolbar = '.toolbar{order:3;position:fixed;left:0;right:0;bottom:0;flex:0 0 auto;z-index:80;'
new_toolbar = '.toolbar{order:3;position:fixed;left:0;right:0;top:auto;bottom:0;height:auto;max-height:68px;flex:0 0 auto;z-index:80;'
if old_toolbar not in s:
    raise SystemExit('v1.0.7 toolbar anchor missing')
s = s.replace(old_toolbar, new_toolbar, 1)

# Keep the mobile editor layout in landscape on touch-style/mobile viewports.
old_media = '@media(max-width:700px){'
new_media = '@media(max-width:700px), (max-height:500px) and (hover:none){'
if old_media not in s:
    raise SystemExit('v1.0.7 mobile media anchor missing')
s = s.replace(old_media, new_media, 1)

p.write_text(s)
(Path('/tmp/mosaic-src/mosaic-notes/index.html')).write_text(s)
