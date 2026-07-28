(function(global){
  'use strict';

  class CameraZoomController{
    constructor(options={}){
      if(!options.element)throw new Error('CameraZoomController requires element.');
      if(typeof options.getZoom!=='function'||typeof options.setZoom!=='function')throw new Error('CameraZoomController requires getZoom and setZoom.');
      this.element=options.element;
      this.getZoom=options.getZoom;
      this.setZoom=options.setZoom;
      this.cancelDrag=options.cancelDrag||(()=>{});
      this.logEvent=options.logEvent||(()=>{});
      this.onZoomStart=options.onZoomStart||(()=>{});
      this.minZoom=Number(options.minZoom)||0.55;
      this.maxZoom=Number(options.maxZoom)||1.85;
      this.wheelSensitivity=Number(options.wheelSensitivity)||0.00115;
      this.pointers=new Map();
      this.pinch=null;
      this.wheelEndTimer=null;
      this.wheelActive=false;
      this.bound={
        wheel:e=>this.onWheel(e),
        down:e=>this.onPointerDown(e),
        move:e=>this.onPointerMove(e),
        up:e=>this.onPointerEnd(e),
        cancel:e=>this.onPointerEnd(e)
      };
    }
    clamp(value){return Math.max(this.minZoom,Math.min(this.maxZoom,Number(value)||1));}
    attach(){
      this.element.addEventListener('wheel',this.bound.wheel,{passive:false});
      this.element.addEventListener('pointerdown',this.bound.down,{capture:true});
      this.element.addEventListener('pointermove',this.bound.move,{capture:true});
      this.element.addEventListener('pointerup',this.bound.up,{capture:true});
      this.element.addEventListener('pointercancel',this.bound.cancel,{capture:true});
      return this;
    }
    detach(){
      this.element.removeEventListener('wheel',this.bound.wheel,{capture:false});
      this.element.removeEventListener('pointerdown',this.bound.down,{capture:true});
      this.element.removeEventListener('pointermove',this.bound.move,{capture:true});
      this.element.removeEventListener('pointerup',this.bound.up,{capture:true});
      this.element.removeEventListener('pointercancel',this.bound.cancel,{capture:true});
      clearTimeout(this.wheelEndTimer);this.pointers.clear();this.pinch=null;
    }
    onWheel(event){
      event.preventDefault();
      const source=event.ctrlKey?'trackpad_pinch':'wheel_or_trackpad_scroll';
      if(!this.wheelActive){
        this.wheelActive=true;this.onZoomStart(source);
        this.logEvent('camera_zoom_start',{source,zoom:this.getZoom()});
      }
      const before=this.getZoom();
      const delta=Math.max(-180,Math.min(180,event.deltaY));
      const after=this.clamp(before*Math.exp(-delta*this.wheelSensitivity));
      this.setZoom(after,{source,center_x:event.clientX,center_y:event.clientY});
      this.logEvent('camera_zoom',{source,zoom_before:+before.toFixed(5),zoom_after:+after.toFixed(5),delta_y:+event.deltaY.toFixed(3),ctrl_key:!!event.ctrlKey});
      clearTimeout(this.wheelEndTimer);
      this.wheelEndTimer=setTimeout(()=>{
        this.wheelActive=false;
        this.logEvent('camera_zoom_end',{source,zoom:this.getZoom()});
      },180);
    }
    touchPointers(){return [...this.pointers.values()].filter(p=>p.pointerType==='touch');}
    distance(a,b){return Math.hypot(a.x-b.x,a.y-b.y);}
    onPointerDown(event){
      if(event.pointerType!=='touch')return;
      this.pointers.set(event.pointerId,{id:event.pointerId,x:event.clientX,y:event.clientY,pointerType:'touch'});
      const touches=this.touchPointers();
      if(touches.length===2){
        this.cancelDrag('pinch_zoom_started');
        const [a,b]=touches;const distance=Math.max(8,this.distance(a,b));
        this.pinch={startDistance:distance,startZoom:this.getZoom(),lastZoom:this.getZoom(),startedAt:performance.now(),sampleCount:0};
        this.element.dataset.pinchZoom='true';
        this.onZoomStart('touch_pinch');
        this.logEvent('camera_zoom_start',{source:'touch_pinch',zoom:this.getZoom(),finger_count:2,start_distance_px:+distance.toFixed(2)});
        event.preventDefault();
      }
    }
    onPointerMove(event){
      if(event.pointerType!=='touch'||!this.pointers.has(event.pointerId))return;
      const p=this.pointers.get(event.pointerId);p.x=event.clientX;p.y=event.clientY;
      if(!this.pinch)return;
      const touches=this.touchPointers();if(touches.length<2)return;
      const [a,b]=touches;const distance=Math.max(8,this.distance(a,b));
      const next=this.clamp(this.pinch.startZoom*(distance/this.pinch.startDistance));
      this.pinch.lastZoom=next;this.pinch.sampleCount++;
      this.setZoom(next,{source:'touch_pinch',center_x:(a.x+b.x)/2,center_y:(a.y+b.y)/2});
      event.preventDefault();
    }
    onPointerEnd(event){
      if(event.pointerType!=='touch')return;
      this.pointers.delete(event.pointerId);
      if(this.pinch&&this.touchPointers().length<2){
        const info=this.pinch;this.pinch=null;delete this.element.dataset.pinchZoom;
        this.logEvent('camera_zoom_end',{source:'touch_pinch',zoom:this.getZoom(),duration_ms:+(performance.now()-info.startedAt).toFixed(3),sample_count:info.sampleCount});
      }
    }
  }

  global.CameraZoomController=CameraZoomController;
})(window);
