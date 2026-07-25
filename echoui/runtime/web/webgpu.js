(function(){
var W={ready:false,initing:null,device:null,ctx:null,format:null,pipeline:null,uniformBuf:null,bindGroup:null};
var WGSL="struct U{w:f32,h:f32,c:vec4f,x:f32,y:f32,sx:f32,sy:f32,p:vec2f;};@group(0)@binding(0)<uniform>U u;@vertex fn vs(@builtin(vertex_index)i:u32)->@builtin(position) vec4f{var p=array<vec2f,6>(vec2f(-1,-1),vec2f(1,-1),vec2f(-1,1),vec2f(-1,1),vec2f(1,-1),vec2f(1,1));var v=p[i];var px=u.x+u.sx*v.x;var py=u.y+u.sy*v.y;return vec4f((px/u.w)*2-1,1-(py/u.h)*2,0,1);}@fragment fn fs()->@location(0) vec4f{return u.c;};";
function supports(){return typeof navigator!=="undefined"&&!!navigator.gpu;}
function parseColor(c){
  if(!c||c.indexOf("#")===0){
    var h=(c||"#888").replace("#","");if(h.length===3)h=h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
    return[parseInt(h.slice(0,2),16)/255,parseInt(h.slice(2,4),16)/255,parseInt(h.slice(4,6),16)/255,1];
  }
  var m=/rgba?\(([^)]+)\)/.exec(c||"");
  if(m){var p=m[1].split(",").map(function(x){return parseFloat(x.trim());});return[p[0]/255||p[0],p[1]/255||p[1],p[2]/255||p[2],p[3]!=null?p[3]:1];}
  return[0.53,0.53,0.53,1];
}
function ensure(canvas){
  if(W.ready)return Promise.resolve(true);
  if(W.initing)return W.initing;
  if(!supports())return Promise.resolve(false);
  W.initing=navigator.gpu.requestAdapter().then(function(a){return a&&a.requestDevice();}).then(function(dev){
    if(!dev)return false;
    W.device=dev;W.ctx=canvas.getContext("webgpu");if(!W.ctx)return false;
    W.format=navigator.gpu.getPreferredCanvasFormat();
    W.ctx.configure({device:dev,format:W.format,alphaMode:"premultiplied"});
    var sh=dev.createShaderModule({code:WGSL});
    W.pipeline=dev.createRenderPipeline({layout:"auto",vertex:{module:sh,entryPoint:"vs"},fragment:{module:sh,entryPoint:"fs",targets:[{format:W.format}]},primitive:{topology:"triangle-list"}});
    W.uniformBuf=dev.createBuffer({size:48,usage:GPUBufferUsage.UNIFORM|GPUBufferUsage.COPY_DST});
    W.bindGroup=dev.createBindGroup({layout:W.pipeline.getBindGroupLayout(0),entries:[{binding:0,resource:{buffer:W.uniformBuf}}]});
    W.ready=true;return true;
  }).catch(function(){return false;});
  return W.initing;
}
function draw(G,g){
  if(!W.ready||!W.device||!W.ctx)return false;
  var dev=W.device,enc=dev.createCommandEncoder(),pass=enc.beginRenderPass({colorAttachments:[{view:W.ctx.getCurrentTexture().createView(),clearValue:{r:0.53,g:0.81,b:0.92,a:1},loadOp:"clear",storeOp:"store"}]});
  pass.setPipeline(W.pipeline);pass.setBindGroup(0,W.bindGroup);
  (G.nodes||[]).forEach(function(n){
    var lx=typeof n.x==="string"&&n.x.indexOf(".")>0?g(n.x):+n.x;
    var ly=typeof n.y==="string"&&n.y.indexOf(".")>0?g(n.y):+n.y;
    var col=parseColor(n.c||"#888");
    var u=new Float32Array([G.width,G.height,col[0],col[1],col[2],col[3],lx,ly,n.w,n.h,0,0]);
    dev.queue.writeBuffer(W.uniformBuf,0,u);
    pass.draw(6);
  });
  pass.end();dev.queue.submit([enc.finish()]);
  return true;
}
window.__echoui=window.__echoui||{};
window.__echoui.webgpu={supports:supports,ensure:ensure,draw:draw};
})();
