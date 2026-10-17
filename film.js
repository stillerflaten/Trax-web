/* Lanseringsvideoen i «Nytt i versjon 2.0», felles for alle språk.
   Uten skript vises videoen med vanlige kontroller. Med skript spiller den lydløst i loop mens den er synlig,
   og knappen slår på lyd (fra starten av filmen). Med «Reduser bevegelse» starter den ikke av seg selv. */
(function(){
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var filmer=document.querySelectorAll('.v2-film');
  for(var i=0;i<filmer.length;i++)(function(f){
    var v=f.querySelector('video'), b=f.querySelector('.v2-lyd'), startet=false;
    if(!v||!b)return;
    v.removeAttribute('controls');v.muted=true;b.hidden=false;
    function tekst(){b.lastChild.nodeValue=v.paused?b.dataset.spill:(v.muted?b.dataset.paa:b.dataset.av);b.classList.toggle('paa',!v.paused&&!v.muted)}
    function spill(){var p=v.play();if(p&&p.catch)p.catch(function(){})}
    b.addEventListener('click',function(){
      if(v.muted||v.paused){v.muted=false;v.currentTime=0;startet=true;spill()}else{v.muted=true}
      tekst();
    });
    v.addEventListener('play',tekst);v.addEventListener('pause',tekst);v.addEventListener('volumechange',tekst);
    if('IntersectionObserver' in window){
      new IntersectionObserver(function(en){
        if(en[0].isIntersecting){if(!still||startet)spill()}else v.pause();
      },{threshold:.25}).observe(v);
    }else if(!still){spill()}
    tekst();
  })(filmer[i]);
})();
