#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'js'/'collector-client.js'
s=P.read_text(encoding='utf-8')

old="""      this.t=options.translate||((key,vars={})=>String(key).replace(/\\{(\\w+)\\}/g,(_,name)=>vars[name]??''));
      this.inFlight=null;
    }

    isAutomaticConfigured(){"""
new="""      this.t=options.translate||((key,vars={})=>String(key).replace(/\\{(\\w+)\\}/g,(_,name)=>vars[name]??''));
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
      try{
        const raw=this.snapshotStorage.getItem(this.snapshotKey(sessionId));
        if(!raw)return null;
        const x=JSON.parse(raw);
        if(!x||x.schema!=='CUBE_REV_SUBMISSION_SNAPSHOT_V1'||String(x.version)!==String(this.version)||String(x.session_id)!==String(sessionId))return null;
        const text=String(x.text||'');
        const checksum=String(x.checksum_fnv1a32||'').toLowerCase();
        const actual=this.hashString(text).toString(16).padStart(8,'0');
        if(!text||!checksum||checksum!==actual)throw new Error('SUBMISSION_SNAPSHOT_STORAGE_CORRUPT');
        this.submissionSnapshotText=text;this.submissionSnapshotChecksum=checksum;
        return {text,checksum,source:'local_storage'};
      }catch(error){
        if(String(error?.message||error).includes('SUBMISSION_SNAPSHOT_STORAGE_CORRUPT'))throw error;
        return null;
      }
    }

    sealSubmissionSnapshot(){
      const session=this.getSession();
      if(!session||!session.session_id)throw new Error('SUBMISSION_SNAPSHOT_SESSION_MISSING');
      const existing=this.loadSubmissionSnapshot(session.session_id);
      if(existing)return existing;
      const text=JSON.stringify(this.exportSession());
      const checksum=this.hashString(text).toString(16).padStart(8,'0');
      if(!text)throw new Error('SUBMISSION_SNAPSHOT_EMPTY');
      this.submissionSnapshotText=text;this.submissionSnapshotChecksum=checksum;
      if(this.snapshotStorage){
        const envelope={schema:'CUBE_REV_SUBMISSION_SNAPSHOT_V1',version:this.version,session_id:session.session_id,checksum_fnv1a32:checksum,text};
        try{this.snapshotStorage.setItem(this.snapshotKey(session.session_id),JSON.stringify(envelope));}
        catch(error){throw new Error(`SUBMISSION_SNAPSHOT_PERSIST_FAILED: ${String(error?.message||error)}`);}
      }
      return {text,checksum,source:'sealed_now'};
    }

    clearSubmissionSnapshot(sessionId){
      this.submissionSnapshotText=null;this.submissionSnapshotChecksum=null;
      if(this.snapshotStorage){try{this.snapshotStorage.removeItem(this.snapshotKey(sessionId));}catch(_){}}
    }

    isAutomaticConfigured(){"""
if old not in s: sys.exit('constructor anchor missing')
s=s.replace(old,new,1)

anchor="""    checkHealth(){
"""
insert="""    verifyDuplicateStoredBytes(sessionId,expectedChecksum){
      const deadline=Date.now()+Math.min(this.config.timeoutMs,30000);
      return new Promise((resolve,reject)=>{
        let settled=false,activeScript=null,timer=null;
        const finish=(error,payload)=>{
          if(settled)return;settled=true;
          if(timer)clearTimeout(timer);if(activeScript)activeScript.remove();
          if(error)reject(error);else resolve(payload);
        };
        const attempt=()=>{
          if(settled)return;
          if(Date.now()>deadline)return finish(new Error('DUPLICATE_STORED_BYTE_REVERIFICATION_TIMEOUT'));
          const nonce=this.randomHex(12);
          const callbackName=`__cubeRevStoredReverify_${nonce}_${Date.now()}`;
          const script=document.createElement('script');activeScript=script;
          let callbackCalled=false;
          const cleanup=()=>{
            try{delete global[callbackName];}catch(_){global[callbackName]=undefined;}
            script.remove();if(activeScript===script)activeScript=null;
          };
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
          script.async=true;
          script.src=this.receiptUrl(nonce,sessionId,callbackName);
          script.onerror=()=>{cleanup();timer=setTimeout(attempt,this.config.receiptPollIntervalMs);};
          script.onload=()=>{if(!callbackCalled){cleanup();timer=setTimeout(attempt,this.config.receiptPollIntervalMs);}};
          document.head.appendChild(script);
        };
        attempt();
      });
    }

"""
if anchor not in s: sys.exit('health anchor missing')
s=s.replace(anchor,insert+anchor,1)

old="""        let activeScript=null;
        let pollSequence=0;
"""
new="""        let activeScript=null;
        let pollSequence=0;
        let duplicateVerificationInFlight=false;
"""
if old not in s: sys.exit('poll anchor missing')
s=s.replace(old,new,1)

old="""          if(receipt.ok===true&&(receipt.status==='stored'||receipt.status==='duplicate')){
            const expectedChecksum=String(fields.checksum_fnv1a32||'').toLowerCase();
            const receivedChecksum=String(receipt.checksum_fnv1a32||'').toLowerCase();
            if(!receivedChecksum||receivedChecksum!==expectedChecksum){
              finish(new Error('수집기가 저장한 파일의 무결성 확인값이 일치하지 않습니다.'));
              return true;
            }
            finish(null,{...receipt,transport,response_verified:true,checksum_verified:true,received_at:receipt.received_at||new Date().toISOString()});
            return true;
          }
"""
new="""          if(receipt.ok===true&&(receipt.status==='stored'||receipt.status==='duplicate')){
            const expectedChecksum=String(fields.checksum_fnv1a32||'').toLowerCase();
            const receivedChecksum=String(receipt.checksum_fnv1a32||'').toLowerCase();
            if(!receivedChecksum||receivedChecksum!==expectedChecksum){
              finish(new Error('수집기가 저장한 파일의 무결성 확인값이 일치하지 않습니다.'));
              return true;
            }
            if(receipt.status==='duplicate'){
              if(duplicateVerificationInFlight)return true;
              duplicateVerificationInFlight=true;
              this.verifyDuplicateStoredBytes(sessionId,expectedChecksum).then(stored=>{
                finish(null,{...receipt,
                  checksum_fnv1a32:stored.checksum_fnv1a32,
                  transport:`${transport}+fresh_drive_lookup`,
                  response_verified:true,checksum_verified:true,stored_byte_reverified:true,
                  stored_confirmation_source:stored.confirmation_source,
                  stored_lookup_nonce:stored.reverification_nonce,
                  received_at:stored.received_at||receipt.received_at||new Date().toISOString()
                });
              }).catch(error=>finish(error));
              return true;
            }
            finish(null,{...receipt,transport,response_verified:true,checksum_verified:true,stored_byte_reverified:false,received_at:receipt.received_at||new Date().toISOString()});
            return true;
          }
"""
if old not in s: sys.exit('receipt anchor missing')
s=s.replace(old,new,1)

old="""      if(!this.isAutomaticConfigured())throw new Error(this.t('collectorClient.notConfigured'));
      if(this.inFlight)return this.inFlight;

      this.inFlight=(async()=>{
"""
new="""      if(!this.isAutomaticConfigured())throw new Error(this.t('collectorClient.notConfigured'));
      if(this.inFlight)return this.inFlight;
      const sealedSnapshot=this.sealSubmissionSnapshot();

      this.inFlight=(async()=>{
"""
if old not in s: sys.exit('submit start anchor missing')
s=s.replace(old,new,1)

old="""        const jsonText=JSON.stringify(this.exportSession());
        const encoded=await this.encodePayload(jsonText);
        const nonce=this.randomHex(12);
        const checksum=this.hashString(jsonText).toString(16).padStart(8,'0');
"""
new="""        const jsonText=sealedSnapshot.text;
        const encoded=await this.encodePayload(jsonText);
        const nonce=this.randomHex(12);
        const checksum=sealedSnapshot.checksum;
"""
if old not in s: sys.exit('snapshot use anchor missing')
s=s.replace(old,new,1)

old="""            checksum_verified:receipt.checksum_verified===true
          });
"""
new="""            checksum_verified:receipt.checksum_verified===true,
            stored_byte_reverified:receipt.stored_byte_reverified===true,
            submission_snapshot_source:sealedSnapshot.source
          });
"""
if old not in s: sys.exit('success metadata anchor missing')
s=s.replace(old,new,1)

old="""          this.setStatus(message,'success',{pending:false,confirmed:true,receipt_code:session.data_submission.receipt_code});
          return receipt;
"""
new="""          this.setStatus(message,'success',{pending:false,confirmed:true,receipt_code:session.data_submission.receipt_code});
          this.clearSubmissionSnapshot(session.session_id);
          return receipt;
"""
if old not in s: sys.exit('clear snapshot anchor missing')
s=s.replace(old,new,1)

P.write_text(s,encoding='utf-8')
print('CR0105R15_PATCH_APPLIED',P)
