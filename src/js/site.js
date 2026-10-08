(function(){
  var root=document.documentElement;
  // theme toggle
  var tb=document.getElementById('theme');
  function dark(){var t=root.getAttribute('data-theme');return t?t==='dark':matchMedia('(prefers-color-scheme:dark)').matches}
  function sync(){if(tb)tb.setAttribute('aria-pressed',dark()?'true':'false')}
  sync();
  if(tb)tb.addEventListener('click',function(){var n=dark()?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}sync()});

  // article: collapse TOC on small screens, reading progress, active TOC item
  var toc=document.querySelector('.tocbox');
  if(toc&&matchMedia('(max-width:63.99rem)').matches)toc.removeAttribute('open');
  var bar=document.querySelector('.progress i'),prose=document.querySelector('.prose');
  if(bar&&prose){var tick=false;addEventListener('scroll',function(){if(tick)return;tick=true;requestAnimationFrame(function(){
    var r=prose.getBoundingClientRect(),h=r.height-innerHeight;bar.style.transform='scaleX('+Math.max(0,Math.min(1,h>0?-r.top/h:0))+')';tick=false})},{passive:true})}
  if(toc&&'IntersectionObserver' in window){
    var links={};toc.querySelectorAll('a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){Object.keys(links).forEach(function(k){links[k].removeAttribute('aria-current')});var l=links[e.target.id];if(l)l.setAttribute('aria-current','true')}})},{rootMargin:'0px 0px -70% 0px'});
    document.querySelectorAll('.prose h2[id]').forEach(function(h){io.observe(h)});
  }

  // callouts: a blockquote that starts with Note, Warning, Tip or Important gets a style
  document.querySelectorAll('.prose blockquote').forEach(function(b){var s=b.querySelector('strong');if(!s)return;var k=s.textContent.toLowerCase().replace(/[^a-z]/g,'');
    if(['note','tip','warning','important','caution'].indexOf(k)>-1)b.classList.add('callout','c-'+k)});

  // diagram zoom
  var imgs=document.querySelectorAll('.prose img');
  if(imgs.length&&typeof HTMLDialogElement==='function'){
    var d=document.createElement('dialog');d.className='zoom';d.setAttribute('aria-label','Enlarged diagram');
    d.innerHTML='<button type="button">Close</button><img alt="">';document.body.appendChild(d);
    var big=d.querySelector('img');
    d.querySelector('button').addEventListener('click',function(){d.close()});
    d.addEventListener('click',function(e){if(e.target===d)d.close()});
    imgs.forEach(function(i){i.tabIndex=0;i.setAttribute('role','button');i.title='Click to enlarge';
      function open(){big.src=i.currentSrc||i.src;big.alt=i.alt;d.showModal()}
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
})();
