(function () {
  "use strict";

  if (typeof Container === "undefined" || typeof html2canvas !== "function") return;

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var hero = document.querySelector(".hero");
  var snapshot = null;
  var capturing = false;
  var needsFullCapture = false;
  var captureTimer = 0;
  var frame = 0;
  var activeUntil = 0;
  var lastDraw = 0;
  var lastScroll = 0;
  var surfaces = [];

  // Use the upstream shader beneath existing semantic HTML. The adapter owns
  // capture and scheduling instead of starting one snapshot/scroll loop per lens.
  class PageGlass extends Container {
    init() {}
    startRenderLoop() {}

    constructor(element) {
      super({ tintOpacity: element.classList.contains("controls") ? 0.36 : 0.2 });
      this.element = element;
      this.interactiveLens = element.matches(".site-nav, .glass-action");
      this.pointer = [0.5, 0.5];
      this.pointerStrength = 0;
      this.pointerTarget = 0;
      this.canvas = document.createElement("canvas");
      this.canvas.className = "liquid-glass-canvas";
      this.canvas.setAttribute("aria-hidden", "true");
      this.canvas.setAttribute("data-html2canvas-ignore", "true");
      element.prepend(this.canvas);
      this.setupCanvas();
      this.failed = !this.gl;
      this.syncSize();
      this.canvas.addEventListener("webglcontextlost", () => this.fallback());
      element.addEventListener("pointermove", (event) => {
        var rect = element.getBoundingClientRect();
        this.pointer = [(event.clientX - rect.left) / rect.width, (event.clientY - rect.top) / rect.height];
        this.pointerTarget = this.interactiveLens ? 1 : 0;
        requestDraw(true);
      }, { passive: true });
      element.addEventListener("pointerleave", () => { this.pointerTarget = 0; requestDraw(true); });
      element.addEventListener("pointerdown", () => { this.pointerTarget = this.interactiveLens ? 1.6 : 0; requestDraw(true); });
      element.addEventListener("pointerup", () => { this.pointerTarget = 0; requestDraw(true); });
      element.addEventListener("pointercancel", () => { this.pointerTarget = 0; requestDraw(true); });
    }

    syncSize() {
      var width = Math.max(1, this.element.clientWidth);
      var height = Math.max(1, this.element.clientHeight);
      this.borderRadius = Math.min(parseFloat(getComputedStyle(this.element).borderTopLeftRadius) || 0, height / 2);
      if (width !== this.width || height !== this.height) {
        this.width = width;
        this.height = height;
        this.canvas.width = width;
        this.canvas.height = height;
      }
    }

    fallback() {
      this.failed = true;
      this.element.classList.remove("liquid-glass-ready");
    }

    updateTexture() {
      if (this.failed || !snapshot) return;
      try {
        this.syncSize();
        var gl = this.gl;
        if (!this.webglInitialized) {
          this.setupShader(snapshot.canvas);
          this.program = gl.getParameter(gl.CURRENT_PROGRAM);
          if (!this.program || !this.gl_refs.texture) throw new Error("Glass shader initialization failed");
          this.pointerLoc = gl.getUniformLocation(this.program, "u_pointer");
          this.pointerStrengthLoc = gl.getUniformLocation(this.program, "u_pointerStrength");
          this.timeLoc = gl.getUniformLocation(this.program, "u_time");
          this.webglInitialized = true;
        } else {
          gl.bindTexture(gl.TEXTURE_2D, this.gl_refs.texture);
          gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, snapshot.canvas);
        }
        gl.useProgram(this.program);
        // Coordinates remain in CSS pixels even when the shared snapshot is
        // downscaled to fit the GPU texture limit on long/mobile documents.
        gl.uniform2f(this.gl_refs.textureSizeLoc, snapshot.width, snapshot.height);
        this.draw(performance.now());
        this.element.classList.add("liquid-glass-ready");
      } catch (error) {
        this.fallback();
        console.warn("Liquid glass is using the CSS fallback:", error.message);
      }
    }

    draw(now) {
      if (this.failed || !this.webglInitialized || !snapshot || snapshot.width !== document.documentElement.clientWidth) return;
      var rect = this.canvas.getBoundingClientRect();
      if (rect.bottom <= 0 || rect.top >= window.innerHeight) return;
      this.syncSize();
      var gl = this.gl;
      var refs = this.gl_refs;
      var pulse = reducedMotion.matches ? 0 : Math.sin(now * 0.007) * 0.003;
      this.pointerStrength = reducedMotion.matches ? 0 : this.pointerStrength + (this.pointerTarget - this.pointerStrength) * 0.22;
      gl.useProgram(this.program);
      gl.viewport(0, 0, this.width, this.height);
      gl.uniform2f(refs.resolutionLoc, this.width, this.height);
      gl.uniform2f(refs.containerPositionLoc, rect.left + rect.width / 2, rect.top + rect.height / 2);
      gl.uniform1f(refs.scrollYLoc, window.scrollY);
      gl.uniform1f(refs.borderRadiusLoc, this.borderRadius);
      gl.uniform1f(refs.blurRadiusLoc, this.interactiveLens ? 1.0 : 1.6);
      gl.uniform1f(refs.warpLoc, 0);
      gl.uniform1f(refs.edgeIntensityLoc, (this.interactiveLens ? 0.042 : 0.028) + pulse);
      gl.uniform1f(refs.rimIntensityLoc, (this.interactiveLens ? 0.065 : 0.045) + pulse);
      gl.uniform1f(refs.edgeDistanceLoc, 0.12);
      gl.uniform1f(refs.rimDistanceLoc, 0.45);
      gl.uniform1f(refs.cornerBoostLoc, 0.012);
      gl.uniform1f(refs.rippleEffectLoc, 0.025 + pulse);
      gl.uniform1f(refs.tintOpacityLoc, this.tintOpacity);
      gl.uniform2f(this.pointerLoc, this.pointer[0], this.pointer[1]);
      gl.uniform1f(this.pointerStrengthLoc, this.pointerStrength);
      gl.uniform1f(this.timeLoc, reducedMotion.matches ? 0 : now / 1000);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }
  }

  function requestDraw(animate) {
    if (document.hidden) return;
    if (animate && !reducedMotion.matches) activeUntil = performance.now() + 700;
    if (!frame) frame = requestAnimationFrame(draw);
  }

  function draw(now) {
    frame = 0;
    if (document.hidden) return;
    if (now - lastDraw >= 32 || reducedMotion.matches) {
      surfaces.forEach(function (surface) { surface.draw(now); });
      lastDraw = now;
    }
    if (now < activeUntil && !reducedMotion.matches) requestDraw(false);
  }

  function captureOptions(scale) {
    var heroTransform = getComputedStyle(document.querySelector(".hero-photo")).transform;
    return {
      scale: scale,
      useCORS: false,
      allowTaint: false,
      logging: false,
      backgroundColor: "#f8fbfa",
      ignoreElements: function (element) {
        return element.classList.contains("liquid-glass-canvas") || element.id === "hero-webgl" || element.classList.contains("reading-progress");
      },
      onclone: function (clonedDocument) {
        var style = clonedDocument.createElement("style");
        style.textContent = "* { animation: none !important; transition: none !important; }" +
          ".glass-surface { visibility: hidden !important; }" +
          ".motion-reveal, .hero-copy > * { opacity: 1 !important; translate: none !important; }" +
          ".theme-card { transform: none !important; }" +
          ".hero-photo { transform: " + heroTransform + " !important; }";
        clonedDocument.head.appendChild(style);
      }
    };
  }

  function refreshTextures() {
    Container.pageSnapshot = snapshot.canvas;
    surfaces.forEach(function (surface) { surface.updateTexture(); });
    requestDraw(true);
  }

  async function captureFull() {
    if (document.hidden || capturing) return;
    capturing = true;
    needsFullCapture = false;
    var width = document.documentElement.clientWidth;
    var height = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
    var limit = Math.min(8192, ...surfaces.filter(function (s) { return !s.failed; }).map(function (s) { return s.gl.getParameter(s.gl.MAX_TEXTURE_SIZE); }));
    var scale = Math.min(1, limit / width, limit / height, Math.sqrt(6000000 / (width * height)));
    try {
      var options = captureOptions(scale);
      Object.assign(options, { x: 0, y: 0, width: width, height: height });
      var canvas = await html2canvas(document.body, options);
      if (width !== document.documentElement.clientWidth || height !== Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)) {
        needsFullCapture = true;
      } else {
        snapshot = { canvas: canvas, width: width, height: height, scale: scale };
        refreshTextures();
      }
    } catch (error) {
      surfaces.forEach(function (surface) { surface.element.classList.remove("liquid-glass-ready"); });
      console.warn("Background capture failed; CSS glass remains available:", error.message);
    } finally {
      capturing = false;
      if (needsFullCapture) scheduleCapture();
    }
  }

  function scheduleCapture() {
    needsFullCapture = true;
    clearTimeout(captureTimer);
    captureTimer = setTimeout(captureFull, 220);
  }

  // Refresh only the moving hero between full layout snapshots. Scrolling itself
  // samples the shared page texture immediately, without taking a DOM screenshot
  // on every frame or hiding/rebuilding the live navigation.
  async function captureHero() {
    if (!snapshot || capturing || document.hidden || reducedMotion.matches || performance.now() - lastScroll < 400) return;
    var rect = hero.getBoundingClientRect();
    if (rect.bottom <= 0 || rect.top >= window.innerHeight) return;
    capturing = true;
    try {
      var canvas = await html2canvas(hero, captureOptions(snapshot.scale));
      var context = snapshot.canvas.getContext("2d");
      var top = (rect.top + window.scrollY) * snapshot.scale;
      // html2canvas leaves its CSS-to-bitmap scale on the 2D context.
      context.setTransform(1, 0, 0, 1, 0, 0);
      context.clearRect(0, top, canvas.width, canvas.height);
      context.drawImage(canvas, 0, top);
      refreshTextures();
    } catch (error) {
      // The last complete snapshot remains usable if a refresh is interrupted.
    } finally {
      capturing = false;
      if (needsFullCapture) scheduleCapture();
    }
  }

  async function start() {
    document.querySelectorAll(".glass-surface").forEach(function (element) {
      var surface = new PageGlass(element);
      if (!surface.failed) surfaces.push(surface);
    });
    if (!surfaces.length) return;
    if (document.fonts) await document.fonts.ready;
    await captureFull();
    window.addEventListener("scroll", function () {
      lastScroll = performance.now();
      requestDraw(true);
    }, { passive: true });
    window.addEventListener("resize", scheduleCapture);
    document.addEventListener("visibilitychange", function () {
      if (!document.hidden) scheduleCapture();
    });
    document.addEventListener("toggle", scheduleCapture, true);
    reducedMotion.addEventListener("change", function () { activeUntil = 0; scheduleCapture(); });
    new MutationObserver(scheduleCapture).observe(document.querySelector(".papers"), { childList: true });
    if ("ResizeObserver" in window) new ResizeObserver(scheduleCapture).observe(document.body);
    setInterval(captureHero, 1200);
  }

  if (document.readyState === "complete") start();
  else window.addEventListener("load", start, { once: true });
}());
