/* Trax – felles skript for alle sider. Siden virker uten det; skriptet legger bare til:
   1) Gamle adresser: lenker til /#support, /#personvern osv. (App Store bruker /#support) sendes til de nye sidene.
   2) «Last ned» i menyen går rett til App Store på iPhone og Google Play på Android.
   3) Faner i «Slik fungerer det» på store skjermer (på mobil står alle stegene under hverandre).
   4) Myk inngang for delene under skjermkanten. Med «Reduser bevegelse» står alt stille.
   5) Språkvelger og mobilmeny lukkes ved klikk utenfor eller Escape. */
(function(){
  var root=document.documentElement;
  root.classList.add('js');

  // 1) Gamle ankre på forsiden. data-gamle på <body> er en liste «anker=adresse» skilt med mellomrom.
  var gamle=document.body.getAttribute('data-gamle');
  if(gamle&&location.hash){
    var h=location.hash.slice(1);
    gamle.split(' ').forEach(function(p){var kv=p.split('=');if(kv[0]===h)location.replace(kv[1])});
  }

  // 2) Plattform for «Last ned»
  var ua=navigator.userAgent||'', ios=/iPhone|iPad|iPod/.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1), android=/Android/.test(ua);
  if(ios||android){
    var url=ios?'https://apps.apple.com/app/id6758005408':'https://play.google.com/store/apps/details?id=tillerflatendigital.trax.android';
    document.querySelectorAll('a[data-last-ned]').forEach(function(a){a.href=url});
  }

  // 3) Faner
  var faner=document.querySelectorAll('.faner [role=tab]'), paneler=document.querySelectorAll('.steg>li');
  function velg(i,fokus){
    faner.forEach(function(f,j){var p=j===i;f.setAttribute('aria-selected',p);f.tabIndex=p?0:-1;if(p&&fokus)f.focus()});
    paneler.forEach(function(p,j){p.hidden=j!==i});
  }
  if(faner.length===paneler.length&&faner.length){
    faner.forEach(function(f,i){
      f.addEventListener('click',function(){velg(i)});
      f.addEventListener('keydown',function(e){
        var n=faner.length,k=e.key;
        if(k==='ArrowRight'||k==='ArrowLeft'){e.preventDefault();velg((i+(k==='ArrowRight'?1:n-1))%n,true)}
      });
    });
    velg(+(document.querySelector('.faner').getAttribute('data-start')||0));
  }

  // 4) Myk inngang
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!still&&'IntersectionObserver' in window){
    var vh=window.innerHeight,io=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}});
    },{rootMargin:'0px 0px -6% 0px'});
    document.querySelectorAll('[data-inn]>*').forEach(function(el,i){
      if(el.getBoundingClientRect().top<vh)return;
      el.classList.add('inn');el.style.transitionDelay=(i%4*70)+'ms';io.observe(el);
    });
  }

  // 5) Lukk menyer
  var det=document.querySelectorAll('details.sprak,details.meny');
  document.addEventListener('click',function(e){det.forEach(function(d){if(d.open&&!d.contains(e.target))d.open=false})});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')det.forEach(function(d){if(d.open){d.open=false;d.querySelector('summary').focus()}})});
})();
