from pathlib import Path
import sys
p=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/mosaic-src/mosaic-notes/app/src/main/assets/index.html')
s=p.read_text()

# Desktop editor/search redesign.
css = r'''
@media(min-width:901px){
  #app{--sidebar-w:248px}
  #app.desktopWide{grid-template-columns:minmax(0,1fr)}
  .topbar .searchWrap{display:none}
  .topActions{margin-left:auto}
  .desktopNav{padding:18px 12px 28px 16px}
  .desktopSearch{display:flex;align-items:center;gap:9px;height:42px;margin:0 4px 18px;padding:0 11px;border:1px solid #ffffff12;border-radius:11px;background:#161619;color:#92929b}
  .desktopSearch:focus-within{border-color:#ffffff25;background:#18181b}
  .desktopSearch input{min-width:0;flex:1;border:0;outline:0;background:transparent;color:#f2f2f5;font:inherit;font-size:14px}
  .desktopSearch button{width:27px;height:27px;border:0;border-radius:8px;background:transparent;color:#999;display:grid;place-items:center;cursor:pointer;padding:0}
  .desktopSearch button:hover{background:#ffffff0b;color:#fff}
  .desktopSearch .icon{width:17px;height:17px}
  .desktopNavHead{padding-top:2px}

  /* Page title and status live at the top of the sidebar on desktop. The DOM
     remains in the editor so mobile can use the same controls without clones. */
  #app.desktopEditor .desktopNav{padding-top:142px}
  #app.desktopEditor .editorHead{position:fixed;z-index:55;left:0;top:72px;width:var(--sidebar-w);height:124px;box-sizing:border-box;padding:20px 20px 15px;background:#1d1d20;border-right:1px solid #ffffff0d;border-bottom:1px solid #ffffff0d}
  #app.desktopEditor .titleInput{font-size:21px;line-height:1.2;letter-spacing:-.025em;padding:0;width:100%;white-space:nowrap;text-overflow:ellipsis;overflow:hidden}
  #app.desktopEditor .editorMeta{margin-top:9px;gap:6px;flex-wrap:wrap;line-height:1.35}
  #app.desktopEditor .editorMeta .metaDot{display:none}
  #app.desktopEditor .saveState{width:100%}

  /* The editor is now the workspace itself, not a card floating inside one. */
  .main.editorMode{padding:0;overflow:hidden;background:#202023}
  .main.editorMode .editorShell{max-width:none;width:100%;height:100%;margin:0;border:0;border-radius:0;box-shadow:none;background:#202023}
  .main.editorMode .editorAccent{height:4px}
  .main.editorMode .toolbar{position:sticky;top:0;z-index:8;padding:9px clamp(28px,3vw,52px);border-top:0;border-bottom:1px solid #ffffff10;background:#1b1b1e;box-shadow:0 1px 0 #0004}
  .main.editorMode .editor{width:100%;box-sizing:border-box;min-height:0;padding:42px clamp(42px,6vw,96px) 120px;font-size:18px;line-height:1.74;scroll-padding-top:70px}
  .main.editorMode .editor>*,.main.editorMode .editor>div:not(.html-embed-wrap),.main.editorMode .editor p,.main.editorMode .editor ul,.main.editorMode .editor ol,.main.editorMode .editor blockquote,.main.editorMode .editor .todo-item{max-width:1080px}
  .main.editorMode .html-embed-wrap,.main.editorMode .editor img{max-width:1180px}
}
@media(min-width:901px) and (max-width:1180px){
  #app{--sidebar-w:218px}
  #app.desktopEditor .editorHead{padding-inline:16px}
  .main.editorMode .toolbar{padding-inline:28px}
  .main.editorMode .editor{padding-inline:44px}
}
'''
anchor='@media(max-width:700px), (max-height:500px) and (hover:none){'
if anchor not in s: raise SystemExit('v109 mobile CSS anchor missing')
s=s.replace(anchor,css+'\n'+anchor,1)

# Mobile must explicitly reset desktop-only editor-head positioning.
mobile_head='.editorHead{padding:18px 18px 10px;order:1;flex:0 0 auto}'
mobile_head_new='.editorHead{position:static!important;width:auto!important;height:auto!important;padding:18px 18px 10px!important;order:1;flex:0 0 auto;border:0!important;background:transparent!important}'
if mobile_head not in s: raise SystemExit('v109 mobile editor head anchor missing')
s=s.replace(mobile_head,mobile_head_new,1)

# Replace desktop nav renderer: sidebar is always present on desktop and owns search.
start=s.index('function renderDesktopNav(){')
end=s.index('\nfunction render(){',start)
new_func=r'''function desktopSearchHTML(){return `<div class="desktopSearch"><span><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/></svg></span><input id="desktopSearchInput" value="${esc(searchInput.value)}" placeholder="Search notes" autocomplete="off" aria-label="Search notes"><button id="desktopClearSearch" class="${searchInput.value?'':'hidden'}" title="Clear search" aria-label="Clear search"><svg class="icon" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>`}
function bindDesktopSearch(){const inp=$('#desktopSearchInput'),clear=$('#desktopClearSearch');if(!inp)return;inp.addEventListener('input',()=>{const pos=inp.selectionStart??inp.value.length;searchInput.value=inp.value;clearSearch.classList.toggle('hidden',!inp.value);render();requestAnimationFrame(()=>{const n=$('#desktopSearchInput');if(n){n.focus();try{n.setSelectionRange(pos,pos)}catch{}}})});if(clear)clear.onclick=()=>{searchInput.value='';clearSearch.classList.add('hidden');render();requestAnimationFrame(()=>$('#desktopSearchInput')?.focus())}}
function renderDesktopNav(){if(!desktopNav||!state)return;app.classList.remove('desktopWide');app.classList.toggle('desktopEditor',view.type==='editor'&&!searchInput.value.trim());let kicker='',title='',items=[],addLabel='',addType='';if(view.type==='home'){kicker='Notebooks';title='All notebooks';items=liveValues(state.notebooks).sort((a,b)=>(b.updatedAt||0)-(a.updatedAt||0)).map(n=>desktopNavItem(n,'notebook',false,{type:'sections',notebookId:n.id}));addLabel='+ New notebook';addType='notebook'}else if(view.type==='sections'){kicker='Notebooks';title='All notebooks';items=liveValues(state.notebooks).sort((a,b)=>(b.updatedAt||0)-(a.updatedAt||0)).map(n=>desktopNavItem(n,'notebook',n.id===view.notebookId,{type:'sections',notebookId:n.id}));addLabel='+ New notebook';addType='notebook'}else if(view.type==='pages'){const n=state.notebooks[view.notebookId];kicker='Sections';title=n?.title||'Notebook';items=liveValues(state.sections).filter(x=>x.notebookId===view.notebookId).sort((a,b)=>(a.order||0)-(b.order||0)||(b.updatedAt||0)-(a.updatedAt||0)).map(x=>desktopNavItem(x,'section',x.id===view.sectionId,{type:'pages',notebookId:view.notebookId,sectionId:x.id}));addLabel='+ New section';addType='section'}else if(view.type==='editor'){const sec=state.sections[view.sectionId],n=state.notebooks[view.notebookId];kicker=n?.title||'Pages';title=sec?.title||'Pages';items=liveValues(state.pages).filter(x=>x.sectionId===view.sectionId).sort((a,b)=>(b.updatedAt||0)-(a.updatedAt||0)).map(x=>desktopNavItem(x,'page',x.id===view.pageId,{type:'editor',notebookId:view.notebookId,sectionId:view.sectionId,pageId:x.id}));addLabel='+ New page';addType='page'}desktopNav.innerHTML=`${desktopSearchHTML()}<div class="desktopNavHead"><div class="desktopNavKicker">${esc(kicker)}</div><div class="desktopNavTitle">${esc(title)}</div></div><div class="desktopNavList">${items.join('')}</div>${addType?`<button class="desktopNavAdd" data-add="${addType}">${addLabel}</button>`:''}`;bindDesktopSearch();desktopNav.querySelectorAll('[data-nav]').forEach(b=>b.onclick=()=>{try{setView(JSON.parse(b.dataset.nav))}catch{}});const add=desktopNav.querySelector('[data-add]');if(add)add.onclick=()=>createEntity(add.dataset.add)}'''
s=s[:start]+new_func+s[end:]

# Search state no longer makes desktop wide/full-screen.
s=s.replace("const searching=!!searchInput.value.trim(),wide=view.type==='home'||searching;app.classList.toggle('desktopWide',wide);if(wide){desktopNav.innerHTML='';return}","")

# Global Escape follows the same hierarchy as the back button. Search/menu/modal
# consume Escape first, which keeps the shortcut predictable rather than destructive.
back="backBtn.onclick=()=>{if(view.type==='editor')setView({type:'pages',notebookId:view.notebookId,sectionId:view.sectionId});else if(view.type==='pages')setView({type:'sections',notebookId:view.notebookId});else if(view.type==='sections')setView({type:'home'})};"
if back not in s: raise SystemExit('v109 back handler anchor missing')
replacement=back+r'''
function goUpOneLevel(){if(view.type==='editor')setView({type:'pages',notebookId:view.notebookId,sectionId:view.sectionId});else if(view.type==='pages')setView({type:'sections',notebookId:view.notebookId});else if(view.type==='sections')setView({type:'home'})}
backBtn.onclick=goUpOneLevel;
document.addEventListener('keydown',e=>{if(e.key!=='Escape'||e.defaultPrevented)return;if(modalShade.classList.contains('show')){e.preventDefault();closeModal();return}if(menuPop.classList.contains('show')){e.preventDefault();menuPop.classList.remove('show');return}if(searchInput.value){e.preventDefault();searchInput.value='';clearSearch.classList.add('hidden');render();return}if(view.type!=='home'){e.preventDefault();goUpOneLevel()}});'''
s=s.replace(back,replacement,1)

# The replacement above leaves the old anonymous back assignment immediately before
# goUpOneLevel, so remove it to avoid two handlers in source (the latter would win,
# but duplicated behavior is how software grows moss).
s=s.replace(back+'\nfunction goUpOneLevel', 'function goUpOneLevel',1)

p.write_text(s)
