(function(global){
  'use strict';

  class CubeRevCollectorClient {
    static normalizeConfig(raw,version){
      const defaults={enabled:false,endpoint:'',manualUploadUrl:'',studyId:`CUBE-REV-${version}`,studyToken:'',autoSubmitOnComplete:true,gzipWhenAvailable:true,timeoutMs:30000};
      const merged={...defaults,...(raw&&typeof raw==='object'?raw:{})};
      merged.enabled=!!merged.enabled;
      merged.endpoint=String(merged.endpoint||'').trim();
      merged.manualUploadUrl=String(merged.manualUploadUrl||merged.endpoint||'').trim();
      merged.studyId=String(merged.studyId||defaults.studyId).trim();
      merged.studyToken=String(merged.studyToken||'');
      merged.autoSubmitOnComplete=merged.autoSubmitOnComplete!==false;
      merged.gzipWhenAvailable=merged.gzipWhenAvailable!==false;
      merged.timeoutMs=Math.max(5000,Number(merged.timeoutMs)||30000);
      return Object.freeze(merged);
    }

    constructor(options){
      this.config=options.config;
      this.version=options.version;
      this.getSession=options.getSession;
      this.exportSession=options.exportSession;
      this.logEvent=options.logEvent||(()=>{});
      this.persist=options.persist||(()=>{});
      this.setStatus=options.setStatus||(()=>{});
      this.randomHex=options.randomHex;
      this.hashString=options.hashString;
      this.inFlight=null;
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
      this.logEvent('collection_portal_opened',{session_id:sessionId||null,opened:!!opened,portal_host:new URL(url).host});
      this.persist();
      return !!opened;
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

    postForm(fields){
      return new Promise((resolve,reject)=>{
        const nonce=fields.submission_nonce,frame=document.createElement('iframe'),form=document.createElement('form');
        frame.name='collector_'+nonce;frame.style.display='none';frame.setAttribute('aria-hidden','true');
        form.method='POST';form.action=this.config.endpoint;form.target=frame.name;form.style.display='none';form.acceptCharset='UTF-8';
        for(const [name,value] of Object.entries(fields)){const input=document.createElement('input');input.type='hidden';input.name=name;input.value=String(value??'');form.appendChild(input);}
        let done=false;
        const cleanup=()=>{global.removeEventListener('message',onMessage);clearTimeout(timer);setTimeout(()=>{form.remove();frame.remove();},0);};
        const onMessage=event=>{const d=event.data;if(!d||d.type!=='CUBE_REV_COLLECTOR_ACK'||d.nonce!==nonce)return;done=true;cleanup();if(d.ok)resolve(d);else reject(new Error(d.error||'수집기가 제출을 거부했습니다.'));};
        global.addEventListener('message',onMessage);
        const timer=setTimeout(()=>{if(done)return;cleanup();reject(new Error('자동 제출 응답 시간이 초과되었습니다.'));},this.config.timeoutMs);
        document.body.append(frame,form);form.submit();
      });
    }

    async submit({manual=false}={}){
      const session=this.getSession();
      if(!session)throw new Error('제출할 세션이 없습니다.');
      if(!this.isAutomaticConfigured())throw new Error('자동 제출 수집기가 설정되지 않았습니다.');
      if(this.inFlight)return this.inFlight;
      this.inFlight=(async()=>{
        const startedAt=new Date().toISOString();
        session.data_submission=session.data_submission||{};
        session.data_submission.status='preparing';
        session.data_submission.attempt_count=(session.data_submission.attempt_count||0)+1;
        session.data_submission.last_attempt_at=startedAt;
        session.data_submission.manual=!!manual;
        this.logEvent('submission_attempted',{attempt_count:session.data_submission.attempt_count,study_id:this.config.studyId,manual:!!manual});
        this.persist();this.setStatus('결과 파일을 제출할 준비를 하고 있습니다.','info');
        const jsonText=JSON.stringify(this.exportSession());
        const encoded=await this.encodePayload(jsonText);
        const nonce=this.randomHex(12);
        const checksum=this.hashString(jsonText).toString(16).padStart(8,'0');
        session.data_submission.status='uploading';
        Object.assign(session.data_submission,{encoding:encoded.encoding,original_bytes:encoded.original_bytes,transmitted_bytes:encoded.transmitted_bytes,checksum_fnv1a32:checksum});
        this.setStatus('결과 파일을 자동 제출하고 있습니다.','info');
        try{
          let ack=null,lastTransportError=null;
          const transportLimit=manual?1:2;
          for(let transportAttempt=1;transportAttempt<=transportLimit;transportAttempt++){
            session.data_submission.transport_attempt_count=(session.data_submission.transport_attempt_count||0)+1;
            session.data_submission.last_transport_attempt=transportAttempt;
            try{
              ack=await this.postForm({payload:encoded.payload,encoding:encoded.encoding,study_id:this.config.studyId,study_token:this.config.studyToken,session_id:session.session_id,version:this.version,checksum_fnv1a32:checksum,original_bytes:encoded.original_bytes,submission_nonce:nonce});
              break;
            }catch(error){
              lastTransportError=error;
              if(transportAttempt<transportLimit){
                this.logEvent('submission_retry_scheduled',{transport_attempt:transportAttempt,next_attempt:transportAttempt+1,reason:String(error?.message||error)});
                this.setStatus('응답을 확인하지 못해 한 번 더 제출을 시도합니다.','info');
                await new Promise(resolve=>setTimeout(resolve,1200));
              }
            }
          }
          if(!ack)throw lastTransportError||new Error('수집기 응답을 확인하지 못했습니다.');
          Object.assign(session.data_submission,{status:ack.status||'submitted',received_at:ack.received_at||new Date().toISOString(),receipt_id:ack.receipt_id||null,file_name:ack.file_name||null,last_error:null});
          this.logEvent('submission_succeeded',{status:session.data_submission.status,receipt_id:session.data_submission.receipt_id,file_name:session.data_submission.file_name,submission_method:'automatic'});
          this.persist();
          this.setStatus(ack.status==='duplicate'?'이 세션은 이미 수집되어 있습니다. 추가 작업은 필요하지 않습니다.':`제출이 완료되었습니다. 저장 파일: ${ack.file_name||session.session_id+'.json'}`,'success');
          return ack;
        }catch(error){
          session.data_submission.status='failed';session.data_submission.last_error=String(error?.message||error);
          this.logEvent('submission_failed',{error:session.data_submission.last_error,manual_portal_available:this.isManualPortalConfigured()});
          this.persist();
          this.setStatus(`자동 제출에 실패했습니다. JSON을 저장한 뒤 제출 페이지에서 직접 올려 주세요. (${session.data_submission.last_error})`,'error');
          throw error;
        }finally{this.inFlight=null;}
      })();
      return this.inFlight;
    }
  }

  global.CubeRevCollectorClient=CubeRevCollectorClient;
})(window);
