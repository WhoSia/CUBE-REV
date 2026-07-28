(function(global){
  'use strict';

  class CubeDragController {
    constructor(options){
      const required=['element','hitTestCube','canRotateCube','applyWholeCubeMove','getCamera','setCamera','setPreview','clearPreview','logEvent'];
      for(const key of required){if(typeof options[key] === 'undefined')throw new Error('CubeDragController missing option: '+key);}
      this.element=options.element;
      this.hitTestCube=options.hitTestCube;
      this.canRotateCube=options.canRotateCube;
      this.applyWholeCubeMove=options.applyWholeCubeMove;
      this.getCamera=options.getCamera;
      this.setCamera=options.setCamera;
      this.setPreview=options.setPreview;
      this.clearPreview=options.clearPreview;
      this.logEvent=options.logEvent;
      this.onCameraGestureStart=options.onCameraGestureStart||(()=>{});
      this.onCubeGestureCommitted=options.onCubeGestureCommitted||(()=>{});
      this.thresholdPx=Number(options.thresholdPx)||34;
      this.previewQuarterTurnPx=Number(options.previewQuarterTurnPx)||110;
      this.pitchLimit=Number(options.pitchLimit)||1.35;
      this.cameraSensitivity=Number(options.cameraSensitivity)||0.008;
      this.active=null;
      this.bound={
        down:e=>this.onPointerDown(e),
        move:e=>this.onPointerMove(e),
        up:e=>this.onPointerUp(e),
        cancel:e=>this.onPointerCancel(e),
        lost:e=>this.onLostPointerCapture(e)
      };
    }

    attach(){
      this.element.addEventListener('pointerdown',this.bound.down);
      this.element.addEventListener('pointermove',this.bound.move);
      this.element.addEventListener('pointerup',this.bound.up);
      this.element.addEventListener('pointercancel',this.bound.cancel);
      this.element.addEventListener('lostpointercapture',this.bound.lost);
      return this;
    }

    detach(){
      this.element.removeEventListener('pointerdown',this.bound.down);
      this.element.removeEventListener('pointermove',this.bound.move);
      this.element.removeEventListener('pointerup',this.bound.up);
      this.element.removeEventListener('pointercancel',this.bound.cancel);
      this.element.removeEventListener('lostpointercapture',this.bound.lost);
      this.clearPreview();
      this.active=null;
    }

    point(e){
      const rect=this.element.getBoundingClientRect();
      return {x:e.clientX-rect.left,y:e.clientY-rect.top,clientX:e.clientX,clientY:e.clientY};
    }

    onPointerDown(e){
      if(e.button!==0||e.isPrimary===false)return;
      const p=this.point(e);
      const overCube=!!this.hitTestCube(p.x,p.y);
      const cubeGesture=overCube&&this.canRotateCube();
      const camera=this.getCamera();
      this.active={
        id:e.pointerId,
        mode:cubeGesture?'cube':'camera',
        start:p,
        last:p,
        startedAt:performance.now(),
        cameraStart:{...camera},
        sampleCount:1,
        maxDistance:0,
        pointerType:e.pointerType||'mouse',modifiers:{shiftKey:e.shiftKey,altKey:e.altKey,ctrlKey:e.ctrlKey,metaKey:e.metaKey}
      };
      this.element.setPointerCapture?.(e.pointerId);
      if(cubeGesture){
        this.element.style.cursor='grabbing';
        this.logEvent('cube_drag_start',{x:+p.x.toFixed(2),y:+p.y.toFixed(2),input_method:'pointer',pointer_type:this.active.pointerType,gesture_threshold_px:this.thresholdPx});
      }else{
        this.onCameraGestureStart();
        this.element.style.cursor='grabbing';
        this.logEvent('camera_drag_start',{yaw:camera.yaw,pitch:camera.pitch,x:+p.x.toFixed(2),y:+p.y.toFixed(2),started_over_cube:overCube,cube_rotation_available:!!this.canRotateCube()});
      }
      e.preventDefault();
    }

    onPointerMove(e){
      const p=this.point(e);
      if(!this.active||this.active.id!==e.pointerId){
        this.element.style.cursor=this.hitTestCube(p.x,p.y)&&this.canRotateCube()?'all-scroll':'grab';
        return;
      }
      const a=this.active;
      a.last=p;a.sampleCount++;
      const dx=p.x-a.start.x,dy=p.y-a.start.y;
      a.maxDistance=Math.max(a.maxDistance,Math.hypot(dx,dy));
      if(a.mode==='camera'){
        this.setCamera({
          yaw:a.cameraStart.yaw+dx*this.cameraSensitivity,
          pitch:Math.max(-this.pitchLimit,Math.min(this.pitchLimit,a.cameraStart.pitch+dy*this.cameraSensitivity)),
          zoom:a.cameraStart.zoom
        });
      }else{
        const horizontal=Math.abs(dx)>=Math.abs(dy);
        const axis=horizontal?'y':'x';
        const rawAngle=horizontal?dx*(Math.PI/2/this.previewQuarterTurnPx):dy*(Math.PI/2/this.previewQuarterTurnPx);
        const angle=Math.max(-Math.PI/2,Math.min(Math.PI/2,rawAngle));
        this.setPreview({axis,angle,dx,dy});
      }
      e.preventDefault();
    }

    classifyMove(dx,dy){
      if(Math.hypot(dx,dy)<this.thresholdPx)return null;
      if(Math.abs(dx)>=Math.abs(dy))return dx>0?"y'":'y';
      return dy>0?"x'":'x';
    }

    finishActive(e,cancelled){
      const a=this.active;if(!a)return;
      const p=e?this.point(e):a.last;
      const dx=p.x-a.start.x,dy=p.y-a.start.y;
      const duration=performance.now()-a.startedAt;
      if(a.mode==='camera'){
        const camera=this.getCamera();
        this.logEvent(cancelled?'camera_drag_cancelled':'camera_drag_end',{
          yaw:camera.yaw,pitch:camera.pitch,duration_ms:+duration.toFixed(3),distance_px:+Math.hypot(dx,dy).toFixed(2),sample_count:a.sampleCount
        });
      }else{
        this.clearPreview();
        const move=cancelled?null:this.classifyMove(dx,dy);
        const payload={dx:+dx.toFixed(2),dy:+dy.toFixed(2),distance_px:+Math.hypot(dx,dy).toFixed(2),duration_ms:+duration.toFixed(3),sample_count:a.sampleCount,recognized_move:move,committed:false};
        if(move&&this.canRotateCube()){
          payload.committed=!!this.applyWholeCubeMove(move,'cube_drag');
          if(payload.committed)this.onCubeGestureCommitted(move,duration);
        }
        this.logEvent(cancelled?'cube_drag_cancelled':'cube_drag_end',payload);
      }
      this.active=null;
      try{if(this.element.hasPointerCapture?.(a.id))this.element.releasePointerCapture(a.id);}catch(_){ }
      this.element.style.cursor=this.hitTestCube(p.x,p.y)&&this.canRotateCube()?'all-scroll':'grab';
    }

    onPointerUp(e){if(this.active&&this.active.id===e.pointerId){this.finishActive(e,false);e.preventDefault();}}
    onPointerCancel(e){if(this.active&&this.active.id===e.pointerId)this.finishActive(e,true);}
    onLostPointerCapture(e){if(this.active&&this.active.id===e.pointerId)this.finishActive(e,true);}
  }

  global.CubeDragController=CubeDragController;
})(window);
