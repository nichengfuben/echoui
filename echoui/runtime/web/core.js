(function(){
var S={},subs={},keys={},last=0,frameFn=null;
function loadFrameScript(src){
  var pre="function __echoui_frame(dt,S,s){";
  if(!src||src.indexOf(pre)!==0)return null;
  var body=src.slice(pre.length);
  if(!body||body.charAt(body.length-1)!=="}")return null;
  try{return new Function("dt","S","s",body.slice(0,-1));}catch(e){return null;}
}
var DOMT={hover_enter:"mouseenter",hover_leave:"mouseleave",drag:"mousedown"};
function q(i){return document.getElementById(i);}
function g(k){return S[k];}
function s(k,v){if(S[k]===v)return;S[k]=v;(subs[k]||[]).forEach(function(f){f(v);});gpu();}
function sub(k,f){subs[k]=subs[k]||[];subs[k].push(f);f(S[k]);}
function tpl(t,d){var o=t;d.forEach(function(k,i){o=o.split("{"+i+"}").join(S[k]);});return o;}
function bindT(n,t,d){function u(){var e=q(n);if(e)e.textContent=tpl(t,d);}d.forEach(function(k){sub(k,u);});u();}
function bindS(n,p,v,d){function u(){var e=q(n);if(!e)return;var x=v;if(typeof v==="string"&&v[0]==="{")x=S[v.slice(1,-1)]+(p==="left"||p==="top"?"px":"");e.style[p]=x;}d.forEach(function(k){sub(k,u);});u();}
function run(a){if(!a)return;if(a.k==="nav"){if(a.href)location.href=a.href;return;}if(a.k==="audio"){var au=window.__echoui&&window.__echoui.audio;if(au&&a.op==="play")au.play(a.src,{loop:!!a.loop,volume:a.volume});return;}if(a.k==="inc")s(a.s,(g(a.s)|0)+a.by);else if(a.k==="dec")s(a.s,(g(a.s)|0)-a.by);else if(a.k==="set")s(a.s,a.v);}
function runA(a){if(!a)return;if(a.script){try{new Function("S","s",a.script)(S,s);}catch(e){}}else run(a);}
function applyP(p){(p||[]).forEach(function(x){var e=q(x.id);if(!e)return;if(x.text!==undefined)e.textContent=x.text;if(x.style)Object.keys(x.style).forEach(function(k){e.style[k]=x.style[k];});});}
function act(h){var a=(window.__ECHoui_CFG.actions||{})[h];if(a&&a.local)runA(a);}
function clk(n,a){var e=q(n);if(!e)return;e.addEventListener("click",function(){if(typeof a==="object"&&a&&a.local)runA(a);else act(a.h||a);});}
function wireD(list){(list||[]).forEach(function(ev){var e=q(ev.node);if(!e)return;var t=DOMT[ev.type]||ev.type;var o=t==="wheel"?{passive:false}:undefined;e.addEventListener(t,function(evt){if(t==="wheel")evt.preventDefault();act(ev.handler);},o);});}
function fitStage(){document.querySelectorAll(".e-stage.e-fill").forEach(function(st){var inner=st.querySelector(".e-stage-inner");if(!inner)return;var dw=+(inner.dataset.w||640),dh=+(inner.dataset.h||360);var sx=window.innerWidth/dw,sy=window.innerHeight/dh;inner.style.transform="scale("+sx+","+sy+")";});}
function gpu2d(G,c){var x=c.getContext("2d");x.clearRect(0,0,G.width,G.height);(G.nodes||[]).forEach(function(n){var lx=typeof n.x==="string"&&n.x.indexOf(".")>0?g(n.x):+n.x;var ly=typeof n.y==="string"&&n.y.indexOf(".")>0?g(n.y):+n.y;x.fillStyle=n.c||"#888";x.fillRect(lx,ly,n.w,n.h);});}
function gpu(){var G=window.__ECHoui_CFG.gpu;if(!G)return;var c=q(G.canvas);if(!c){document.querySelectorAll(".e-gpu-hide").forEach(function(e){e.style.visibility="visible";});return;}if(G.backend==="webgpu"&&window.__echoui&&window.__echoui.webgpu&&window.__echoui.webgpu.supports()){window.__echoui.webgpu.ensure(c).then(function(ok){if(ok&&window.__echoui.webgpu.draw(G,g))return;gpu2d(G,c);});return;}gpu2d(G,c);}
function localF(t){if(!frameFn)return;last=last||t;var dt=Math.min(0.05,(t-last)/1000||0.016);last=t;frameFn(dt,S,s);}
function loop(t){localF(t||performance.now());requestAnimationFrame(loop);}
document.addEventListener("keydown",function(e){keys[e.code]=1;var m=window.__ECHoui_CFG.keymap||{};if(m[e.code]){e.preventDefault();act(m[e.code]);}});
document.addEventListener("keyup",function(e){keys[e.code]=0;});
window.__echoui={g:g,s:s,sub:sub,apply:function(p){Object.keys(p).forEach(function(k){s(k,p[k]);});},key:function(c){return!!keys[c];},gpu:gpu,fitStage:fitStage,storage:function(){return window.__echoui.storage;}};
function resumeCfg(){var el=document.getElementById("__echoui_resume");if(!el)return null;try{return JSON.parse(el.textContent||"");}catch(e){return null;}}
document.addEventListener("DOMContentLoaded",function(){var c=window.__ECHoui_CFG||{};var r=resumeCfg();if(r&&r.signals)Object.keys(r.signals).forEach(function(k){c.signals=c.signals||{};if(c.signals[k]===undefined)c.signals[k]=r.signals[k];});Object.keys(c.signals||{}).forEach(function(k){S[k]=c.signals[k];});if(window.__echoui.storage&&window.__echoui.storage.opfsInit)window.__echoui.storage.opfsInit();var ui=window.__echoui&&window.__echoui.ui;(c.bindings||[]).forEach(function(b){if(b.t==="text")bindT(b.n,b.tpl,b.d);else if(b.t==="style")bindS(b.n,b.p,b.v,b.d);else if(b.t==="attr"&&ui)ui.bindAttr(b.n,b.a,b.v,b.d,S,sub);else if(b.t==="bg"&&ui)ui.bindBg(b.n,b.v,b.d,S,sub);});if(ui){ui.wireFiles(c.file_inputs,S,s,sub);ui.wireOverlays(c.overlays,S,sub);}if(window.__echoui.gestures){window.__echoui.gestures.wireGestures(c.gestures,S,s,sub);window.__echoui.gestures.wireVirtualLists();}(c.clicks||[]).forEach(function(x){clk(x.node,c.actions[x.action||x.handler]||x.handler);});wireD(c.dom);if(c.frame_script)frameFn=loadFrameScript(c.frame_script);gpu();fitStage();window.addEventListener("resize",fitStage);if(c.frames||c.frame_local)requestAnimationFrame(loop);});
})();
