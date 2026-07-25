(function(){
function q(i){return document.getElementById(i);}
function bindAttr(n,a,tpl,d,S,sub){
  function u(){var e=q(n);if(!e)return;var v=tpl;if(typeof v==="string"&&v[0]==="{"&&v[v.length-1]==="}")v=S[v.slice(1,-1)]||"";e.setAttribute(a,v);if(a==="src"&&e.tagName==="IMG")e.style.display=v?"block":"none";}
  (d||[]).forEach(function(k){sub(k,u);});u();
}
function bindBg(n,tpl,d,S,sub){
  function u(){var e=q(n);if(!e)return;var v=tpl;if(typeof v==="string"&&v[0]==="{"&&v[v.length-1]==="}")v=S[v.slice(1,-1)]||"";if(v)e.style.backgroundImage=v?"url("+JSON.stringify(v)+")":"none";}
  (d||[]).forEach(function(k){sub(k,u);});u();
}
function wireFiles(list,S,s,sub){
  (list||[]).forEach(function(f){
    var e=q(f.node);if(!e)return;
    e.addEventListener("change",function(){
      var file=e.files&&e.files[0];if(!file||!f.signal)return;
      var r=new FileReader();
      r.onload=function(){s(f.signal,r.result);if(f.preview&&f.previewNode){var img=q(f.previewNode);if(img)img.src=r.result;}};
      r.readAsDataURL(file);
    });
  });
}
function wireOverlays(list,S,sub){
  (list||[]).forEach(function(o){
    function u(){var el=q(o.node);if(!el)return;var open=o.openSignal?!!S[o.openSignal]:!!o.open;
      el.classList.toggle("e-overlay-open",open);el.setAttribute("aria-hidden",open?"false":"true");}
    if(o.openSignal)sub(o.openSignal,u);u();
  });
}
window.__echoui=window.__echoui||{};
window.__echoui.ui={bindAttr:bindAttr,bindBg:bindBg,wireFiles:wireFiles,wireOverlays:wireOverlays};
})();
