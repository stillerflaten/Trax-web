/* Skjermbildegalleri på forsiden: piler og prikker over en vannrett liste med scroll-snap.
   Sveip og rulling gjøres av nettleseren selv; skriptet legger bare til knappene og holder prikkene oppdatert.
   Tekstene til knappene står i data-attributter på .galleri, så skriptet er felles for index.html, sv/index.html og en/index.html. */
(function(){
  var g=document.querySelector('.galleri');
  if(!g)return;
  var liste=g.querySelector('.g-liste'), ktrl=g.querySelector('.g-ktrl'), prikker=g.querySelector('.g-prikker');
  var bilder=[].slice.call(liste.children), piler=g.querySelectorAll('.g-pil'), knapper=[], aktiv=-1, maal=-1, stopp=0;
  var rolig=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

  function gaTil(i){
    i=Math.max(0,Math.min(bilder.length-1,i));
    maal=i; marker(i); // huskes til rullingen stopper, så to raske trykk på pila går to bilder fram
    clearTimeout(stopp);stopp=setTimeout(function(){maal=-1},800);
    liste.scrollTo({left:bilder[i].offsetLeft-bilder[0].offsetLeft,behavior:rolig?'auto':'smooth'});
  }

  // Det bildet som står nærmest venstre kant er det aktive; helt til høyre er det siste aktivt
  function oppdater(){
    var x=liste.scrollLeft, i=0, best=1e9;
    if(x+liste.clientWidth>=liste.scrollWidth-2)i=bilder.length-1;
    else bilder.forEach(function(b,n){var d=Math.abs(b.offsetLeft-bilder[0].offsetLeft-x);if(d<best){best=d;i=n}});
    if(maal<0&&i!==aktiv)marker(i);
  }

  function marker(i){
    aktiv=i;
    knapper.forEach(function(k,n){if(n===i)k.setAttribute('aria-current','true');else k.removeAttribute('aria-current')});
    piler[0].disabled=i===0;
    piler[1].disabled=i===bilder.length-1;
  }

  bilder.forEach(function(b,n){
    var k=document.createElement('button');
    k.type='button';
    k.setAttribute('aria-label',(g.dataset.prikk||'{n} / {t}').replace('{n}',n+1).replace('{t}',bilder.length));
    k.addEventListener('click',function(){gaTil(n)});
    prikker.appendChild(k);knapper.push(k);
  });
  [].forEach.call(piler,function(p){p.addEventListener('click',function(){gaTil((maal<0?aktiv:maal)+(+p.dataset.steg))})});

  var ventende=0;
  liste.addEventListener('scroll',function(){if(!ventende)ventende=requestAnimationFrame(function(){ventende=0;oppdater()});
    clearTimeout(stopp);stopp=setTimeout(function(){maal=-1;oppdater()},150)},{passive:true});
  window.addEventListener('resize',oppdater);
  ktrl.hidden=false;
  oppdater();
})();
