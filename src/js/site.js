(function(){
  var root=document.documentElement;
  // narrow screens: keep the current section visible in the scrolling nav
  var cur=document.querySelector('.nav [aria-current]');
  if(cur){var nv=cur.parentNode;nv.scrollLeft=Math.max(0,cur.offsetLeft-nv.offsetLeft-16)}

  // article: collapse TOC on small screens, highlight the current section
  var toc=document.querySelector('.tocbox');
  if(toc&&matchMedia('(max-width:63.99rem)').matches)toc.removeAttribute('open');
  if(toc&&'IntersectionObserver' in window){
    var links={};toc.querySelectorAll('a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){Object.keys(links).forEach(function(k){links[k].removeAttribute('aria-current')});var l=links[e.target.id];if(l)l.setAttribute('aria-current','true')}})},{rootMargin:'0px 0px -70% 0px'});
    document.querySelectorAll('.prose h2[id]').forEach(function(h){io.observe(h)});
  }

  // diagram zoom: opens at natural size, scrolls and pinch-zooms natively; Escape or Close to leave, focus stays inside
  var imgs=document.querySelectorAll('.prose img');
  if(imgs.length&&typeof HTMLDialogElement==='function'){
    var d=document.createElement('dialog');d.className='zoom';d.setAttribute('aria-label','Enlarged diagram');
    d.innerHTML='<div class="zoom-tools"><button type="button" class="zoom-toggle" aria-pressed="false">Fit to screen</button><button type="button" class="zoom-close">Close</button></div><div class="zoom-image" tabindex="0" role="group"><img alt=""></div>'; document.body.appendChild(d);
    var big=d.querySelector('img'),box=d.querySelector('.zoom-image'),z=d.querySelector('.zoom-toggle'),cl=d.querySelector('.zoom-close'),opener=null;
    function setFit(f){d.classList.toggle('fit',f);z.textContent=f?'Actual size':'Fit to screen';z.setAttribute('aria-pressed',f?'true':'false')}
    cl.addEventListener('click',function(){d.close()});
    z.addEventListener('click',function(){setFit(!d.classList.contains('fit'))});
    d.addEventListener('click',function(e){if(e.target===d)d.close()});
    d.addEventListener('close',function(){document.documentElement.style.overflow='';if(opener&&opener.focus)opener.focus()});
    d.addEventListener('keydown',function(e){if(e.key!=='Tab')return;var f=[z,cl,box],i=f.indexOf(document.activeElement);
      if(e.shiftKey&&i<=0){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&(i===f.length-1||i<0)){e.preventDefault();f[0].focus()}});
    imgs.forEach(function(i){i.tabIndex=0;i.setAttribute('role','button');i.title='Click to enlarge';
      function open(){opener=i;setFit(false);var w=Math.min(i.naturalWidth||1200,1600);d.style.setProperty('--zoom-width',Math.max(w,1200)+'px');big.src=i.currentSrc||i.src;big.alt=i.alt;box.setAttribute('aria-label',i.alt||'Enlarged diagram');box.scrollTop=0;box.scrollLeft=0;document.documentElement.style.overflow='hidden';d.showModal();cl.focus()}
      i.addEventListener('click',open);i.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}})});
  }

  // search page
  var form=document.querySelector('.sform');
  if(form){
    var q=document.getElementById('q'),res=document.getElementById('sresults'),st=document.getElementById('sstatus'),idx=null,total=0;
    var esc=function(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
    function load(){return idx?Promise.resolve(idx):fetch('/search.json').then(function(r){return r.json()}).then(function(j){idx=j;total=j.length;return j})}
    function run(){
      var v=q.value.trim().toLowerCase();
      var u=new URL(location.href);if(v)u.searchParams.set('q',q.value.trim());else u.searchParams.delete('q');history.replaceState(null,'',u);
      if(!v){res.innerHTML='';st.textContent='Type to search '+(total||'')+' articles.';return}
      load().then(function(data){
        var words=v.split(/\s+/);
        var hits=data.map(function(a){var score=0,t=a.t.toLowerCase(),d=a.d.toLowerCase(),g=a.g.join(' ').toLowerCase(),x=a.x.toLowerCase(),c=(a.c+' '+a.s).toLowerCase();
          for(var i=0;i<words.length;i++){var w=words[i],m=0;
            if(t.indexOf(w)>-1)m+=10;if(g.indexOf(w)>-1)m+=6;if(c.indexOf(w)>-1)m+=4;if(d.indexOf(w)>-1)m+=3;if(x.indexOf(w)>-1)m+=1;
            if(!m)return null;score+=m}
          return{a:a,s:score,x:x,w:words[0]}}).filter(Boolean).sort(function(a,b){return b.s-a.s});
        st.textContent=hits.length?hits.length+' result'+(hits.length>1?'s':'')+' for “'+q.value.trim()+'”':'No articles match “'+q.value.trim()+'”. Try a shorter word, or browse all articles.';
        res.innerHTML=hits.map(function(h){var a=h.a,i=h.x.indexOf(h.w),snip='';
          if(i>-1&&a.t.toLowerCase().indexOf(h.w)<0&&a.d.toLowerCase().indexOf(h.w)<0){var s=Math.max(0,i-60);snip='…'+esc(a.x.slice(s,i+110).trim())+'…'}
          return '<li><a href="'+a.u+'"><span class="k">'+esc(a.c)+' / '+esc(a.s)+'</span><strong>'+esc(a.t)+'</strong><span class="d">'+esc(a.d.length>180?a.d.slice(0,180)+'…':a.d)+'</span>'+(snip?'<span class="sn">'+snip+'</span>':'')+'</a></li>'}).join('');
      });
    }
    form.addEventListener('submit',function(e){e.preventDefault();run()});
    q.addEventListener('input',run);
    var init=new URL(location.href).searchParams.get('q');if(init){q.value=init;run()}else load();
  }
  // "/" opens search
  addEventListener('keydown',function(e){if(e.key==='/'&&!/input|textarea|select/i.test((document.activeElement||{}).tagName||'')&&!document.querySelector('.sform')){e.preventDefault();location.href='/search/'}});

  // Keyboard access: a table that scrolls sideways on a narrow screen must be reachable with the keyboard
  function tableFocus(){
    document.querySelectorAll('.prose table').forEach(function(tb){
      if(tb.scrollWidth>tb.clientWidth+1)tb.setAttribute('tabindex','0');else tb.removeAttribute('tabindex');
    });
  }
  tableFocus();
  addEventListener('resize',tableFocus);
  // Articles page: topic chips + text filter (list is fully visible without JS)
  (function(){
    var box=document.querySelector('[data-afilter]'),ul=document.querySelector('[data-alist]');
    if(!box||!ul)return;
    var items=[].slice.call(ul.children),q=box.querySelector('input'),btns=[].slice.call(box.querySelectorAll('.fchips button')),
        cnt=box.querySelector('.fcount'),empty=document.querySelector('.fempty'),topic='';
    box.hidden=false;
    function apply(){
      var v=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean),n=0;
      items.forEach(function(li){
        var ok=(!topic||li.getAttribute('data-topic')===topic)&&v.every(function(w){return li.getAttribute('data-text').indexOf(w)>-1});
        li.hidden=!ok;if(ok)n++;
      });
      cnt.textContent='Showing '+n+' of '+items.length+' articles';
      if(empty)empty.hidden=n>0;
    }
    btns.forEach(function(b){b.addEventListener('click',function(){
      topic=b.getAttribute('data-topic');
      btns.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
      apply();
    })});
    q.addEventListener('input',apply);
    apply();
  })();
})();
