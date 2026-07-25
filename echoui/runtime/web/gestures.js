(function(){
function q(i){return document.getElementById(i);}
function wireGestures(list,S,s,sub){
  (list||[]).forEach(function(g){
    var e=q(g.node);if(!e)return;
    var sx=0,sy=0,active=false;
    e.addEventListener("pointerdown",function(ev){active=true;sx=ev.clientX;sy=ev.clientY;e.setPointerCapture(ev.pointerId);});
    e.addEventListener("pointermove",function(ev){
      if(!active)return;
      var dx=ev.clientX-sx,dy=ev.clientY-sy;sx=ev.clientX;sy=ev.clientY;
      if(g.signalX)s(g.signalX,(S[g.signalX]||0)+dx);
      if(g.signalY)s(g.signalY,(S[g.signalY]||0)+dy);
    });
    e.addEventListener("pointerup",function(){active=false;});
    e.addEventListener("pointercancel",function(){active=false;});
  });
}
function wireVirtualLists(){
  document.querySelectorAll(".e-virtual-list").forEach(function(el){
    var ih=+(el.dataset.itemHeight||40),total=+(el.dataset.total||0);
    var vp=el.querySelector(".e-virtual-viewport");
    if(!vp)return;
    el.addEventListener("scroll",function(){
      var start=Math.floor(el.scrollTop/ih);
      vp.style.transform="translateY("+(start*ih)+"px)";
      vp.dataset.start=String(start);
    });
  });
}
window.__echoui=window.__echoui||{};
window.__echoui.gestures={wireGestures:wireGestures,wireVirtualLists:wireVirtualLists};
})();
