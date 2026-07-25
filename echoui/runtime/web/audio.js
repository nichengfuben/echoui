(function(){
var bgm=null,vol=1.0,spd=1.0;
function playSrc(src,loop,v){
  if(!src)return;
  if(src.indexOf("__note:")===0){
    var p=src.split(":");var f=+p[1],b=+(p[2]||1);
    try{var ctx=new (window.AudioContext||window.webkitAudioContext)();
      var o=ctx.createOscillator();var g=ctx.createGain();
      o.frequency.value=f;g.gain.value=(v||vol)*0.2;
      o.connect(g);g.connect(ctx.destination);o.start();
      o.stop(ctx.currentTime+b*0.5);}catch(e){}
    return;
  }
  var a=new Audio(src);a.volume=v!=null?v:vol;a.playbackRate=spd;
  if(loop)a.loop=true;
  a.play().catch(function(){});
  return a;
}
window.__echoui=window.__echoui||{};
window.__echoui.audio={
  play:function(src,opts){opts=opts||{};return playSrc(src,!!opts.loop,opts.volume);},
  bgm:function(src){if(bgm){try{bgm.pause();}catch(e){}}bgm=playSrc(src,true);},
  stopBgm:function(){if(bgm){try{bgm.pause();bgm=null;}catch(e){}}},
  setVolume:function(pct){vol=Math.max(0,Math.min(1,pct/100));if(bgm)bgm.volume=vol;},
  setSpeed:function(pct){spd=Math.max(0.25,Math.min(4,pct/100));if(bgm)bgm.playbackRate=spd;},
  speak:function(text,lang){try{var u=new SpeechSynthesisUtterance(text);if(lang)u.lang=lang;speechSynthesis.speak(u);}catch(e){}}
};
})();
