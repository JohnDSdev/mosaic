from pathlib import Path
import sys
path=Path(sys.argv[1])
s=path.read_text()

# Bring the original source up to the cleaned-up v1.0.3 Android UI first.
# These replacements are conditional so the patch is also safe on an already-updated file.
if 'body{overflow:hidden}' in s:
    s=s.replace('body{overflow:hidden}','body{overflow:hidden;padding-top:env(safe-area-inset-top,0px);padding-right:env(safe-area-inset-right,0px);padding-bottom:env(safe-area-inset-bottom,0px);padding-left:env(safe-area-inset-left,0px)}',1)
s=s.replace('padding:12px max(14px,env(safe-area-inset-right)) 12px max(14px,env(safe-area-inset-left));','padding:12px 14px;')
s=s.replace('bottom:max(24px,env(safe-area-inset-bottom));','bottom:max(24px,calc(env(safe-area-inset-bottom,0px) + 12px));')
s=s.replace('button,input,textarea{font:inherit}button{color:inherit}', 'button,input,textarea{font:inherit}button{color:inherit;-webkit-tap-highlight-color:transparent}button:focus,button:focus-visible{outline:none;box-shadow:none}',1)
s=s.replace('.iconbtn{width:44px;height:44px;border:0;border-radius:15px;background:transparent;display:grid;place-items:center;cursor:pointer;font-size:22px}.iconbtn:hover{background:#ffffff0d}', '.iconbtn{width:44px;height:44px;border:0;border-radius:15px;background:transparent;display:grid;place-items:center;cursor:pointer;color:#f3f5fb;-webkit-tap-highlight-color:transparent;transition:background .14s ease,transform .12s ease}.iconbtn:hover{background:#ffffff0d}.iconbtn:active{background:#ffffff12;transform:scale(.97)}.iconbtn:focus,.iconbtn:focus-visible{outline:none;box-shadow:none}.icon{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}.iconFill{fill:currentColor;stroke:none}',1)
s=s.replace('.tool{min-width:38px;height:38px;padding:0 10px;border:0;border-radius:11px;background:transparent;cursor:pointer;font-weight:650}.tool:hover{background:#ffffff10}', '.tool{width:42px;min-width:42px;height:42px;padding:0;border:0;border-radius:13px;background:transparent;cursor:pointer;font-weight:650;display:inline-flex;align-items:center;justify-content:center;color:#f3f5fb;-webkit-tap-highlight-color:transparent;transition:background .14s ease,transform .12s ease}.tool:hover{background:#ffffff10}.tool:active{background:#ffffff14;transform:scale(.97)}.tool:focus,.tool:focus-visible{outline:none;box-shadow:none}',1)
back='<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 18l-6-6 6-6"/><path d="M9 12h8"/></svg>'
search='<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/></svg>'
sync='<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6v5h-5"/><path d="M4 18v-5h5"/><path d="M19 11a7 7 0 0 0-12-3"/><path d="M5 13a7 7 0 0 0 12 3"/></svg>'
dots='<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><circle class="iconFill" cx="12" cy="5" r="1.7"/><circle class="iconFill" cx="12" cy="12" r="1.7"/><circle class="iconFill" cx="12" cy="19" r="1.7"/></svg>'
close='<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
plus='<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" style="width:25px;height:25px"><path d="M12 5v14M5 12h14"/></svg>'
s=s.replace('<button class="iconbtn" id="backBtn" title="Back" aria-label="Back">‹</button>',f'<button class="iconbtn" id="backBtn" title="Back" aria-label="Back">{back}</button>')
s=s.replace('<div class="searchWrap"><span>⌕</span><input id="searchInput" placeholder="Search notes" autocomplete="off"><button class="iconbtn hidden" id="clearSearch" style="width:32px;height:32px" aria-label="Clear search">×</button></div>',f'<div class="searchWrap"><span style="display:grid;place-items:center;color:#aaa">{search}</span><input id="searchInput" placeholder="Search notes" autocomplete="off"><button class="iconbtn hidden" id="clearSearch" style="width:32px;height:32px" aria-label="Clear search">{close}</button></div>')
s=s.replace('<button class="iconbtn hideMobile" id="syncBtn" title="Sync now" aria-label="Sync now">↻</button>',f'<button class="iconbtn hideMobile" id="syncBtn" title="Sync now" aria-label="Sync now">{sync}</button>')
s=s.replace('<button class="iconbtn" id="settingsBtn" title="Settings" aria-label="Settings">⋮</button>',f'<button class="iconbtn" id="settingsBtn" title="Settings" aria-label="Settings">{dots}</button>')
s=s.replace('<button class="fab" id="fab" aria-label="Add">+</button>',f'<button class="fab" id="fab" aria-label="Add">{plus}</button>')

path.write_text(s)
print("prepatched", path)
