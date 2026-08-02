'use strict';
class CollectorSubmitShadow0807 {
  constructor(o){Object.assign(this,o);this.inFlight=null;}
  async submit({manual=false}={}){
    const session=this.getSession();
    if(!session)throw new Error('NO_SESSION');
    if(!this.isAutomaticConfigured())throw new Error('NOT_CONFIGURED');
    if(this.inFlight)return this.inFlight;
    this.inFlight=(async()=>{
      const startedAt=this.now();
      session.data_submission=session.data_submission||{};
      session.data_submission.status='preparing';
      session.data_submission.receipt_confirmed=false;
      session.data_submission.attempt_count=(session.data_submission.attempt_count||0)+1;
      session.data_submission.last_attempt_at=startedAt;
      session.data_submission.manual=!!manual;
      this.persist();
      session.data_submission.status='checking_collector';
      const health=await this.checkHealth();
      if(String(health.collector_id)!==this.config.collectorId)throw new Error('WRONG_COLLECTOR');
      if(String(health.protocol_version)!==this.config.protocolVersion)throw new Error('PROTOCOL_MISMATCH');
      if(String(health.expected_version)!==this.version)throw new Error('VERSION_MISMATCH');
      session.data_submission.collector_health={checked_at:this.now(),expected_version:health.expected_version,collector_id:health.collector_id,protocol_version:health.protocol_version};
      this.persist();
      const jsonText=JSON.stringify(this.exportSession());
      const nonce=this.randomHex(12);
      const checksum=this.hashString(jsonText).toString(16).padStart(8,'0');
      const encoded=await this.encodePayload(jsonText);
      Object.assign(session.data_submission,{status:'uploading',checksum_fnv1a32:checksum,submission_nonce:nonce,encoding:encoded.encoding,original_bytes:encoded.original_bytes,transmitted_bytes:encoded.transmitted_bytes});
      this.persist();
      try{
        const receipt=await this.postWithConfirmedReceipt({payload:encoded.payload,encoding:encoded.encoding,session_id:session.session_id,version:this.version,checksum_fnv1a32:checksum,submission_nonce:nonce});
        const received=String(receipt.checksum_fnv1a32||'').toLowerCase();
        if(received!==checksum.toLowerCase())throw new Error('CHECKSUM_MISMATCH');
        if(receipt.ok!==true||!['stored','duplicate'].includes(receipt.status))throw new Error(receipt.error||'COLLECTOR_REJECTED');
        Object.assign(session.data_submission,{status:'received',collector_status:receipt.status,receipt_confirmed:true,checksum_verified:true,receipt_code:receipt.receipt_code||null,last_error:null});
        this.persist();
        return receipt;
      }catch(e){
        session.data_submission.status='failed';
        session.data_submission.receipt_confirmed=false;
        session.data_submission.last_error=String(e.message||e);
        this.persist();
        throw e;
      }finally{this.inFlight=null;}
    })();
    return this.inFlight;
  }
}
if(typeof module!=='undefined')module.exports=CollectorSubmitShadow0807;
