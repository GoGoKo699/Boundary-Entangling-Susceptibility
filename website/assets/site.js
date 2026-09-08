/* Reader controls only. Scientific content and math require no JavaScript. */
'use strict';
(function(){
  document.documentElement.classList.add('js');
  const root=document.body.dataset.root || '';
  const theme=document.getElementById('theme');
  const menu=document.getElementById('menu');
  function setTheme(dark){
    document.documentElement.dataset.theme=dark?'dark':'light';
    theme.textContent=dark?'Light':'Dark';
    theme.setAttribute('aria-label',dark?'Switch to light reading theme':'Switch to dark reading theme');
  }
  let saved=null;
  try{saved=localStorage.getItem('bes-theme');}catch(e){/* Storage is optional, including local-file browsing. */}
  setTheme(saved==='dark');
  theme.addEventListener('click',function(){
    const dark=document.documentElement.dataset.theme!=='dark';setTheme(dark);
    try{localStorage.setItem('bes-theme',dark?'dark':'light');}catch(e){}
  });
  menu.addEventListener('click',function(){
    const nav=document.getElementById('side-navigation');const open=nav.classList.toggle('open');
    menu.setAttribute('aria-expanded',String(open));
  });
  const input=document.getElementById('search');
  const results=document.getElementById('search-results');
  const status=document.getElementById('search-status');
  document.getElementById('search-form').addEventListener('submit',e=>e.preventDefault());
  input.addEventListener('input',function(){
    results.replaceChildren();status.textContent='';
    const query=input.value.trim().toLocaleLowerCase();
    if(query.length<2)return;
    const words=query.split(/\s+/).filter(Boolean);
    const hits=(window.BES_SEARCH||[]).map(item=>{
      const title=item.title.toLocaleLowerCase(),text=item.text.toLocaleLowerCase();
      if(!words.every(w=>text.includes(w)||title.includes(w)))return null;
      const score=words.reduce((s,w)=>s+(title.includes(w)?10:0),0)+(item.section==='Source files'?-5:0);
      return {item,score};
    }).filter(Boolean).sort((a,b)=>b.score-a.score).slice(0,8);
    status.textContent=hits.length?`${hits.length} matching pages`:'No matching pages. Try a shorter term.';
    hits.forEach(({item})=>{
      const a=document.createElement('a');a.href=root+item.url;a.textContent=item.title;
      const small=document.createElement('small');small.textContent=item.section;a.appendChild(small);results.appendChild(a);
    });
  });
})();
