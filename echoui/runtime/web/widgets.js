(function(){
function loadScript(src){return new Promise(function(res,rej){var s=document.createElement("script");s.src=src;s.onload=res;s.onerror=rej;document.head.appendChild(s);});}
function initCharts(){
  if(typeof Chart==="undefined")return;
  document.querySelectorAll(".e-chartjs").forEach(function(el){
    if(el.dataset.eInit==="1")return;
    el.dataset.eInit="1";
    var values=[];try{values=JSON.parse(el.dataset.values||"[]");}catch(e){values=[];}
    var typ=el.dataset.chartType||"bar";
    new Chart(el,{type:typ,data:{labels:values.map(function(_,i){return String(i+1);}),datasets:[{data:values,backgroundColor:"#6200EE"}]},options:{responsive:false,animation:false,plugins:{legend:{display:false}}}});
  });
}
function initMaps(){
  if(typeof maplibregl==="undefined")return;
  document.querySelectorAll(".e-maplibre").forEach(function(el){
    if(el.dataset.eInit==="1")return;
    el.dataset.eInit="1";
    new maplibregl.Map({container:el.id,style:"https://demotiles.maplibre.org/style.json",center:[+el.dataset.lng||0,+el.dataset.lat||0],zoom:+el.dataset.zoom||2});
  });
}
function boot(){
  var needC=!!document.querySelector(".e-chartjs");
  var needM=!!document.querySelector(".e-maplibre");
  var chain=Promise.resolve();
  if(needC)chain=chain.then(function(){return loadScript("https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js");});
  if(needM){
    chain=chain.then(function(){
      var l=document.createElement("link");l.rel="stylesheet";l.href="https://cdn.jsdelivr.net/npm/maplibre-gl@4.1.2/dist/maplibre-gl.css";document.head.appendChild(l);
      return loadScript("https://cdn.jsdelivr.net/npm/maplibre-gl@4.1.2/dist/maplibre-gl.js");
    });
  }
  chain.then(function(){initCharts();initMaps();}).catch(function(){});
}
window.__echoui=window.__echoui||{};
window.__echoui.widgets={boot:boot};
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",boot);else boot();
})();
