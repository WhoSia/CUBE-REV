(function(global){
  'use strict';

  class CubeRevCollectorClient {
    static normalizeConfig(raw,version){
      const defaults={enabled:false,endpoint:'',manualUploadUrl:'',studyId:`CUBE-REV-${version}`,studyToken:'',autoSubmitOnComplete:true,gzipWhenAvailable:true,timeoutMs:45000};
      const merged={...defaults,...(raw&&typeof raw==='object'?raw:{})};
      merged.enabled=!!merged.enabled;
      merged.endpoint=String(merged.endpoint||'').trim();
      merged.manualUploadUrl=String(merged.manualUploadUrl||merged.endpoint||'').trim();
      merged.studyId=String(merged.studyId||defaults.studyId).trim();
      merged.studyToken=String(merged.studyToken||'');
      merged.autoSubmitOnComplete=merged.autoSubmitOnComplete!==false;
      merged.gzipWhenAvailable=merged.gzipWhenAvailable!==false;
      merged.timeoutMs=Math.max(10000,Number(merged.timeoutMs)||45000);
      return Object.freeze(merged);
    }

    constructor(options){
      this.config=options.config;this.version=options.version;this.getSession=options.getSession;this.exportSession=options.exportSession;
      this.logEvent=options.logEvent||(()=>{});this.persist=options.persist||(()=>{});this.setStatus=options.setStatus||(()=>{});
      this.randomHex=options.randomHex;this.hashString=options.hashString;this.inFlight=null;
    }

    isAutomaticConfigured(){return this.config.enabled&&/^https:\/\//i.test(this.config.endpoint);}
    isManualPortalConfigured(){return /^https:\/\//i.test(this.config.manualUploadUrl||this.config.endpoint);}

    manualPortalUrl(sessionId){
      if(!this.isManualPortalConfigured())return '';
      const url=new URL(this.config.manualUploadUrl||this.config.endpoint);
      url.searchParams.set('source','cube-rev-experiment');
      if(sessionId){url.searchParams.set('session_id',sessionId);url.searchParams.set('expected_file',sessionId+'.json');}
      return url.toString();
    }

    openManualPortal(sessionId){
      const url=this.manualPortalUrl(sessionId);if(!url)return false;
      const opened=global.open(url,'_blank','noopener,noreferrer');
      this.logEvent('collection_portal_opened',{session_id:sessionId||null,opened:!!opened,portal_host:new URL(url).host});this.persist();return !!opened;
    }

    arrayBufferToBase64(buffer){
      const bytes=new Uint8Array(buffer);let out='';const chunk=0x8000;
      for(let i=0;i<bytes.length;i+=chunk)out+=String.fromCharCode(...bytes.subarray(i,Math.min(i+chunk,bytes.length)));
      return btoa(out);
    }

    async encodePayload(jsonText){
      const originalBytes=new TextEncoder().encode(jsonText).byteLength;
      if(this.config.gzipWhenAvailable&&'CompressionStream' in globalThis){
        const compressed=await new Response(new Blob([jsonText]).stream().pipeThrough(new CompressionStream('gzip'))).arrayBuffer();
        return {payload:this.arrayBufferToBase64(compressed),encoding:'gzip-base64',original_bytes:originalBytes,transmitted_bytes:compressed.byteLength};
      }
      return {payload:jsonText,encoding:'json',original_bytes:originalBytes,transmitted_bytes:originalBytes};
    }

    async postOpaque(fields){
      const body=new URLSearchParams();for(const [k,v] of Object.entries(fields))body.set(k,String(v??''));
      const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),this.config.timeoutMs);
      try{
        await fetch(this.config.endpoint,{method:'POST',mode:'no-cors',redirect:'follow',credentials:'omit',headers:{'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'},body:body.toString(),signal:controller.signal,keepalive:false});
        return {ok:true,status:'sent_unconfirmed',transport:'fetch_no_cors',received_at:new Date().toISOString(),file_name:fields.session_id+'.json'};
      }finally{clearTimeout(timer);}
    }

    async submit({manual=false}={}){
      const session=this.getSession();if(!session)throw new Error('제출할 세션이 없습니다.');
      if(!this.isAutomaticConfigured())throw new Error('자동 제출 연결 정보를 불러오지 못했습니다. 페이지를 강력 새로고침한 뒤 다시 시도해 주세요.');
      if(this.inFlight)return this.inFlight;
      this.inFlight=(async()=>{
        const startedAt=new Date().toISOString();session.data_submission=session.data_submission||{};
        session.data_submission.status='preparing';session.data_submission.attempt_count=(session.data_submission.attempt_count||0)+1;
        session.data_submission.last_attempt_at=startedAt;session.data_submission.manual=!!manual;
        this.logEvent('submission_attempted',{attempt_count:session.data_submission.attempt_count,study_id:this.config.studyId,manual:!!manual});
        this.persist();this.setStatus('결과 파일을 제출할 준비를 하고 있습니다.','info',{pending:true});
        const jsonText=JSON.stringify(this.exportSession());const encoded=await this.encodePayload(jsonText);
        const nonce=this.randomHex(12),checksum=this.hashString(jsonText).toString(16).padStart(8,'0');
        session.data_submission.status='uploading';Object.assign(session.data_submission,{encoding:encoded.encoding,original_bytes:encoded.original_bytes,transmitted_bytes:encoded.transmitted_bytes,checksum_fnv1a32:checksum});
        this.setStatus('결과 파일을 자동 제출하고 있습니다. 잠시만 기다려 주세요.','info',{pending:true});
        try{
          const ack=await this.postOpaque({payload:encoded.payload,encoding:encoded.encoding,study_id:this.config.studyId,study_token:this.config.studyToken,session_id:session.session_id,version:this.version,checksum_fnv1a32:checksum,original_bytes:encoded.original_bytes,submission_nonce:nonce});
          Object.assign(session.data_submission,{status:ack.status,received_at:ack.received_at,receipt_id:null,file_name:ack.file_name,last_error:null,transport:ack.transport,response_verification:'not_available_cross_origin'});
          this.logEvent('submission_dispatched',{status:ack.status,file_name:ack.file_name,submission_method:'automatic',transport:ack.transport,response_verified:false});
          this.persist();
          this.setStatus('자동 제출 요청을 보냈습니다. 브라우저 보안상 수집기 응답을 직접 읽을 수는 없지만, 전송 과정은 정상적으로 끝났습니다.','success',{pending:false});
          return ack;
        }catch(error){
          session.data_submission.status='failed';session.data_submission.last_error=String(error?.name==='AbortError'?'전송 제한 시간을 넘겼습니다.':error?.message||error);
          this.logEvent('submission_failed',{error:session.data_submission.last_error,manual_portal_available:this.isManualPortalConfigured()});this.persist();
          this.setStatus(`자동 제출 요청을 보내지 못했습니다. JSON을 저장한 뒤 제출 페이지에서 직접 올려 주세요. (${session.data_submission.last_error})`,'error',{pending:false});
          throw error;
        }finally{this.inFlight=null;}
      })();
      return this.inFlight;
    }
  }

  global.CubeRevCollectorClient=CubeRevCollectorClient;
})(window);
