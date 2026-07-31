(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CubeRevCameraOrbit = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const IDENTITY = Object.freeze([1, 0, 0, 0, 1, 0, 0, 0, 1]);

  function multiply(a, b) {
    const out = new Array(9);
    for (let row = 0; row < 3; row++) {
      for (let col = 0; col < 3; col++) {
        out[row * 3 + col] =
          a[row * 3] * b[col] +
          a[row * 3 + 1] * b[col + 3] +
          a[row * 3 + 2] * b[col + 6];
      }
    }
    return out;
  }

  function rotationX(angle) {
    const c = Math.cos(angle), s = Math.sin(angle);
    return [1, 0, 0, 0, c, -s, 0, s, c];
  }

  function rotationY(angle) {
    const c = Math.cos(angle), s = Math.sin(angle);
    return [c, 0, s, 0, 1, 0, -s, 0, c];
  }

  function fromEuler(yaw = 0, pitch = 0) {
    return multiply(rotationX(pitch), rotationY(yaw));
  }

  function apply(matrix, point) {
    return [
      matrix[0] * point[0] + matrix[1] * point[1] + matrix[2] * point[2],
      matrix[3] * point[0] + matrix[4] * point[1] + matrix[5] * point[2],
      matrix[6] * point[0] + matrix[7] * point[1] + matrix[8] * point[2]
    ];
  }

  function matrixForCamera(camera = {}) {
    if (Array.isArray(camera.view_matrix) && camera.view_matrix.length === 9 &&
        camera.view_matrix.every(Number.isFinite)) {
      return camera.view_matrix.slice();
    }
    return fromEuler(Number(camera.yaw) || 0, Number(camera.pitch) || 0);
  }

  function screenRelativeOrbit(camera, dx, dy, sensitivity) {
    const start = matrixForCamera(camera);
    // Pre-multiplication makes both axes camera/screen-relative. Horizontal
    // drag is always about screen-up and vertical drag is always about
    // screen-right, even after the view crosses 180 degrees.
    const delta = multiply(
      rotationX(dy * sensitivity),
      rotationY(dx * sensitivity)
    );
    return {
      yaw: (Number(camera.yaw) || 0) + dx * sensitivity,
      pitch: (Number(camera.pitch) || 0) + dy * sensitivity,
      zoom: Number(camera.zoom) || 1,
      view_matrix: multiply(delta, start),
      orbit_model: "screen_relative_matrix_v1"
    };
  }

  function resetCamera(zoom = 1) {
    return {
      yaw: 0,
      pitch: 0,
      zoom,
      view_matrix: IDENTITY.slice(),
      orbit_model: "screen_relative_matrix_v1"
    };
  }

  return {
    IDENTITY,
    multiply,
    rotationX,
    rotationY,
    fromEuler,
    apply,
    matrixForCamera,
    screenRelativeOrbit,
    resetCamera
  };
});
