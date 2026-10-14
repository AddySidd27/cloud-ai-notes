(function(){
  'use strict';
  var prose=document.querySelector('.prose');
  if(!prose)return;
  var uid=0;
  function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e}
  function store(){try{return window.localStorage}catch(e){return null}}
  function read(k){try{var s=store();return s?JSON.parse(s.getItem(k)):null}catch(e){return null}}
  function write(k,v){try{var s=store();if(s)s.setItem(k,JSON.stringify(v))}catch(e){}}

  /* 1. path picker */
  prose.querySelectorAll('[data-path-picker]').forEach(function(pp){
    var btns=[].slice.call(pp.querySelectorAll('[data-path]'));
    var panels=[].slice.call(pp.querySelectorAll('[data-path-panel]'));
    if(!btns.length||!panels.length)return;
    var hint=el('p','path-picker__hint','Choose a path above to see its steps.');
    hint.setAttribute('role','status');
    panels.forEach(function(p){
      var id='pp'+(++uid);p.id=p.id||id;p.hidden=true;p.setAttribute('role','region');p.tabIndex=-1;
    });
    function pick(b){
      var key=b.getAttribute('data-path');
      btns.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
      panels.forEach(function(p){p.hidden=p.getAttribute('data-path-panel')!==key});
      hint.hidden=true;
    }
    btns.forEach(function(b){
      b.setAttribute('aria-pressed','false');
      var p=panels.filter(function(x){return x.getAttribute('data-path-panel')===b.getAttribute('data-path')})[0];
      if(p){b.setAttribute('aria-controls',p.id);p.setAttribute('aria-label',b.textContent.trim())}
      b.addEventListener('click',function(){pick(b)});
    });
    var bar=pp.querySelector('.path-picker__buttons');
    bar.parentNode.insertBefore(hint,bar.nextSibling);
    pp.classList.add('is-enhanced');
  });

  /* 2. task-list checklists: "- [ ] text" arrives from Markdown as <li>[ ] text</li> */
  var pathKey=location.pathname;
  var lists=[];
  prose.querySelectorAll('ul').forEach(function(ul){
    var items=[].slice.call(ul.children).filter(function(li){return li.tagName==='LI'&&/^\s*\[( |x|X)\]\s/.test(li.textContent)});
    if(!items.length||items.length!==ul.children.length)return;
    lists.push({ul:ul,items:items});
  });
  lists.forEach(function(L,n){
    var key='ia-checklist:'+pathKey+':'+n;
    var saved=read(key)||[];
    var boxes=[];
    L.ul.classList.add('ia-checklist');
    L.items.forEach(function(li,i){
      // strip the "[ ] " marker from the first text node
      var w=document.createTreeWalker(li,NodeFilter.SHOW_TEXT),t=w.nextNode();
      var pre=t.nodeValue.replace(/^\s*\[( |x|X)\]\s/,'');
      var startsChecked=/^\s*\[[xX]\]/.test(t.nodeValue);
      t.nodeValue=pre;
      var id='ia-t'+(++uid);
      var cb=el('input');cb.type='checkbox';cb.id=id;
      var lab=el('label');lab.htmlFor=id;
      // move inline children (up to a nested list) into the label
      var kids=[].slice.call(li.childNodes);
      kids.forEach(function(k){
        if(k.nodeType===1&&(k.tagName==='UL'||k.tagName==='OL'))return;
        if(k.nodeType===1&&k.tagName==='P'){while(k.firstChild)lab.appendChild(k.firstChild);k.remove();return}
        lab.appendChild(k);
      });
      li.insertBefore(lab,li.firstChild);li.insertBefore(cb,lab);
      li.classList.add('ia-task');
      cb.checked=saved.length?!!saved[i]:startsChecked;
      boxes.push(cb);
    });
    var bar=el('div','ia-bar');
    var status=el('span','ia-status');status.setAttribute('role','status');
    var reset=el('button','ia-btn','Reset');reset.type='button';
    reset.setAttribute('aria-label','Reset this checklist');
    bar.appendChild(status);bar.appendChild(reset);
    L.ul.parentNode.insertBefore(bar,L.ul);
    function update(persist){
      var d=boxes.filter(function(b){return b.checked}).length;
      status.textContent=d+' of '+boxes.length+' done';
      if(persist)write(key,boxes.map(function(b){return b.checked}));
    }
    boxes.forEach(function(b){b.addEventListener('change',function(){update(true)})});
    reset.addEventListener('click',function(){boxes.forEach(function(b){b.checked=false});update(true)});
    update(false);
  });

  /* 3. copy buttons */
  function fallbackCopy(text){
    var ta=el('textarea');ta.value=text;ta.setAttribute('readonly','');
    ta.style.cssText='position:fixed;top:0;left:0;opacity:0';
    document.body.appendChild(ta);ta.select();
    var ok=false;try{ok=document.execCommand('copy')}catch(e){}
    ta.remove();return ok;
  }
  function copy(text){
    if(navigator.clipboard&&navigator.clipboard.writeText){
      return navigator.clipboard.writeText(text).then(function(){return true},function(){return fallbackCopy(text)});
    }
    return Promise.resolve(fallbackCopy(text));
  }
  prose.querySelectorAll('pre').forEach(function(pre){
    var code=pre.querySelector('code')||pre;
    var wrap=el('div','ia-code'),bar=el('div','ia-code__bar');
    var b=el('button','ia-btn','Copy');b.type='button';b.setAttribute('aria-label','Copy code to clipboard');
    var live=el('span','ia-sr');live.setAttribute('role','status');
    bar.appendChild(b);bar.appendChild(live);
    pre.parentNode.insertBefore(wrap,pre);wrap.appendChild(bar);wrap.appendChild(pre);
    var timer;
    b.addEventListener('click',function(){
      copy(code.textContent.replace(/\n$/,'')).then(function(ok){
        clearTimeout(timer);
        b.textContent=ok?'Copied':'Copy failed';b.classList.toggle('is-done',ok);
        b.setAttribute('aria-label',ok?'Code copied to clipboard':'Copy failed, select the code manually');
        live.textContent=ok?'Code copied':'Copy failed';
        timer=setTimeout(function(){b.textContent='Copy';b.classList.remove('is-done');b.setAttribute('aria-label','Copy code to clipboard');live.textContent=''},1500);
      });
    });
  });

  /* 4. expand all / collapse all */
  var dets=[].slice.call(prose.querySelectorAll('details'));
  if(dets.length){
    var tb=el('div','ia-expandbar');
    var tg=el('button','ia-btn');tg.type='button';
    tb.appendChild(tg);
    dets[0].parentNode.insertBefore(tb,dets[0]);
    var sync=function(){var all=dets.every(function(d){return d.open});tg.textContent=all?'Collapse all':'Expand all';
      tg.setAttribute('aria-label',(all?'Collapse':'Expand')+' all '+dets.length+' sections')};
    dets.forEach(function(d){d.addEventListener('toggle',sync)});
    tg.addEventListener('click',function(){var all=dets.every(function(d){return d.open});dets.forEach(function(d){d.open=!all});sync()});
    sync();
  }
  /* 5. the "On this page" rail with active-section highlight is already provided by site.js for every article. */
})();
