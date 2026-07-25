(function(){
var P="echoui:",mem={},rootHandle=null;
function lsGet(k){try{return localStorage.getItem(P+k);}catch(e){return mem[k]!=null?mem[k]:null;}}
function lsSet(k,v){try{localStorage.setItem(P+k,v);}catch(e){mem[k]=v;}}
function lsDel(k){try{localStorage.removeItem(P+k);}catch(e){delete mem[k];}}
function flush(){
  if(!rootHandle)return;
  rootHandle.getFileHandle("echoui-kv.json",{create:true}).then(function(fh){
    return fh.createWritable().then(function(w){
      w.write(JSON.stringify(mem));return w.close();
    });
  }).catch(function(){});
}
function opfsInit(){
  if(typeof navigator==="undefined"||!navigator.storage||!navigator.storage.getDirectory)return Promise.resolve(false);
  return navigator.storage.getDirectory().then(function(root){
    rootHandle=root;
    return root.getFileHandle("echoui-kv.json",{create:true}).then(function(fh){
      return fh.getFile().then(function(file){return file.text();});
    }).then(function(txt){
      if(txt){try{mem=JSON.parse(txt);}catch(e){mem={};}}
      Object.keys(mem).forEach(function(k){lsSet(k,mem[k]);});
      return true;
    });
  }).catch(function(){return false;});
}
var storage={
  get:function(k){return lsGet(k);},
  set:function(k,v){lsSet(k,String(v));mem[k]=String(v);flush();},
  delete:function(k){lsDel(k);delete mem[k];flush();},
  jsonGet:function(k){var r=storage.get(k);if(!r)return null;try{return JSON.parse(r);}catch(e){return null;}},
  jsonSet:function(k,o){storage.set(k,JSON.stringify(o));},
  opfsInit:opfsInit
};
window.__echoui=window.__echoui||{};
window.__echoui.storage=storage;
})();
