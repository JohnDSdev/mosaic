from pathlib import Path
p=Path('/tmp/mosaic-src/mosaic-notes/app/src/main/assets/index.html')
s=p.read_text()

# Initial wide layout keeps setup/search centered before a vault is loaded.
s=s.replace('<div id="app">','<div id="app" class="desktopWide">',1)
# Insert desktop navigation rail.
s=s.replace('  <main class="main" id="main"></main>', '  <aside class="desktopNav" id="desktopNav" aria-label="Notebook navigation"></aside>\n  <main class="main" id="main"></main>',1)

# Desktop styling: navigation rail, denser cards, proper document/editor proportions.
insert_css=r'''
@media(min-width:901px){
  #app{display:grid;grid-template-columns:248px minmax(0,1fr);grid-template-rows:72px minmax(0,1fr);height:100%}
  #app.desktopWide{grid-template-columns:minmax(0,1fr)}
  .topbar{grid-column:1/-1;grid-row:1;height:72px;padding:10px 22px;gap:10px;box-shadow:0 1px 0 #0003;z-index:40}
  .brand{font-size:16px;min-width:64px}.crumb{gap:7px}.crumb span{max-width:260px}.searchWrap{height:46px;max-width:760px;border-radius:18px;background:#252528}.searchWrap input{font-size:16px}
  .desktopNav{grid-column:1;grid-row:2;min-width:0;overflow:auto;padding:22px 12px 28px 16px;background:#1d1d20;border-right:1px solid #ffffff0d;scrollbar-width:thin;scrollbar-color:#ffffff18 transparent}
  .desktopWide .desktopNav{display:none}.desktopWide .main{grid-column:1;grid-row:2;padding-inline:max(30px,calc((100vw - 1420px)/2))}
  .main{grid-column:2;grid-row:2;min-width:0;padding:28px max(28px,calc((100vw - 248px - 1360px)/2));scrollbar-gutter:stable both-edges}
  .desktopNavHead{padding:0 10px 14px}.desktopNavKicker{font-size:11px;line-height:1;text-transform:uppercase;letter-spacing:.11em;color:#7f7f88;font-weight:750}.desktopNavTitle{font-size:20px;font-weight:780;letter-spacing:-.035em;margin-top:7px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.desktopNavList{display:grid;gap:4px}.desktopNavItem{position:relative;width:100%;min-height:48px;border:0;border-radius:13px;background:transparent;color:#d8d8df;padding:8px 10px 8px 13px;display:flex;align-items:center;gap:10px;text-align:left;cursor:pointer;transition:background .12s ease,color .12s ease}.desktopNavItem:hover{background:#ffffff0a;color:#fff}.desktopNavItem.active{background:#ffffff0f;color:#fff}.desktopNavItem.active:before{content:"";position:absolute;left:0;top:10px;bottom:10px;width:3px;border-radius:999px;background:var(--nav-accent,var(--accent))}.desktopNavDot{width:9px;height:9px;border-radius:3px;flex:0 0 auto;background:var(--nav-accent,#777)}.desktopNavCopy{min-width:0;flex:1}.desktopNavName{font-size:14px;font-weight:680;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.desktopNavMeta{font-size:11px;color:#85858f;margin-top:2px}.desktopNavAdd{width:calc(100% - 8px);margin:14px 4px 0;border:1px solid #ffffff12;border-radius:13px;background:#ffffff06;color:#bdbdc6;padding:10px 12px;cursor:pointer;text-align:left;font-weight:650}.desktopNavAdd:hover{background:#ffffff0c;color:#fff}
  .pageTitleRow{margin:4px 2px 22px}.pageTitleRow h1{font-size:32px}.subtitle{font-size:13px}.grid{grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:15px;align-content:start;padding-bottom:90px}.card{min-height:164px;padding:19px;border-radius:19px;box-shadow:0 1px 0 #0003;transition:transform .14s ease,border-color .14s ease,box-shadow .14s ease}.card:hover{transform:translateY(-2px);border-color:#ffffff2e;box-shadow:0 10px 28px #0002}.cardTitle{font-size:19px}.cardPreview{font-size:14px;max-height:62px;margin-top:15px}.fab{width:58px;height:58px;border-radius:18px;right:28px;bottom:28px}
  .main.editorMode{padding:22px 26px;overflow:hidden}.editorShell{max-width:1060px;border-radius:22px;box-shadow:0 16px 44px #0004}.editorAccent{height:6px}.editorHead{padding:24px 34px 15px}.titleInput{font-size:38px;line-height:1.12}.editorMeta{margin-top:8px}.toolbar{padding:8px 26px;gap:4px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}.toolbar::-webkit-scrollbar{display:none}.tool{width:38px;min-width:38px;height:38px;border-radius:10px}.tool.sep{margin-left:10px}.editor{min-height:0;padding:36px 52px 110px;font-size:18px;line-height:1.72;scroll-padding-top:24px}.editor>*,.editor>div:not(.html-embed-wrap){max-width:820px}.editor p,.editor ul,.editor ol,.editor blockquote,.editor .todo-item{max-width:820px}.html-embed-wrap,.editor img{max-width:900px}
  .modal{border-radius:22px}.toast{bottom:24px}
}
@media(min-width:901px) and (max-width:1180px){
  #app{grid-template-columns:218px minmax(0,1fr)}.main{padding-inline:22px}.desktopNav{padding-left:10px}.crumb span{max-width:150px}.searchWrap{max-width:520px}.editor{padding-inline:38px}.titleInput{font-size:34px}
}
@media(min-width:1500px){.grid{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}.main.editorMode{padding-top:28px;padding-bottom:28px}}
'''
anchor='@media(max-width:700px), (max-height:500px) and (hover:none){'
if anchor not in s: raise SystemExit('mobile anchor missing')
s=s.replace(anchor,insert_css+'\n'+anchor,1)

# Capture app/nav refs.
s=s.replace("const main=$('#main'), fab=$('#fab'), backBtn=$('#backBtn'), crumb=$('#crumb'), searchInput=$('#searchInput'), clearSearch=$('#clearSearch');",
            "const app=$('#app'), main=$('#main'), desktopNav=$('#desktopNav'), fab=$('#fab'), backBtn=$('#backBtn'), crumb=$('#crumb'), searchInput=$('#searchInput'), clearSearch=$('#clearSearch');",1)

# Add desktop nav helpers before render().
render_anchor="function render(){if(!state)return;"
helpers=r'''function navCount(type,id){if(type==='notebook')return liveValues(state.sections).filter(x=>x.notebookId===id).length;if(type==='section')return liveValues(state.pages).filter(x=>x.sectionId===id).length;return 0}
function desktopNavItem(item,type,active,target){const count=navCount(type,item.id),unit=type==='notebook'?'section':type==='section'?'page':'',meta=type==='page'?'Page':`${count} ${unit}${count===1?'':'s'}`;return `<button class="desktopNavItem ${active?'active':''}" style="--nav-accent:${item.color||'#7c9cff'}" data-nav='${esc(JSON.stringify(target))}'><span class="desktopNavDot"></span><span class="desktopNavCopy"><span class="desktopNavName">${esc(item.title||'Untitled')}</span><span class="desktopNavMeta">${esc(meta)}</span></span></button>`}
function renderDesktopNav(){if(!desktopNav||!state)return;const searching=!!searchInput.value.trim(),wide=view.type==='home'||searching;app.classList.toggle('desktopWide',wide);if(wide){desktopNav.innerHTML='';return}let kicker='',title='',items=[],addLabel='',addType='';if(view.type==='sections'){kicker='Notebooks';title='Your notes';items=liveValues(state.notebooks).sort((a,b)=>(b.updatedAt||0)-(a.updatedAt||0)).map(n=>desktopNavItem(n,'notebook',n.id===view.notebookId,{type:'sections',notebookId:n.id}));addLabel='+ New notebook';addType='notebook'}else if(view.type==='pages'){const n=state.notebooks[view.notebookId];kicker='Sections';title=n?.title||'Notebook';items=liveValues(state.sections).filter(x=>x.notebookId===view.notebookId).sort((a,b)=>(a.order||0)-(b.order||0)||(b.updatedAt||0)-(a.updatedAt||0)).map(x=>desktopNavItem(x,'section',x.id===view.sectionId,{type:'pages',notebookId:view.notebookId,sectionId:x.id}));addLabel='+ New section';addType='section'}else if(view.type==='editor'){const sec=state.sections[view.sectionId],n=state.notebooks[view.notebookId];kicker=n?.title||'Pages';title=sec?.title||'Pages';items=liveValues(state.pages).filter(x=>x.sectionId===view.sectionId).sort((a,b)=>(b.updatedAt||0)-(a.updatedAt||0)).map(x=>desktopNavItem(x,'page',x.id===view.pageId,{type:'editor',notebookId:view.notebookId,sectionId:view.sectionId,pageId:x.id}));addLabel='+ New page';addType='page'}desktopNav.innerHTML=`<div class="desktopNavHead"><div class="desktopNavKicker">${esc(kicker)}</div><div class="desktopNavTitle">${esc(title)}</div></div><div class="desktopNavList">${items.join('')}</div>${addType?`<button class="desktopNavAdd" data-add="${addType}">${addLabel}</button>`:''}`;desktopNav.querySelectorAll('[data-nav]').forEach(b=>b.onclick=()=>{try{setView(JSON.parse(b.dataset.nav))}catch{}});const add=desktopNav.querySelector('[data-add]');if(add)add.onclick=()=>createEntity(add.dataset.add)}
'''
if render_anchor not in s: raise SystemExit('render anchor missing')
s=s.replace(render_anchor,helpers+render_anchor,1)
# Call desktop navigation early in render.
s=s.replace("function render(){if(!state)return;crumb.innerHTML=crumbs();", "function render(){if(!state)return;crumb.innerHTML=crumbs();renderDesktopNav();",1)

# Final responsive safeguards and sidebar typography.
s=s.replace('.main.editorMode{overflow:hidden;overscroll-behavior:none}::highlight(mosaic-spelling)', '.main.editorMode{overflow:hidden;overscroll-behavior:none}.desktopNav{display:none}::highlight(mosaic-spelling)',1)
s=s.replace('.desktopNav{grid-column:1;grid-row:2;min-width:0;overflow:auto;', '.desktopNav{display:block;grid-column:1;grid-row:2;min-width:0;overflow-y:auto;overflow-x:hidden;',1)
s=s.replace('.desktopNavName{font-size:14px;font-weight:680;white-space:nowrap;', '.desktopNavName{display:block;font-size:14px;font-weight:680;white-space:nowrap;',1)
s=s.replace('.desktopNavMeta{font-size:11px;color:#85858f;margin-top:2px}', '.desktopNavMeta{display:block;font-size:11px;color:#85858f;margin-top:2px}',1)
s=s.replace("const count=navCount(type,item.id),unit=type==='notebook'?'section':type==='section'?'page':'',meta=type==='page'?'Page':`${count} ${unit}${count===1?'':'s'}`;return `<button", "const count=navCount(type,item.id),unit=type==='notebook'?'section':type==='section'?'page':'',meta=type==='page'?'':`${count} ${unit}${count===1?'':'s'}`;return `<button",1)
s=s.replace('<span class=\"desktopNavName\">${esc(item.title||\'Untitled\')}</span><span class=\"desktopNavMeta\">${esc(meta)}</span>', '<span class=\"desktopNavName\">${esc(item.title||\'Untitled\')}</span>${meta?`<span class=\"desktopNavMeta\">${esc(meta)}</span>`:\'\'}',1)
p.write_text(s)
(Path('/tmp/mosaic-src/mosaic-notes/index.html')).write_text(s)
