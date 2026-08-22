(function(root,factory){
  const api=factory();
  if(typeof module==="object"&&module.exports)module.exports=api;
  root.CubeRevNaturalisticTelemetry0105R1=api;
})(typeof globalThis!=="undefined"?globalThis:this,function(){
  "use strict";
  const TELEMETRY_VERSION="CR0105R1-NATURALISTIC-TELEMETRY-1";
  const CAMERA_MODEL_VERSION="CR0105-CAMERA-STATE-1";
  function finite(v){return Number.isFinite(Number(v));}
  function matrix(camera,orbit){
    if(orbit&&typeof orbit.matrixForCamera==="function")return orbit.matrixForCamera(camera||{});
    const m=camera&&camera.view_matrix;
    return Array.isArray(m)&&m.length===9?m.slice():null;
  }
  function cameraSnapshot(camera,orbit,inputSource){
    camera=camera||{};
    return {yaw:finite(camera.yaw)?Number(camera.yaw):0,pitch:finite(camera.pitch)?Number(camera.pitch):0,
      zoom:finite(camera.zoom)?Number(camera.zoom):1,view_matrix:matrix(camera,orbit),
      orbit_model:camera.orbit_model||"screen_relative_matrix_v1",input_source:inputSource||"camera_control",
      camera_model_version:CAMERA_MODEL_VERSION};
  }
  function defaultSource(type,payload){
    if(payload&&payload.source)return String(payload.source);
    if(type.startsWith("camera_drag"))return "pointer_camera_drag";
    if(type.startsWith("camera_zoom"))return "camera_zoom_control";
    if(type==="camera_reset")return "camera_reset_control";
    return "camera_control";
  }
  function decorateCameraPayload(type,payload,getCamera,orbit){
    const p=Object.assign({},payload||{});
    if(!String(type).startsWith("camera_"))return p;
    const snap=cameraSnapshot(typeof getCamera==="function"?getCamera():{},orbit,defaultSource(type,p));
    for(const [k,v] of Object.entries(snap)){if(p[k]===undefined||p[k]===null)p[k]=v;}
    p.camera_state=Object.assign({},snap);
    p.telemetry_version=TELEMETRY_VERSION;
    return p;
  }
  function wrapLogEvent(baseLogEvent,getCamera,orbit){
    if(typeof baseLogEvent!=="function")throw new Error("baseLogEvent required");
    return function(type,payload){return baseLogEvent(type,decorateCameraPayload(type,payload,getCamera,orbit));};
  }
  function prospectiveCameraComplete(payload){return payload&&finite(payload.yaw)&&finite(payload.pitch)&&finite(payload.zoom)&&Array.isArray(payload.view_matrix)&&payload.view_matrix.length===9&&payload.input_source&&payload.camera_model_version===CAMERA_MODEL_VERSION;}
  return {TELEMETRY_VERSION,CAMERA_MODEL_VERSION,cameraSnapshot,decorateCameraPayload,wrapLogEvent,prospectiveCameraComplete};
});
