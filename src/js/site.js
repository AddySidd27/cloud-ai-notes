(function(){
  var tb=document.querySelector('.tocbox');
  if(tb&&matchMedia('(max-width:63.99rem)').matches)tb.removeAttribute('open');
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
