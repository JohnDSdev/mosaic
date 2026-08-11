from pathlib import Path
p=Path('/tmp/mosaic-src/mosaic-notes/app/src/main/assets/index.html')
s=p.read_text()
changes=[
('.main{flex:1;overflow:auto;overscroll-behavior-y:contain;','.main{flex:1;min-height:0;overflow:auto;overscroll-behavior-y:contain;'),
('#app{height:100%}','#app{height:100%;min-height:0}'),
('.main{padding:16px 14px}','.main{padding:16px 14px;min-height:0}.main.editorMode{padding:0;overflow:hidden;min-height:0}'),
('.editorShell{border-radius:0;border-left:0;border-right:0;margin:-16px -14px;height:calc(100% + 32px);overscroll-behavior:none}','.editorShell{border-radius:0;border:0;margin:0;height:100%;min-height:0;box-shadow:none;overscroll-behavior:none}'),
('.editorHead{padding:18px 18px 10px;order:1}','.editorHead{padding:18px 18px 10px;order:1;flex:0 0 auto}'),
('.editor{order:2;padding:22px 19px 24px;font-size:17px;scroll-padding-bottom:24px;overscroll-behavior-y:contain}','.editor{order:2;min-height:0;padding:22px 19px calc(92px + env(safe-area-inset-bottom,0px));font-size:17px;scroll-padding-bottom:calc(92px + env(safe-area-inset-bottom,0px));overflow-y:auto;overscroll-behavior-y:contain;-webkit-overflow-scrolling:touch}'),
('.toolbar{order:3;position:static;flex:0 0 auto;z-index:4;padding:8px 10px;gap:4px;overflow-x:auto;flex-wrap:nowrap;border-top:1px solid #ffffff18;border-bottom:0;background:#1b1b1ef7;box-shadow:0 -8px 26px #0004;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);scrollbar-width:none;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}','.toolbar{order:3;position:fixed;left:0;right:0;bottom:0;flex:0 0 auto;z-index:80;padding:8px 10px calc(8px + env(safe-area-inset-bottom,0px));gap:4px;overflow-x:auto;flex-wrap:nowrap;border-top:1px solid #ffffff18;border-bottom:0;background:#1b1b1ef7;box-shadow:0 -8px 26px #0004;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);scrollbar-width:none;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}')]
for old,new in changes:
    if old not in s: raise SystemExit('v106 anchor missing: '+old[:60])
    s=s.replace(old,new,1)
p.write_text(s)
Path('/tmp/mosaic-src/mosaic-notes/index.html').write_text(s)
