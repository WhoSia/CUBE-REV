(function(global){
  'use strict';

  class CubeDragController {
    constructor(options){
      const required=['element','pickSticker','resolveStickerDrag','canTurnFace','applyFaceMove','getCamera','setCamera','setPreview','clearPreview','logEvent'];
      for(const key of required){if(typeof options[key] === 'undefined')throw new Error('CubeDragController missing option: '+key);}
      this.element=options.element;
      this.pickSticker=options.pickSticker;
      this.resolveStickerDrag=options.resolveStickerDrag;
      this.canTurnFace=options.canTurnFace;
      this.applyFaceMove=options.applyFaceMove;
      this.getCamera=options.getCamera;
      this.setCamera=options.setCamera;
      this.setPreview=options.setPreview;
      this.clearPreview=options.clearPreview;
      this.logEvent=options.logEvent;
      this.onCameraGestureStart=options.onCameraGestureStart||(()=>{});
      this.onStickerGestureCommitted=options.onStickerGestureCommitted||(()=>{});
      this.thresholdPx=Math.max(24,Number(options.thresholdPx)||42);
      this.thresholdTouchPx=Math.max(24,Number(options.thresholdTouchPx)||34);
      this.thresholdPenPx=Math.max(24,Number(options.thresholdPenPx)||36);
      this.minDirectionScore=Math.max(0.5,Math.min(0.99,Number(options.minDirectionScore)||0.72));
      this.minScoreMargin=Math.max(0,Math.min(0.5,Number(options.minScoreMargin)||0.08));
      this.minStraightness=Math.max(0.25,Math.min(1,Number(options.minStraightness)||0.55));
      this.pitchLimit=Number(options.pitchLimit)||1.35;
      this.cameraSensitivity=Number(options.cameraSensitivity)||0.008;
      this.cameraSensitivityTouch=Number(options.cameraSensitivityTouch)||0.0065;
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

    cancelActive(reason='external_cancel'){
      if(!this.active)return false;
      const a=this.active;
      this.clearPreview();
      this.logEvent(a.mode==='sticker'?'sticker_drag_cancelled':'camera_drag_cancelled',{
        reason,
        pointer_type:a.pointerType,
        duration_ms:+(performance.now()-a.startedAt).toFixed(3),
        sample_count:a.sampleCount
      });
      this.active=null;
      try{if(this.element.hasPointerCapture?.(a.id))this.element.releasePointerCapture(a.id);}catch(_){ }
      this.element.style.cursor='grab';
      return true;
    }

    point(e){
      const rect=this.element.getBoundingClientRect();
      return {x:e.clientX-rect.left,y:e.clientY-rect.top,clientX:e.clientX,clientY:e.clientY};
    }

    onPointerDown(e){
      if(this.element.dataset.pinchZoom==='true')return;
      if(e.button!==0||e.isPrimary===false)return;
      const p=this.point(e);
      const sticker=this.canTurnFace()?this.pickSticker(p.x,p.y):null;
      const camera=this.getCamera();
      this.active={
        id:e.pointerId,
        mode:sticker?'sticker':'camera',
        sticker,
        start:p,
        last:p,
        previous:p,
        startedAt:performance.now(),
        cameraStart:{...camera},
        sampleCount:1,
        pathLength:0,
        maxDistance:0,
        lastResolution:null,
        pointerType:e.pointerType||'mouse',
        thresholdPx:(e.pointerType==='touch'?this.thresholdTouchPx:e.pointerType==='pen'?this.thresholdPenPx:this.thresholdPx),
        modifiers:{shiftKey:e.shiftKey,altKey:e.altKey,ctrlKey:e.ctrlKey,metaKey:e.metaKey}
      };
      this.element.setPointerCapture?.(e.pointerId);
      this.element.style.cursor='grabbing';
      if(sticker){
        this.logEvent('sticker_drag_start',{
          x:+p.x.toFixed(2),y:+p.y.toFixed(2),pointer_type:this.active.pointerType,
          sticker_face:sticker.face,sticker_cell:sticker.cell,cubie_pos:sticker.pos,
          gesture_threshold_px:this.active.thresholdPx,turn_policy:'single_quarter_turn_only'
        });
      }else{
        this.onCameraGestureStart();
        this.logEvent('camera_drag_start',{yaw:camera.yaw,pitch:camera.pitch,x:+p.x.toFixed(2),y:+p.y.toFixed(2),started_on_sticker:false});
      }
      e.preventDefault();
    }

    onPointerMove(e){
      if(this.element.dataset.pinchZoom==='true'){if(this.active)this.cancelActive('pinch_zoom_active');return;}
      const p=this.point(e);
      if(!this.active||this.active.id!==e.pointerId){
        const sticker=this.canTurnFace()?this.pickSticker(p.x,p.y):null;
        this.element.style.cursor=sticker?'grab':'grab';
        return;
      }
      const a=this.active;
      a.pathLength+=Math.hypot(p.x-a.previous.x,p.y-a.previous.y);
      a.previous=p;a.last=p;a.sampleCount++;
      const dx=p.x-a.start.x,dy=p.y-a.start.y;
      a.maxDistance=Math.max(a.maxDistance,Math.hypot(dx,dy));
      if(a.mode==='camera'){
        this.setCamera({
          yaw:a.cameraStart.yaw+dx*(a.pointerType==='touch'?this.cameraSensitivityTouch:this.cameraSensitivity),
          pitch:Math.max(-this.pitchLimit,Math.min(this.pitchLimit,a.cameraStart.pitch+dy*(a.pointerType==='touch'?this.cameraSensitivityTouch:this.cameraSensitivity))),
          zoom:a.cameraStart.zoom
        });
      }else{
        const resolution=this.resolveStickerDrag(a.sticker,dx,dy,{commit:false,thresholdPx:a.thresholdPx,pointerType:a.pointerType});
        a.lastResolution=resolution;
        if(resolution?.preview)this.setPreview(resolution.preview);else this.clearPreview();
      }
      e.preventDefault();
    }

    evaluateGesture(a,p){
      const dx=p.x-a.start.x,dy=p.y-a.start.y;
      const distance=Math.hypot(dx,dy);
      const straightness=a.pathLength>0?Math.min(1,distance/a.pathLength):1;
      const resolution=this.resolveStickerDrag(a.sticker,dx,dy,{commit:true,thresholdPx:a.thresholdPx,pointerType:a.pointerType});
      const score=Number(resolution?.score||0);
      const margin=Number(resolution?.scoreMargin||0);
      const accepted=!!resolution?.token&&distance>=a.thresholdPx&&score>=this.minDirectionScore&&margin>=this.minScoreMargin&&straightness>=this.minStraightness;
      return {dx,dy,distance,straightness,resolution,accepted};
    }

    finishActive(e,cancelled){
      const a=this.active;if(!a)return;
      const p=e?this.point(e):a.last;
      const duration=performance.now()-a.startedAt;
      if(a.mode==='camera'){
        const dx=p.x-a.start.x,dy=p.y-a.start.y,camera=this.getCamera();
        this.logEvent(cancelled?'camera_drag_cancelled':'camera_drag_end',{
          yaw:camera.yaw,pitch:camera.pitch,duration_ms:+duration.toFixed(3),distance_px:+Math.hypot(dx,dy).toFixed(2),sample_count:a.sampleCount
        });
      }else{
        this.clearPreview();
        const result=this.evaluateGesture(a,p);
        let committed=false;
        if(!cancelled&&result.accepted&&this.canTurnFace()){
          committed=!!this.applyFaceMove(result.resolution.token,'sticker_drag');
          if(committed)this.onStickerGestureCommitted(result.resolution.token,duration);
        }
        const r=result.resolution||{};
        this.logEvent(cancelled?'sticker_drag_cancelled':'sticker_drag_end',{
          sticker_face:a.sticker.face,sticker_cell:a.sticker.cell,cubie_pos:a.sticker.pos,pointer_type:a.pointerType,gesture_threshold_px:a.thresholdPx,
          dx:+result.dx.toFixed(2),dy:+result.dy.toFixed(2),distance_px:+result.distance.toFixed(2),path_length_px:+a.pathLength.toFixed(2),
          straightness:+result.straightness.toFixed(4),duration_ms:+duration.toFixed(3),sample_count:a.sampleCount,
          candidate_face:r.face||null,recognized_move:result.accepted?r.token:null,direction_score:r.score==null?null:+r.score.toFixed(4),
          score_margin:r.scoreMargin==null?null:+r.scoreMargin.toFixed(4),committed,
          rejection_reason:cancelled?'pointer_cancelled':result.accepted?null:(result.distance<a.thresholdPx?'too_short':result.straightness<this.minStraightness?'path_not_straight':(r.score||0)<this.minDirectionScore?'direction_unclear':(r.scoreMargin||0)<this.minScoreMargin?'axis_ambiguous':'unresolved'),
          turn_policy:'single_quarter_turn_only',double_turn_generated:false
        });
      }
      this.active=null;
      try{if(this.element.hasPointerCapture?.(a.id))this.element.releasePointerCapture(a.id);}catch(_){ }
      const sticker=this.canTurnFace()?this.pickSticker(p.x,p.y):null;
      this.element.style.cursor=sticker?'grab':'grab';
    }

    onPointerUp(e){if(this.active&&this.active.id===e.pointerId){this.finishActive(e,false);e.preventDefault();}}
    onPointerCancel(e){if(this.active&&this.active.id===e.pointerId)this.finishActive(e,true);}
    onLostPointerCapture(e){if(this.active&&this.active.id===e.pointerId)this.finishActive(e,true);}
  }

  global.CubeDragController=CubeDragController;
})(window);
