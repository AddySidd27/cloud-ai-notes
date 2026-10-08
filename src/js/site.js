(function(){
  var root=document.documentElement;
  var btn=document.querySelector('.theme');
  function current(){var t=root.getAttribute('data-theme');if(t)return t;return matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}
  function label(){if(btn)btn.textContent=current()==='dark'?'Light theme':'Dark theme'}
  if(btn){label();btn.addEventListener('click',function(){var n=current()==='dark'?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}label()})}
  var imgs=document.querySelectorAll('.prose img');
  if(imgs.length&&typeof HTMLDialogElement==='function'){
    var d=document.createElement('dialog');d.className='zoom';d.setAttribute('aria-label','Enlarged diagram');
    d.innerHTML='<button type="button">Close</button><img alt="">';document.body.appendChild(d);
    var big=d.querySelector('img');
    d.querySelector('button').addEventListener('click',function(){d.close()});
    d.addEventListener('click',function(e){if(e.target===d)d.close()});
    imgs.forEach(function(i){i.tabIndex=0;i.setAttribute('role','button');
      function open(){big.src=i.currentSrc||i.src;big.alt=i.alt;d.showModal()}
      i.addEventListener('click',open);i.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}})});
  }
})();
