/* Sporlinja øverst: fire poter går over skjermen og etterlater det stiplede sporet.
   Spilles én gang per besøk (sessionStorage), og først når linja er synlig på skjermen.
   Med «reduser bevegelse» eller uten JS vises sporet statisk. Felles for index.html, sv/index.html og en/index.html. */
(function(){
  var svg=document.querySelector('.trackline');
  if(!svg)return;
  var NS='http://www.w3.org/2000/svg', H=60, PAD=16, STEP=21, SIDE=7;
  var root=document.documentElement;
  // Originalkurven i et 700 × 60-rom; skaleres til faktisk bredde så poter og prikker ikke strekkes
  var BASE=[['M',10,40],['C',90,10,150,55,240,30],['S',380,8,460,38],['S',600,50,690,18]];
  var path=svg.querySelector('path'), dots=svg.querySelectorAll('circle');
  var mask, maskPath, paws, raf=0, W=0, L=0;

  function el(n,a){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);return e}

  function layout(){
    W=Math.max(320,Math.round(svg.getBoundingClientRect().width));
    var sx=function(x){return PAD+(x-10)*(W-2*PAD)/680};
    var d=BASE.map(function(s){var o=s[0];for(var i=1;i<s.length;i+=2)o+=' '+sx(s[i]).toFixed(1)+' '+s[i+1];return o}).join(' ');
    svg.setAttribute('viewBox','0 0 '+W+' '+H);
    svg.removeAttribute('preserveAspectRatio');
    path.setAttribute('d',d);
    dots[0].setAttribute('cx',sx(10));dots[1].setAttribute('cx',sx(690));
    if(maskPath){maskPath.setAttribute('d',d);mask.firstChild.setAttribute('width',W)}
    L=path.getTotalLength();
  }

  function played(){try{return sessionStorage.getItem('trax-spor')==='1'}catch(e){return false}}
  function markPlayed(){try{sessionStorage.setItem('trax-spor','1')}catch(e){}}
  function done(){root.classList.remove('spor-klar')}

  layout();
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(still||played()||!('IntersectionObserver' in window)||!path.getPointAtLength){done();return}
  window.traxSpor=true;

  // Maske som avdekker den stiplede linja bak potene
  var defs=el('defs');
  mask=el('mask',{id:'spor-maske',maskUnits:'userSpaceOnUse',x:0,y:-20,height:H+40});
  mask.appendChild(el('rect',{x:0,y:-20,width:W,height:H+40,fill:'black'}));
  // Stilen settes inline så den ikke arver stiplingen fra .trackline path i CSS-en
  maskPath=el('path',{d:path.getAttribute('d'),style:'fill:none;stroke:#fff;stroke-width:10px;stroke-linecap:round'});
  mask.appendChild(maskPath);
  // Én pote, med tærne pekende i gåretningen (oppover før rotasjon)
  var paw=el('g',{id:'spor-pote'});
  paw.appendChild(el('ellipse',{cx:0,cy:2.6,rx:4.3,ry:3.7}));
  [[-4.7,-2.6,1.7],[-1.7,-5.4,1.85],[1.7,-5.4,1.85],[4.7,-2.6,1.7]].forEach(function(t){paw.appendChild(el('circle',{cx:t[0],cy:t[1],r:t[2]}))});
  defs.appendChild(mask);defs.appendChild(paw);
  svg.insertBefore(defs,svg.firstChild);
  path.setAttribute('mask','url(#spor-maske)');
  paws=el('g',{'class':'paws'});
  svg.appendChild(paws);

  function finish(){
    cancelAnimationFrame(raf);raf=0;
    path.removeAttribute('mask');
    while(paws.firstChild)paws.removeChild(paws.firstChild);
    svg.classList.add('ferdig');
  }

  function run(){
    markPlayed();
    layout();
    // Potene settes ned annenhver gang til venstre og høyre for linja
    var prints=[];
    for(var s=STEP*0.5;s<=L;s+=STEP){
      var a=path.getPointAtLength(Math.max(0,s-1)),b=path.getPointAtLength(Math.min(L,s+1)),p=path.getPointAtLength(s);
      var ang=Math.atan2(b.y-a.y,b.x-a.x),side=prints.length%2?1:-1;
      var x=p.x-Math.sin(ang)*SIDE*side,y=p.y+Math.cos(ang)*SIDE*side;
      var u=el('use',{href:'#spor-pote',transform:'translate('+x.toFixed(1)+' '+y.toFixed(1)+') rotate('+(ang*180/Math.PI+90).toFixed(1)+') scale(1.25)',opacity:0});
      paws.appendChild(u);prints.push({s:s,u:u});
    }
    var TAIL=STEP*4.5, speed=Math.min(520,Math.max(230,L/2.6)), t0=0;
    maskPath.style.strokeDasharray=L+' '+(L+10);
    function frame(now){
      if(!t0)t0=now;
      var s=(now-t0)/1000*speed;
      maskPath.style.strokeDashoffset=L-Math.max(0,Math.min(L,s-STEP*0.6));
      for(var i=0;i<prints.length;i++){
        var age=(s-prints[i].s)/STEP, o=age<0?0:age<0.35?age/0.35:age<3?1:Math.max(0,1-(age-3)/1.4);
        prints[i].u.setAttribute('opacity',o.toFixed(2));
      }
      if(s>=L)svg.classList.add('ferdig');
      if(s<L+TAIL)raf=requestAnimationFrame(frame);else finish();
    }
    maskPath.style.strokeDashoffset=L;
    svg.classList.add('spiller');
    done();
    raf=requestAnimationFrame(frame);
  }

  var io=new IntersectionObserver(function(en){
    if(en[0].isIntersecting){io.disconnect();setTimeout(run,250)}
  },{threshold:0.6});
  io.observe(svg);

  var rt;
  window.addEventListener('resize',function(){
    clearTimeout(rt);
    rt=setTimeout(function(){if(Math.round(svg.getBoundingClientRect().width)!==W){if(raf)finish();layout()}},150);
  });
})();
