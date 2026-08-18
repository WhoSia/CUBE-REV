(function(global){
  'use strict';

  class CubeRevCollectorClient {
    static normalizeConfig(raw,version){
      const defaults={
        enabled:false,
        endpoint:'',
        manualUploadUrl:'',
        studyId:`CUBE-REV-${version}`,
        collectorId:`CUBE-REV-${String(version||'').replaceAll('.','')}-UNBOUND`,
        protocolVersion:'receipt-v2',
        autoSubmitOnComplete:true,
        gzipWhenAvailable:true,
        timeoutMs:90000,
        receiptPollIntervalMs:1500,
        healthCheckTimeoutMs:12000
      };
      const merged={...defaults,...(raw&&typeof raw==='object'?raw:{})};
      merged.enabled=!!merged.enabled;
      merged.endpoint=String(merged.endpoint||'').trim();
      merged.manualUploadUrl=String(merged.manualUploadUrl||merged.endpoint||'').trim();
      merged.studyId=String(merged.studyId||defaults.studyId).trim();
      merged.collectorId=String(merged.collectorId||defaults.collectorId).trim();
      merged.protocolVersion=String(merged.protocolVersion||defaults.protocolVersion).trim();
      merged.autoSubmitOnComplete=merged.autoSubmitOnComplete!==false;
      merged.gzipWhenAvailable=merged.gzipWhenAvailable!==false;
      merged.timeoutMs=Math.max(30000,Number(merged.timeoutMs)||90000);
      merged.receiptPollIntervalMs=Math.max(700,Number(merged.receiptPollIntervalMs)||1500);
      merged.healthCheckTimeoutMs=Math.max(5000,Number(merged.healthCheckTimeoutMs)||12000);
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
      this.t=options.translate||((key,vars={})=>String(key).replace(/\{(\w+)\}/g,(_,name)=>vars[name]??''));
      this.inFlight=null;
      this.submissionSnapshotText=null;
      this.submissionSnapshotChecksum=null;
      this.snapshotStorage=options.snapshotStorage||null;
      if(!this.snapshotStorage){try{this.snapshotStorage=global.localStorage||null;}catch(_){this.snapshotStorage=null;}}
      this.snapshotKeyPrefix=`cube-rev:submission-snapshot:${this.version}:`;
    }

    snapshotKey(sessionId){return this.snapshotKeyPrefix+String(sessionId||'');}

    loadSubmissionSnapshot(sessionId){
      if(this.submissionSnapshotText&&this.submissionSnapshotChecksum){
        return {text:this.submissionSnapshotText,checksum:this.submissionSnapshotChecksum,source:'memory'};
      }
      if(!this.snapshotStorage)return null;
      let raw=null;
      try{raw=this.snapshotStorage.getItem(this.snapshotKey(sessionId));}catch(_){return null;}
      if(!raw)return null;
      let x;
      try{x=JSON.parse(raw);}catch(_){throw new Error('SUBMISSION_SNAPSHOT_STORAGE_CORRUPT');}
      if(!x||x.schema!=='CUBE_REV_SUBMISSION_SNAPSHOT_V1'||String(x.version)!==String(this.version)||String(x.session_id)!==String(sessionId)){
        throw new Error('SUBMISSION_SNAPSHOT_STORAGE_CORRUPT');
      }
      const text=String(x.text||'');
      const checksum=String(x.checksum_fnv1a32||'').toLowerCase();
      const actual=this.hashString(text).toString(16).padStart(8,'0');
      if(!text||!checksum||checksum!==actual)throw new Error('SUBMISSION_SNAPSHOT_STORAGE_CORRUPT');
      this.submissionSnapshotText=text;
      this.submissionSnapshotChecksum=checksum;
      return {text,checksum,source:'local_storage'};
    }

    sealSubmissionSnapshot(){
      const session=this.getSession();
      if(!session||!session.session_id)throw new Error('SUBMISSION_SNAPSHOT_SESSION_MISSING');
      const existing=this.loadSubmissionSnapshot(session.session_id);
      if(existing)return existing;
      if(!this.snapshotStorage)throw new Error('SUBMISSION_SNAPSHOT_PERSIST_UNAVAILABLE');
      const text=JSON.stringify(this.exportSession());
      const checksum=this.hashString(text).toString(16).padStart(8,'0');
      if(!text)throw new Error('SUBMISSION_SNAPSHOT_EMPTY');
      const envelope={
        schema:'CUBE_REV_SUBMISSION_SNAPSHOT_V1',version:this.version,
        session_id:session.session_id,checksum_fnv1a32:checksum,text
      };
      try{
        this.snapshotStorage.setItem(this.snapshotKey(session.session_id),JSON.stringify(envelope));
        const verify=this.snapshotStorage.getItem(this.snapshotKey(session.session_id));
        if(verify!==JSON.stringify(envelope))throw new Error('write verification mismatch');
      }catch(error){
        throw new Error(`SUBMISSION_SNAPSHOT_PERSIST_FAILED: ${String(error?.message||error)}`);
      }
      this.submissionSnapshotText=text;
      this.submissionSnapshotChecksum=checksum;
      return {text,checksum,source:'sealed_now'};
    }

    clearSubmissionSnapshot(sessionId){
      this.submissionSnapshotText=null;
      this.submissionSnapshotChecksum=null;
      if(this.snapshotStorage){try{this.snapshotStorage.removeItem(this.snapshotKey(sessionId));}catch(_){}}
    }

    isAutomaticConfigured(){
      return this.config.enabled&&/^https:\/\/script\.google\.com\/macros\/s\//i.test(this.config.endpoint)&&this.config.endpoint.endsWith('/exec');
    }

    isManualPortalConfigured(){
      return /^https:\/\//i.test(this.config.manualUploadUrl||this.config.endpoint);
    }

    manualPortalUrl(sessionId){
      if(!this.isManualPortalConfigured())return '';
      const url=new URL(this.config.manualUploadUrl||this.config.endpoint);
      url.searchParams.set('source','cube-rev-experiment');
      if(sessionId){
        url.searchParams.set('session_id',sessionId);
        url.searchParams.set('expected_file',sessionId+'.json');
      }
      return url.toString();
    }

    openManualPortal(sessionId){
      const url=this.manualPortalUrl(sessionId);
      if(!url)return false;
      const opened=global.open(url,'_blank','noopener,noreferrer');
      this.logEvent('collection_portal_opened',{session_id:sessionId||null,opened:!!opened,portal_host:new URL(url).host});
      this.persist();
      return !!opened;
    }

    arrayBufferToBase64(buffer){
      const bytes=new Uint8Array(buffer);let out='';const chunk=0x8000;
      for(let i=0;i<bytes.length;i+=chunk){
        out+=String.fromCharCode(...bytes.subarray(i,Math.min(i+chunk,bytes.length)));
      }
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

    createFormField(form,name,value){
      const field=name==='payload'?document.createElement('textarea'):document.createElement('input');
      field.name=name;
      if(field.tagName==='INPUT')field.type='hidden';
      field.value=String(value??'');
      field.hidden=true;
      form.appendChild(field);
    }

    submitFormToHiddenFrame(fields,frameName){
      const form=document.createElement('form');
      form.method='POST';form.action=this.config.endpoint;form.target=frameName;form.acceptCharset='UTF-8';form.style.display='none';
      for(const [name,value] of Object.entries(fields))this.createFormField(form,name,value);
      document.body.appendChild(form);form.submit();setTimeout(()=>form.remove(),0);
    }

    receiptUrl(nonce,sessionId,callbackName){
      const url=new URL(this.config.endpoint);
      url.searchParams.set('action','receipt');url.searchParams.set('submission_nonce',nonce);url.searchParams.set('session_id',sessionId);
      url.searchParams.set('collector_id',this.config.collectorId);url.searchParams.set('protocol_version',this.config.protocolVersion);
      url.searchParams.set('version',this.version);url.searchParams.set('callback',callbackName);url.searchParams.set('_',String(Date.now()));
      return url.toString();
    }

    healthUrl(callbackName){
      const url=new URL(this.config.endpoint);
      url.searchParams.set('action','health');url.searchParams.set('collector_id',this.config.collectorId);
      url.searchParams.set('protocol_version',this.config.protocolVersion);url.searchParams.set('version',this.version);
      url.searchParams.set('callback',callbackName);url.searchParams.set('_',String(Date.now()));
      return url.toString();
    }

    checkHealth(){
      return new Promise((resolve,reject)=>{
        const callbackName=`__cubeRevHealth_${this.randomHex(8)}`;
        const script=document.createElement('script');let settled=false;
        const cleanup=()=>{clearTimeout(timer);try{delete global[callbackName];}catch(_){global[callbackName]=undefined;}script.remove();};
        const finish=(error,payload)=>{if(settled)return;settled=true;cleanup();if(error)reject(error);else resolve(payload);};
        const timer=setTimeout(()=>finish(new Error(this.t('collectorClient.healthTimeout'))),this.config.healthCheckTimeoutMs);
        global[callbackName]=(payload)=>{
          if(!payload||payload.ok!==true)return finish(new Error(payload?.error||this.t('collectorClient.healthFailed')));
          if(String(payload.collector_id||'')!==this.config.collectorId)return finish(new Error(this.t('collectorClient.wrongCollector')));
          if(String(payload.protocol_version||'')!==this.config.protocolVersion)return finish(new Error(this.t('collectorClient.protocolMismatch')));
          if(String(payload.expected_version||'')!==this.version)return finish(new Error(this.t('collectorClient.versionMismatch')));
          finish(null,payload);
        };
        script.async=true;script.src=this.healthUrl(callbackName);script.onerror=()=>finish(new Error(this.t('collectorClient.healthLoadFailed')));document.head.appendChild(script);
      });
    }

    verifyDuplicateStoredBytes(sessionId,expectedChecksum){
      const deadline=Date.now()+Math.min(this.config.timeoutMs,30000);
      return new Promise((resolve,reject)=>{
        let settled=false,activeScript=null,timer=null;
        const finish=(error,payload)=>{
          if(settled)return;settled=true;if(timer)clearTimeout(timer);if(activeScript)activeScript.remove();
          if(error)reject(error);else resolve(payload);
        };
        const attempt=()=>{
          if(settled)return;
          if(Date.now()>deadline)return finish(new Error('DUPLICATE_STORED_BYTE_REVERIFICATION_TIMEOUT'));
          const nonce=this.randomHex(12);
          const callbackName=`__cubeRevStoredReverify_${nonce}_${Date.now()}`;
          const script=document.createElement('script');activeScript=script;let callbackCalled=false;
          const cleanup=()=>{try{delete global[callbackName];}catch(_){global[callbackName]=undefined;}script.remove();if(activeScript===script)activeScript=null;};
          global[callbackName]=(payload)=>{
            callbackCalled=true;cleanup();
            if(!payload||String(payload.submission_nonce||'')!==nonce||String(payload.session_id||'')!==String(sessionId)){
              timer=setTimeout(attempt,this.config.receiptPollIntervalMs);return;
            }
            if(payload.ok===false||payload.status==='error')return finish(new Error(payload.error||'DUPLICATE_STORED_BYTE_REVERIFICATION_REJECTED'));
            if(payload.ok===true&&payload.status==='stored'&&String(payload.confirmation_source||'')==='drive_lookup'){
              const actual=String(payload.checksum_fnv1a32||'').toLowerCase();
              if(!actual||actual!==String(expectedChecksum||'').toLowerCase())return finish(new Error('DUPLICATE_STORED_BYTE_CHECKSUM_MISMATCH'));
              return finish(null,{...payload,stored_byte_reverified:true,reverification_nonce:nonce});
            }
            timer=setTimeout(attempt,this.config.receiptPollIntervalMs);
          };
          script.async=true;script.src=this.receiptUrl(nonce,sessionId,callbackName);
          script.onerror=()=>{cleanup();timer=setTimeout(attempt,this.config.receiptPollIntervalMs);};
          script.onload=()=>{if(!callbackCalled){cleanup();timer=setTimeout(attempt,this.config.receiptPollIntervalMs);}};
          document.head.appendChild(script);
        };
        attempt();
      });
    }

    postWithConfirmedReceipt(fields){
      const nonce=String(fields.submission_nonce||'');
      const sessionId=String(fields.session_id||'');
      if(!nonce||!sessionId)return Promise.reject(new Error('제출 확인 식별자를 만들지 못했습니다.'));
      return new Promise((resolve,reject)=>{
        const frameName=`cubeRevReceiptFrame_${nonce}`;
        const iframe=document.createElement('iframe');iframe.name=frameName;iframe.hidden=true;iframe.setAttribute('aria-hidden','true');iframe.style.display='none';
        let settled=false,pollTimer=null,timeoutTimer=null,activeScript=null,pollSequence=0,duplicateVerificationInFlight=false;
        const cleanup=()=>{global.removeEventListener('message',onMessage);if(pollTimer)clearTimeout(pollTimer);if(timeoutTimer)clearTimeout(timeoutTimer);if(activeScript)activeScript.remove();iframe.remove();};
        const finish=(error,receipt)=>{if(settled)return;settled=true;cleanup();if(error)reject(error);else resolve(receipt);};
        const normalizeReceipt=(raw)=>{
          if(!raw||typeof raw!=='object')return null;
          if(String(raw.submission_nonce||raw.nonce||'')!==nonce)return null;
          if(String(raw.session_id||'')!==sessionId)return null;
          return raw;
        };
        const handleReceipt=(raw,transport)=>{
          const receipt=normalizeReceipt(raw);if(!receipt)return false;if(receipt.status==='pending')return true;
          if(receipt.ok===true&&(receipt.status==='stored'||receipt.status==='duplicate')){
            const expectedChecksum=String(fields.checksum_fnv1a32||'').toLowerCase();
            const receivedChecksum=String(receipt.checksum_fnv1a32||'').toLowerCase();
            if(!receivedChecksum||receivedChecksum!==expectedChecksum){finish(new Error('수집기가 저장한 파일의 무결성 확인값이 일치하지 않습니다.'));return true;}
            if(receipt.status==='duplicate'){
              if(duplicateVerificationInFlight)return true;
              duplicateVerificationInFlight=true;
              this.verifyDuplicateStoredBytes(sessionId,expectedChecksum).then(stored=>{
                finish(null,{...receipt,checksum_fnv1a32:stored.checksum_fnv1a32,transport:`${transport}+fresh_drive_lookup`,response_verified:true,checksum_verified:true,stored_byte_reverified:true,stored_confirmation_source:stored.confirmation_source,stored_lookup_nonce:stored.reverification_nonce,received_at:stored.received_at||receipt.received_at||new Date().toISOString()});
              }).catch(error=>finish(error));
              return true;
            }
            finish(null,{...receipt,transport,response_verified:true,checksum_verified:true,stored_byte_reverified:false,received_at:receipt.received_at||new Date().toISOString()});return true;
          }
          if(receipt.ok===false||receipt.status==='error'){finish(new Error(receipt.error||'수집기가 결과 저장을 거부했습니다.'));return true;}
          return false;
        };
        const onMessage=(event)=>{const data=event&&event.data;if(!data||data.type!=='CUBE_REV_COLLECTOR_ACK')return;handleReceipt(data,'iframe_postmessage');};
        const schedulePoll=(delay=this.config.receiptPollIntervalMs)=>{if(settled)return;pollTimer=setTimeout(pollReceipt,delay);};
        const pollReceipt=()=>{
          if(settled)return;pollSequence+=1;
          const callbackName=`__cubeRevReceipt_${nonce}_${pollSequence}`;
          const script=document.createElement('script');activeScript=script;let callbackCalled=false;
          const clearCallback=()=>{try{delete global[callbackName];}catch(_){global[callbackName]=undefined;}script.remove();if(activeScript===script)activeScript=null;};
          global[callbackName]=(payload)=>{callbackCalled=true;clearCallback();const handled=handleReceipt(payload,'jsonp_receipt_poll');if(!settled&&(handled||payload?.status==='pending'))schedulePoll();else if(!settled)schedulePoll();};
          script.async=true;script.src=this.receiptUrl(nonce,sessionId,callbackName);
          script.onerror=()=>{clearCallback();if(!settled)schedulePoll();};
          script.onload=()=>{if(!callbackCalled){clearCallback();if(!settled)schedulePoll();}};
          document.head.appendChild(script);
        };
        global.addEventListener('message',onMessage);document.body.appendChild(iframe);
        timeoutTimer=setTimeout(()=>finish(new Error(this.t('collectorClient.receiptTimeout'))),this.config.timeoutMs);
        try{this.submitFormToHiddenFrame(fields,frameName);schedulePoll(1200);}catch(error){finish(error);}
      });
    }

    async submit({manual=false}={}){
      const session=this.getSession();
      if(!session)throw new Error(this.t('collectorClient.noSession'));
      if(!this.isAutomaticConfigured())throw new Error(this.t('collectorClient.notConfigured'));
      if(this.inFlight)return this.inFlight;
      const sealedSnapshot=this.sealSubmissionSnapshot();

      this.inFlight=(async()=>{
        const startedAt=new Date().toISOString();
        session.data_submission=session.data_submission||{};
        session.data_submission.status='preparing';session.data_submission.receipt_confirmed=false;
        session.data_submission.attempt_count=(session.data_submission.attempt_count||0)+1;
        session.data_submission.last_attempt_at=startedAt;session.data_submission.manual=!!manual;
        this.logEvent('submission_attempted',{attempt_count:session.data_submission.attempt_count,study_id:this.config.studyId,manual:!!manual,confirmation_protocol:'post_then_receipt_v2'});
        this.persist();session.data_submission.status='checking_collector';this.setStatus(this.t('collectorClient.checking'),'info',{pending:true});
        const health=await this.checkHealth();
        session.data_submission.collector_health={checked_at:new Date().toISOString(),expected_version:health.expected_version,receipt_confirmation_available:health.receipt_confirmation_available===true,deployment_id:health.deployment_id||null,collector_id:health.collector_id||null,protocol_version:health.protocol_version||null};
        this.logEvent('collector_health_confirmed',session.data_submission.collector_health);this.persist();this.setStatus(this.t('collectorClient.preparingFile'),'info',{pending:true});

        const jsonText=sealedSnapshot.text;
        const encoded=await this.encodePayload(jsonText);
        const nonce=this.randomHex(12);
        const checksum=sealedSnapshot.checksum;
        session.data_submission.status='uploading';
        Object.assign(session.data_submission,{encoding:encoded.encoding,original_bytes:encoded.original_bytes,transmitted_bytes:encoded.transmitted_bytes,checksum_fnv1a32:checksum,submission_nonce:nonce,confirmation_protocol:'post_then_jsonp_receipt_v2',submission_snapshot_source:sealedSnapshot.source});
        this.persist();this.setStatus(this.t('collectorClient.sending'),'info',{pending:true});

        try{
          const receipt=await this.postWithConfirmedReceipt({payload:encoded.payload,encoding:encoded.encoding,study_id:this.config.studyId,collector_id:this.config.collectorId,protocol_version:this.config.protocolVersion,session_id:session.session_id,version:this.version,checksum_fnv1a32:checksum,original_bytes:encoded.original_bytes,submission_nonce:nonce});
          const collectorStatus=receipt.status;
          Object.assign(session.data_submission,{status:'received',collector_status:collectorStatus,receipt_confirmed:true,received_at:receipt.received_at,receipt_code:receipt.receipt_code||null,file_name:receipt.file_name||session.session_id+'.json',last_error:null,transport:receipt.transport,response_verification:'collector_receipt',checksum_verified:receipt.checksum_verified===true,stored_byte_reverified:receipt.stored_byte_reverified===true,submission_snapshot_source:sealedSnapshot.source});
          this.logEvent('submission_receipt_confirmed',{collector_status:collectorStatus,file_name:session.data_submission.file_name,receipt_code:session.data_submission.receipt_code,submission_method:manual?'manual_retry':'automatic',transport:receipt.transport,response_verified:true,checksum_verified:receipt.checksum_verified===true,stored_byte_reverified:receipt.stored_byte_reverified===true});
          this.persist();
          const message=collectorStatus==='duplicate'?this.t('collectorClient.receivedDuplicate'):this.t('collectorClient.receivedStored',{file:session.data_submission.file_name});
          this.setStatus(message,'success',{pending:false,confirmed:true,receipt_code:session.data_submission.receipt_code});
          this.clearSubmissionSnapshot(session.session_id);
          return receipt;
        }catch(error){
          session.data_submission.status='failed';session.data_submission.receipt_confirmed=false;session.data_submission.last_error=String(error?.message||error);
          this.logEvent('submission_failed',{error:session.data_submission.last_error,manual_portal_available:this.isManualPortalConfigured(),receipt_confirmed:false});
          this.persist();this.setStatus(this.t('collectorClient.failed',{error:session.data_submission.last_error}),'error',{pending:false,failed:true});
          throw error;
        }finally{this.inFlight=null;}
      })();
      return this.inFlight;
    }
  }

  CubeRevCollectorClient.R15_RECEIPT_RACE_CLOSURE='0.10.5-R1.5';
  global.CubeRevCollectorClient=CubeRevCollectorClient;
})(window);
