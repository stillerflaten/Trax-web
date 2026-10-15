/* Bevegelse på forsiden, felles for index.html, sv/index.html og en/index.html.
   1) Delene i hver seksjon glir rolig inn når de kommer til syne (toppen gjøres med CSS ved lasting).
   2) Telefonen i toppen synker litt når du scroller.
   3) Sporlinja fortsetter fra toppen og nedover siden mens du scroller. Hver seksjon er en gjenstand
      som får en grønn hake når sporet når den, og siste gjenstand er App Store-knappen nederst.
      På brede skjermer går linja i margen til høyre; på smalere skjermer vises bare gjenstandene
      som prikker foran overskriftene.
   Med «Reduser bevegelse» står alt stille: linja er tegnet ferdig og alle gjenstandene er funnet. */
(function(){
  var root=document.documentElement;
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS='http://www.w3.org/2000/svg';
  function el(n,a){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);return e}

  // ---------- 1) Innglidning per seksjon ----------
  // Skjermbildegalleriet er bevisst ikke med: bevegelse inni den vannrette rullelista ga hakking når man scrollet nedover på iPhone.
  var GRUPPER=['.funk h2,.funk .sub,.fg li','.del-g > div,.del img','.om-g blockquote,.om-g > div','#support h2,.sup-intro,.post,.faq > div,.pv','footer .stort,footer .rad'];
  if(!still&&'IntersectionObserver' in window){
    var vh=window.innerHeight, io=new IntersectionObserver(function(en){
      en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}});
    },{rootMargin:'0px 0px -8% 0px'});
    GRUPPER.forEach(function(sel){
      var els=document.querySelectorAll(sel), n=0;
      for(var i=0;i<els.length;i++){
        if(els[i].getBoundingClientRect().top<vh)continue; // allerede synlig ved lasting: la stå
        els[i].classList.add('inn');els[i].style.transitionDelay=(Math.min(n++,5)*80)+'ms';io.observe(els[i]);
      }
    });
  }

  // ---------- 2) Telefonen i toppen ----------
  var tlf=document.querySelector('.flate img'), py=-1;

  // ---------- 3) Sporlinja ----------
  var MAAL=['.funk h2','.del h2','.om-g blockquote','#support h2','footer .kjop'];
  var maal=[];MAAL.forEach(function(s){var e=document.querySelector(s);if(e)maal.push(e)});
  var start=document.querySelector('.trackline > circle:last-of-type');
  var svg=el('svg',{'class':'sporlinje','aria-hidden':'true'}), path=el('path',{'class':'spor'});
  var mask=el('mask',{id:'spor-vei',maskUnits:'userSpaceOnUse'}), mrect=el('rect',{x:0,y:0,fill:'black'});
  var mpath=el('path',{style:'fill:none;stroke:#fff;stroke-width:12px;stroke-linecap:round'});
  mask.appendChild(mrect);mask.appendChild(mpath);
  var defs=el('defs');defs.appendChild(mask);svg.appendChild(defs);
  path.setAttribute('mask','url(#spor-vei)');svg.appendChild(path);
  var merker=[], prikker=[], L=0, prover=[], bred=false, tegnet=0, funnet=[];
  for(var i=0;i<maal.length;i++){
    var g=el('g',{'class':'gj'});
    g.appendChild(el('circle',{'class':'m',r:15}));
    var t=el('text',{'text-anchor':'middle',dy:'.35em'});t.textContent=String(i+1);g.appendChild(t);
    var h=el('g',{'class':'hake'});h.appendChild(el('circle',{r:8.5,cx:11,cy:-11}));h.appendChild(el('path',{d:'M7.2 -11 l2.6 2.6 l5 -5.2'}));g.appendChild(h);
    svg.appendChild(g);merker.push(g);
    var d=document.createElement('span');d.className='gj-prikk';d.setAttribute('aria-hidden','true');
    var mor=maal[i].closest('.rad')||maal[i];mor.insertBefore(d,mor.firstChild);prikker.push(d);funnet.push(false);
  }
  document.body.appendChild(svg);

  function finn(i){
    if(funnet[i])return;funnet[i]=true;
    merker[i].classList.add('funnet');prikker[i].classList.add('funnet');
  }

  function layout(){
    var w=root.clientWidth;
    bred=w>=1240&&!!start;
    root.classList.toggle('spor-bred',bred);
    svg.style.height='0px';
    if(!bred)return;
    var hoyde=root.scrollHeight, sy=window.scrollY||window.pageYOffset;
    svg.style.height=hoyde+'px';svg.setAttribute('viewBox','0 0 '+w+' '+hoyde);
    mrect.setAttribute('width',w);mrect.setAttribute('height',hoyde);
    var venstre=maal[0].getBoundingClientRect().left, gx=w-venstre/2, sving=Math.min(venstre*.3,46);
    var s=start.getBoundingClientRect(), p={x:s.left+s.width/2,y:s.top+s.height/2+sy}, d='M'+p.x.toFixed(1)+' '+p.y.toFixed(1);
    var punkter=[];
    for(var i=0;i<maal.length;i++){
      var r=maal[i].getBoundingClientRect(), q={x:gx,y:r.top+Math.min(r.height,60)/2+sy}, dy=q.y-p.y, k=(i%2?1:-1)*sving;
      d+=' C'+(p.x+k).toFixed(1)+' '+(p.y+dy*.35).toFixed(1)+' '+(q.x-k).toFixed(1)+' '+(q.y-dy*.35).toFixed(1)+' '+q.x.toFixed(1)+' '+q.y.toFixed(1);
      merker[i].setAttribute('transform','translate('+q.x.toFixed(1)+' '+q.y.toFixed(1)+')');
      punkter.push(q);p=q;
    }
    path.setAttribute('d',d);mpath.setAttribute('d',d);
    L=path.getTotalLength();prover=[];
    for(var l=0;l<=L;l+=6)prover.push([l,path.getPointAtLength(l).y]);
    prover.push([L,path.getPointAtLength(L).y]);
    // lengden fram til hver gjenstand
    for(var j=0,m=0;j<punkter.length;j++){while(m<prover.length-1&&prover[m][1]<punkter[j].y-1)m++;punkter[j].l=prover[m][0]}
    merker.forEach(function(g,i){g.dataset.l=punkter[i].l});
    mpath.style.strokeDasharray=L+' '+(L+20);
    oppdater(true);
  }

  function oppdater(tving){
    var sy=window.scrollY||window.pageYOffset, vh=window.innerHeight;
    if(tlf&&!still){var ny=Math.min(sy*.12,90);if(ny!==py&&sy<vh*1.5){py=ny;tlf.style.setProperty('--py',ny.toFixed(1)+'px')}}
    if(!bred){
      // smal skjerm: gjenstanden er funnet når overskriften er godt inne på skjermen
      for(var i=0;i<maal.length;i++)if(!funnet[i]&&maal[i].getBoundingClientRect().top<vh*.75)finn(i);
      return;
    }
    var y=sy+vh*.62, l=L;
    if(!still){for(var k=0;k<prover.length;k++)if(prover[k][1]>=y){l=prover[k][0];break}}
    if(sy+vh>=root.scrollHeight-4)l=L; // helt nederst: sporet er gått ferdig
    if(l>tegnet||tving){tegnet=Math.max(tegnet,l);mpath.style.strokeDashoffset=(L-tegnet).toFixed(1)}
    for(var j=0;j<merker.length;j++)if(+merker[j].dataset.l<=tegnet+1)finn(j);
  }

  if(still){root.classList.add('spor-still');maal.forEach(function(e,i){finn(i)})}
  var ventende=0;
  window.addEventListener('scroll',function(){if(!ventende)ventende=requestAnimationFrame(function(){ventende=0;oppdater()})},{passive:true});
  var rt;function relayout(){clearTimeout(rt);rt=setTimeout(layout,120)}
  window.addEventListener('resize',relayout);
  window.addEventListener('load',layout);
  if('ResizeObserver' in window)new ResizeObserver(relayout).observe(document.body);
  layout();
})();
