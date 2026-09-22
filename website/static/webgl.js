(function () {
  "use strict";

  var canvas = document.getElementById("hero-webgl");
  if (!canvas) {
    return;
  }
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  var gl = canvas.getContext("webgl", { alpha: true, antialias: false, premultipliedAlpha: false });
  if (!gl) {
    canvas.remove();
    return;
  }

  var vertexSource = [
    "attribute vec2 a_position;",
    "void main() {",
    "  gl_Position = vec4(a_position, 0.0, 1.0);",
    "}"
  ].join("\n");

  var fragmentSource = [
    "precision highp float;",
    "uniform vec2 u_resolution;",
    "uniform float u_time;",
    "",
    "void main() {",
    "  vec2 uv = gl_FragCoord.xy / u_resolution.xy;",
    "  float aspect = u_resolution.x / u_resolution.y;",
    "  float t = u_time * 0.28;",
    "  float x = (uv.x - 0.5) * aspect;",
    "  float terrain = uv.y + 0.03 * sin(x * 7.0 + t) + 0.016 * sin(x * 17.0 - t * 0.7);",
    "  float contour = 1.0 - smoothstep(0.0, 0.018, abs(sin(terrain * 46.0)));",
    "  float meridian = 1.0 - smoothstep(0.0, 0.013, abs(sin((x + terrain * 0.13) * 25.0)));",
    "  float fade = smoothstep(0.12, 0.75, uv.y) * (1.0 - smoothstep(0.84, 1.0, uv.y));",
    "  float lines = (contour * 0.38 + meridian * 0.18) * fade;",
    "  gl_FragColor = vec4(vec3(0.12, 0.42, 0.46), lines * 0.45);",
    "}"
  ].join("\n");

  function compile(type, source) {
    var shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      throw new Error(gl.getShaderInfoLog(shader));
    }
    return shader;
  }

  var program = gl.createProgram();
  gl.attachShader(program, compile(gl.VERTEX_SHADER, vertexSource));
  gl.attachShader(program, compile(gl.FRAGMENT_SHADER, fragmentSource));
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    throw new Error(gl.getProgramInfoLog(program));
  }

  var positionLocation = gl.getAttribLocation(program, "a_position");
  var resolutionLocation = gl.getUniformLocation(program, "u_resolution");
  var timeLocation = gl.getUniformLocation(program, "u_time");

  var buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array([-1, -1, 3, -1, -1, 3]),
    gl.STATIC_DRAW
  );

  function resize() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var width = Math.max(1, Math.floor(canvas.clientWidth * dpr));
    var height = Math.max(1, Math.floor(canvas.clientHeight * dpr));
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
      gl.viewport(0, 0, width, height);
    }
  }

  var startTime = performance.now();
  var inView = true;
  var scheduled = false;
  function schedule() {
    if (!scheduled && inView && !document.hidden) {
      scheduled = true;
      requestAnimationFrame(render);
    }
  }

  function render(now) {
    scheduled = false;
    resize();
    gl.useProgram(program);
    gl.uniform2f(resolutionLocation, canvas.width, canvas.height);
    gl.uniform1f(timeLocation, reducedMotion.matches ? 0 : (now - startTime) / 1000);
    gl.enableVertexAttribArray(positionLocation);
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    if (!reducedMotion.matches) {
      schedule();
    }
  }

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      inView = entries[0].isIntersecting;
      if (inView) {
        schedule();
      }
    }).observe(canvas);
  }
  window.addEventListener("resize", schedule);
  document.addEventListener("visibilitychange", schedule);
  reducedMotion.addEventListener("change", schedule);
  schedule();
}());
