(function(){
window.__echoui=window.__echoui||{};
var plat={
  notify:function(title,body){
    if(!("Notification" in window))return;
    if(Notification.permission==="granted")new Notification(title,{body:body||""});
    else if(Notification.permission!=="denied")Notification.requestPermission().then(function(p){
      if(p==="granted")new Notification(title,{body:body||""});
    });
  },
  clipboardWrite:function(t){return navigator.clipboard&&navigator.clipboard.writeText(t);},
  clipboardRead:function(){return navigator.clipboard?navigator.clipboard.readText():Promise.resolve("");},
  share:function(d){return navigator.share?navigator.share(d):Promise.reject("no share");},
  vibrate:function(p){if(navigator.vibrate)navigator.vibrate(p);},
  battery:function(){return navigator.getBattery?navigator.getBattery():Promise.resolve({level:1,charging:true});},
  online:function(){return navigator.onLine;},
  geolocate:function(){return new Promise(function(res,rej){
    if(!navigator.geolocation)return rej("no geo");
    navigator.geolocation.getCurrentPosition(function(p){
      res({lat:p.coords.latitude,lng:p.coords.longitude,acc:p.coords.accuracy});
    },rej);
  });}
};
window.__echoui.platform=plat;
})();
