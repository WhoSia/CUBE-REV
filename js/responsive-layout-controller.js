(function(global){
  'use strict';

  class ResponsiveLayoutController {
    constructor(options={}){
      this.root=options.root||document.documentElement;
      this.sheet=options.sheet||null;
      this.backdrop=options.backdrop||null;
      this.openButton=options.openButton||null;
      this.closeButton=options.closeButton||null;
      this.logEvent=options.logEvent||(()=>{});
      this.onViewportChange=options.onViewportChange||(()=>{});
      this.phoneMax=Math.max(560,Number(options.phoneMax)||720);
      this.tabletMax=Math.max(this.phoneMax+1,Number(options.tabletMax)||1100);
      this.state=null;
      this.lastFocused=null;
      this.bound={
        update:()=>this.update(),
        open:()=>this.openSheet('button'),
        close:()=>this.closeSheet('button'),
        backdrop:()=>this.closeSheet('backdrop'),
        keydown:e=>this.onKeyDown(e)
      };
    }

    attach(){
      this.openButton?.addEventListener('click',this.bound.open);
      this.closeButton?.addEventListener('click',this.bound.close);
      this.backdrop?.addEventListener('click',this.bound.backdrop);
      document.addEventListener('keydown',this.bound.keydown);
      global.addEventListener('resize',this.bound.update,{passive:true});
      global.addEventListener('orientationchange',this.bound.update,{passive:true});
      global.visualViewport?.addEventListener('resize',this.bound.update,{passive:true});
      global.visualViewport?.addEventListener('scroll',this.bound.update,{passive:true});
      this.update(true);
      return this;
    }

    detach(){
      this.openButton?.removeEventListener('click',this.bound.open);
      this.closeButton?.removeEventListener('click',this.bound.close);
      this.backdrop?.removeEventListener('click',this.bound.backdrop);
      document.removeEventListener('keydown',this.bound.keydown);
      global.removeEventListener('resize',this.bound.update);
      global.removeEventListener('orientationchange',this.bound.update);
      global.visualViewport?.removeEventListener('resize',this.bound.update);
      global.visualViewport?.removeEventListener('scroll',this.bound.update);
    }

    viewport(){
      const vv=global.visualViewport;
      return {
        // Form-factor decisions use the layout viewport. visualViewport.width can
        // change during pinch zoom and should not switch the whole interface mode.
        width:Math.round(document.documentElement.clientWidth||global.innerWidth||vv?.width||0),
        // Height follows the visual viewport so mobile browser bars and keyboards
        // do not cover the canvas or the fixed action bar.
        height:Math.round(vv?.height||global.innerHeight||document.documentElement.clientHeight||0),
        scale:Number(vv?.scale||1)
      };
    }

    classify(width){
      if(width<=this.phoneMax)return 'phone';
      if(width<=this.tabletMax)return 'tablet';
      return 'desktop';
    }

    snapshot(){
      const viewport=this.viewport();
      const coarse=global.matchMedia?.('(pointer: coarse)').matches===true;
      const hover=global.matchMedia?.('(hover: hover)').matches===true;
      const reducedMotion=global.matchMedia?.('(prefers-reduced-motion: reduce)').matches===true;
      const orientation=viewport.width>=viewport.height?'landscape':'portrait';
      return {
        form_factor:this.classify(viewport.width),
        viewport_width:viewport.width,
        viewport_height:viewport.height,
        viewport_scale:viewport.scale,
        orientation,
        pointer_mode:coarse?'coarse':'fine',
        hover_available:hover,
        reduced_motion:reducedMotion,
        max_touch_points:Number(navigator.maxTouchPoints||0)
      };
    }

    update(initial=false){
      const next=this.snapshot();
      this.root.dataset.formFactor=next.form_factor;
      this.root.dataset.pointerMode=next.pointer_mode;
      this.root.dataset.orientation=next.orientation;
      this.root.style.setProperty('--visual-viewport-height',next.viewport_height+'px');
      this.root.style.setProperty('--visual-viewport-width',next.viewport_width+'px');
      if(next.form_factor!=='phone')this.closeSheet('layout_change',false);
      const changed=!this.state||Object.keys(next).some(key=>next[key]!==this.state[key]);
      if(changed){
        const previous=this.state;
        this.state=next;
        if(!initial)this.logEvent('responsive_layout_change',{previous,next});
        this.onViewportChange(next,previous);
      }
    }

    isOpen(){return !!this.sheet?.classList.contains('is-open');}

    openSheet(source='unknown'){
      if(!this.sheet||this.state?.form_factor!=='phone')return false;
      this.lastFocused=document.activeElement instanceof HTMLElement?document.activeElement:null;
      this.sheet.classList.add('is-open');
      this.sheet.setAttribute('aria-hidden','false');
      this.backdrop?.classList.remove('hidden');
      this.openButton?.setAttribute('aria-expanded','true');
      document.body.classList.add('mobile-sheet-open');
      this.closeButton?.focus({preventScroll:true});
      this.logEvent('mobile_control_sheet_opened',{source,layout:this.snapshot()});
      return true;
    }

    closeSheet(source='unknown',restoreFocus=true){
      if(!this.sheet)return false;
      const wasOpen=this.isOpen();
      this.sheet.classList.remove('is-open');
      this.sheet.setAttribute('aria-hidden',this.state?.form_factor==='phone'?'true':'false');
      this.backdrop?.classList.add('hidden');
      this.openButton?.setAttribute('aria-expanded','false');
      document.body.classList.remove('mobile-sheet-open');
      if(wasOpen){
        this.logEvent('mobile_control_sheet_closed',{source});
        if(restoreFocus)this.lastFocused?.focus?.({preventScroll:true});
      }
      return wasOpen;
    }

    focusableElements(){
      if(!this.sheet)return [];
      return [...this.sheet.querySelectorAll('button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])')]
        .filter(el=>!el.disabled&&!el.hidden&&el.getClientRects().length>0);
    }

    onKeyDown(event){
      if(event.key==='Escape'&&this.isOpen()){
        event.preventDefault();
        this.closeSheet('escape');
        return;
      }
      if(event.key!=='Tab'||!this.isOpen())return;
      const items=this.focusableElements();
      if(!items.length)return;
      const first=items[0],last=items[items.length-1];
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
      else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
    }
  }

  global.ResponsiveLayoutController=ResponsiveLayoutController;
})(window);
