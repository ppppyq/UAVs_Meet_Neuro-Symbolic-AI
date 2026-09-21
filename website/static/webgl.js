(function () {
  "use strict";

  var canvas = document.getElementById("hero-webgl");
  if (!canvas) {
    return;
  }

  var gl = canvas.getContext("webgl", { alpha: true, antialias: false });
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
    "vec2 hash(vec2 p) {",
    "  p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));",
    "  return fract(sin(p) * 43758.5453123);",
    "}",
    "",
    "float noise(vec2 p) {",
    "  vec2 i = floor(p);",
    "  vec2 f = fract(p);",
    "  vec2 u = f * f * (3.0 - 2.0 * f);",
    "  return mix(mix(dot(hash(i), f), dot(hash(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0)), u.x),",
    "             mix(dot(hash(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0)), dot(hash(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0)), u.x), u.y);",
    "}",
    "",
    "void main() {",
    "  vec2 uv = gl_FragCoord.xy / u_resolution.xy;",
    "  float aspect = u_resolution.x / u_resolution.y;",
    "  vec2 p = vec2(uv.x * aspect, uv.y);",
    "  float t = u_time * 0.18;",
    "",
    "  float n = sin(p.x * 2.4 + t) + cos(p.y * 3.2 - t * 0.8);",
    "  n += sin((p.x + p.y) * 2.1 + t * 1.4) * 0.65;",
    "  n += noise(p * 3.5 + t * 0.45) * 1.7;",
    "",
    "  vec3 deep = vec3(0.06, 0.16, 0.58);",
    "  vec3 bright = vec3(0.62, 0.28, 0.96);",
    "  vec3 col = mix(deep, bright, 0.5 + 0.5 * sin(n * 1.7));",
    "",
    "  vec2 cell = fract(p * 6.0 + t * 0.12) - 0.5;",
    "  float node = smoothstep(0.13, 0.0, length(cell));",
    "  col += vec3(0.55, 0.78, 1.0) * node * 0.95;",
    "",
    "  float pulse = smoothstep(0.035, 0.0, abs(sin((p.x + p.y) * 11.0 - t * 5.2)));",
    "  col += vec3(0.88, 0.95, 1.0) * pulse * 0.28;",
    "",
    "  float vignette = smoothstep(1.35, 0.2, length(uv - 0.5));",
    "  gl_FragColor = vec4(col * vignette, 1.0);",
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
  function render(now) {
    resize();
    gl.useProgram(program);
    gl.uniform2f(resolutionLocation, canvas.width, canvas.height);
    gl.uniform1f(timeLocation, (now - startTime) / 1000);
    gl.enableVertexAttribArray(positionLocation);
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    requestAnimationFrame(render);
  }

  window.addEventListener("resize", resize);
  requestAnimationFrame(render);
}());
