/* Aura's original silhouette, lit as one continuous piece of satin metal.
 * No dependencies, geometric deformation, image downloads or animated filters.
 * The SVG underneath is the permanent, accessible fallback.
 */
(() => {
  'use strict';

  const LOGO_WIDTH = 1789.33;
  const LOGO_HEIGHT = 925.59;
  const LOGO_PATH = 'M0,925.59h923.43l306.37-306.37h105.11c15.83,0,28.65,12.83,28.65,28.65v277.72h270.77v-308.53l-241.89,1.93c-15.91.13-28.88-12.74-28.88-28.65V0h-387.05c-33.3,0-65.23,13.24-88.76,36.8L0,925.59Z';
  const DISTANCE_RANGE = 40;

  function start() {
    const canvas = document.getElementById('aura-canvas');
    if (!canvas || typeof Path2D === 'undefined') return;

    const sculpture = canvas.closest('.sculpture') || canvas.parentElement;
    const toggle = document.getElementById('motion-toggle');
    const label = document.getElementById('motion-label');
    const replay = document.getElementById('motion-replay');
    const controls = document.querySelector('.motion-controls');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const coarsePointer = window.matchMedia('(pointer: coarse)');

    let gl;
    let resources;
    let mask;
    let raf = null;
    let lastTick = null;
    let lastPaint = -Infinity;
    let elapsed = 0;
    let paused = false;
    let lost = false;
    let failed = false;
    let revealed = false;
    let pageHidden = false;
    let resizeNeeded = true;
    const pointer = { x: 0, y: 0, targetX: 0, targetY: 0 };

    canvas.style.opacity = '0';
    canvas.setAttribute('aria-hidden', 'true');

    function canAnimate() {
      return !paused && !reducedMotion.matches && !document.hidden &&
        !pageHidden && !lost && !failed;
    }

    function updateControls() {
      const staticMode = failed || lost;
      if (controls) controls.hidden = !revealed || staticMode || reducedMotion.matches;
      if (toggle) {
        toggle.disabled = reducedMotion.matches || staticMode;
        toggle.dataset.paused = String(paused || reducedMotion.matches || staticMode);
        toggle.setAttribute('aria-label', failed ? 'Modo estático / Static mode' :
          lost ? 'Restaurando animação / Restoring animation' :
          reducedMotion.matches ? 'Movimento reduzido / Reduced motion' :
          paused ? 'Retomar animação / Resume animation' : 'Pausar animação / Pause animation');
      }
      if (label) {
        label.textContent = failed ? 'Modo estático' : lost ? 'Restaurando animação' :
          reducedMotion.matches ? 'Movimento reduzido' : paused ? 'Retomar animação' : 'Pausar animação';
      }
      if (replay) replay.disabled = reducedMotion.matches || staticMode;
    }

    function stop() {
      if (raf !== null) cancelAnimationFrame(raf);
      raf = null;
      lastTick = null;
    }

    function requestPaint() {
      if (raf === null && !failed && !lost && !document.hidden && !pageHidden) {
        raf = requestAnimationFrame(frame);
      }
    }

    function useFallback(error) {
      failed = true;
      stop();
      canvas.style.opacity = '0';
      canvas.classList.remove('is-ready');
      canvas.dataset.ready = 'false';
      updateControls();
      if (error) console.warn('Aura motion: using the static SVG fallback.', error);
    }

    /* A padded, antialiased mask preserves the source path exactly. A chamfer
     * distance transform is computed once; the GPU uses it for rounded bevels.
     * Two texture channels store distance at 16-bit precision, avoiding bands.
     */
    function createMask() {
      const width = 1024;
      const height = Math.round(width * LOGO_HEIGHT / LOGO_WIDTH);
      const pad = 24;
      const textureWidth = width + pad * 2;
      const textureHeight = height + pad * 2;
      const source = document.createElement('canvas');
      source.width = textureWidth;
      source.height = textureHeight;
      const ctx = source.getContext('2d', { willReadFrequently: true });
      if (!ctx) throw new Error('Canvas mask is unavailable.');
      ctx.translate(pad, pad);
      ctx.scale(width / LOGO_WIDTH, height / LOGO_HEIGHT);
      ctx.fillStyle = '#fff';
      ctx.fill(new Path2D(LOGO_PATH));

      const pixels = ctx.getImageData(0, 0, textureWidth, textureHeight).data;
      const count = textureWidth * textureHeight;
      const inside = new Uint8Array(count);
      const distances = new Float32Array(count);
      for (let i = 0; i < count; i++) inside[i] = pixels[i * 4 + 3] >= 128 ? 1 : 0;
      distances.fill(10000);

      // Seed both sides of the boundary at half a texel from the vector edge.
      for (let y = 1; y < textureHeight - 1; y++) {
        const row = y * textureWidth;
        for (let x = 1; x < textureWidth - 1; x++) {
          const i = row + x;
          const bit = inside[i];
          if (bit !== inside[i - 1] || bit !== inside[i + 1] ||
              bit !== inside[i - textureWidth] || bit !== inside[i + textureWidth]) {
            distances[i] = 0.5;
          }
        }
      }

      const diagonal = Math.SQRT2;
      for (let y = 1; y < textureHeight - 1; y++) {
        const row = y * textureWidth;
        for (let x = 1; x < textureWidth - 1; x++) {
          const i = row + x;
          distances[i] = Math.min(distances[i], distances[i - 1] + 1,
            distances[i - textureWidth] + 1,
            distances[i - textureWidth - 1] + diagonal,
            distances[i - textureWidth + 1] + diagonal);
        }
      }
      for (let y = textureHeight - 2; y > 0; y--) {
        const row = y * textureWidth;
        for (let x = textureWidth - 2; x > 0; x--) {
          const i = row + x;
          distances[i] = Math.min(distances[i], distances[i + 1] + 1,
            distances[i + textureWidth] + 1,
            distances[i + textureWidth - 1] + diagonal,
            distances[i + textureWidth + 1] + diagonal);
        }
      }

      const data = new Uint8Array(count * 4);
      for (let i = 0; i < count; i++) {
        const signed = Math.min(DISTANCE_RANGE, distances[i]) * (inside[i] ? 1 : -1);
        const encoded = Math.round((signed / DISTANCE_RANGE * 0.5 + 0.5) * 65535);
        data[i * 4] = encoded >>> 8;
        data[i * 4 + 1] = encoded & 255;
        data[i * 4 + 2] = pixels[i * 4 + 3];
        data[i * 4 + 3] = 255;
      }
      return { data, width: textureWidth, height: textureHeight,
        scale: [width / textureWidth, height / textureHeight],
        offset: [pad / textureWidth, pad / textureHeight] };
    }

    const vertexSource = `
      attribute vec2 aPosition;
      varying vec2 vUv;
      void main() {
        vUv = aPosition * 0.5 + 0.5;
        gl_Position = vec4(aPosition, 0.0, 1.0);
      }
    `;

    function fragmentSource(precision) {
      return `
        precision ${precision} float;
        varying vec2 vUv;
        uniform sampler2D uMask;
        uniform vec2 uTexel;
        uniform vec2 uMaskScale;
        uniform vec2 uMaskOffset;
        uniform vec2 uPointer;
        uniform float uTime;
        uniform float uIntro;

        float distanceAt(vec2 uv) {
          vec2 value = texture2D(uMask, uv).rg;
          return (dot(value, vec2(256.0 / 257.0, 1.0 / 257.0)) * 2.0 - 1.0) * 40.0;
        }

        float gaussian(float value) { return exp(-value * value); }

        float panel(vec2 ray, vec2 center, vec2 size) {
          vec2 local = (ray - center) / size;
          return exp(-dot(local, local) * 1.45);
        }

        // Broad anisotropic studio reflections suggest a brushed finish without
        // grain, glitter, repeated stripes, or pixel-level animated noise.
        vec3 studio(vec3 ray, vec2 lightShift) {
          vec2 p = ray.xy + lightShift;
          vec3 light = vec3(0.043, 0.047, 0.052);
          light += vec3(0.94, 0.965, 1.0) *
            panel(p, vec2(-0.23, 0.26), vec2(0.35, 0.79)) * 1.62;
          float negativeFill = gaussian((p.x + p.y * 0.58 - 0.065) / 0.082);
          light *= 1.0 - negativeFill * 0.76;
          float ribbon = gaussian((p.x + p.y * 0.36 + 0.055) / 0.039);
          light += vec3(0.97, 0.975, 0.98) * ribbon * 1.34;
          light += vec3(1.0, 0.97, 0.92) *
            panel(p, vec2(0.73, 0.10), vec2(0.115, 0.85)) * 2.6;
          light += vec3(0.83, 0.89, 1.0) *
            panel(p, vec2(-0.13, -0.79), vec2(0.85, 0.14)) * 1.25;
          return light;
        }

        void main() {
          vec2 uv = vUv * uMaskScale + uMaskOffset;
          float coverage = texture2D(uMask, uv).b;
          if (coverage < 0.002) discard;

          float distance = distanceAt(uv);
          vec2 stepSize = uTexel * 1.5;
          vec2 gradient = vec2(
            distanceAt(uv + vec2(stepSize.x, 0.0)) - distanceAt(uv - vec2(stepSize.x, 0.0)),
            distanceAt(uv + vec2(0.0, stepSize.y)) - distanceAt(uv - vec2(0.0, stepSize.y))
          );
          gradient /= max(length(gradient), 0.0001);

          float bevel = clamp(1.0 - max(distance, 0.0) / 5.1, 0.0, 1.0);
          vec2 curvature = vec2((vUv.x - 0.47) * 0.20, (vUv.y - 0.51) * 0.15);
          curvature += vec2(sin(vUv.y * 4.2) * 0.028, sin(vUv.x * 4.7) * 0.018);
          vec3 normal = normalize(vec3(curvature - gradient * bevel,
            max(0.11, sqrt(max(0.0, 1.0 - bevel * bevel)))));
          vec3 view = normalize(vec3((vUv - 0.5) * vec2(0.13, 0.075), 1.6));
          vec3 reflection = reflect(-view, normal);

          float phase = uTime * 0.3926990817; // One quiet light cycle every 16 s.
          vec2 lightShift = vec2(sin(phase) * 0.16, (cos(phase) - 1.0) * 0.05);
          lightShift += uPointer * vec2(0.055, 0.042);
          vec3 radiance = studio(reflection, lightShift);
          float facing = max(dot(normal, view), 0.0);
          vec3 fresnel = mix(vec3(0.86, 0.89, 0.925), vec3(1.0), pow(1.0 - facing, 5.0));
          radiance *= fresnel * (0.84 + facing * 0.16);

          // A reflected strip light travels across the large, calm top surface.
          // Its dark neighboring flag makes the metal read as a studio object.
          float satinCoordinate = vUv.x * 0.91 + vUv.y * 0.53;
          float satinCenter = 0.71 + sin(phase - 0.72) * 0.65;
          float satin = gaussian((satinCoordinate - satinCenter) / 0.088);
          float satinFlag = gaussian((satinCoordinate - satinCenter - 0.17) / 0.14);
          radiance *= 1.0 - satinFlag * 0.38;
          radiance += vec3(0.97, 0.985, 1.0) * satin * 1.85 * (0.5 + facing * 0.5);

          // The piece stays whole throughout the reveal. Only illumination moves.
          float entrance = smoothstep(0.025, 0.82, uIntro);
          radiance *= mix(0.20, 1.0, entrance);
          float sweepProgress = uIntro * uIntro * (3.0 - 2.0 * uIntro);
          float sweepPosition = mix(-0.36, 1.82, sweepProgress);
          float diagonal = vUv.x * 0.98 + vUv.y * 0.53;
          float envelope = smoothstep(0.02, 0.17, uIntro) * (1.0 - smoothstep(0.81, 1.0, uIntro));
          float sweep = gaussian((diagonal - sweepPosition) / 0.075);
          float wash = gaussian((diagonal - sweepPosition + 0.11) / 0.30);
          radiance += vec3(0.90, 0.94, 1.0) * (sweep * 1.3 + wash * 0.17) * envelope;

          // Soft photographic roll-off retains highlights against the pale UI.
          vec3 color = radiance / (radiance + vec3(0.76));
          color = pow(max(color, vec3(0.0)), vec3(1.0 / 2.2));
          gl_FragColor = vec4(color, coverage);
        }
      `;
    }

    function compile(type, source) {
      const shader = gl.createShader(type);
      if (!shader) throw new Error('Unable to allocate an Aura shader.');
      gl.shaderSource(shader, source);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        const message = gl.getShaderInfoLog(shader);
        gl.deleteShader(shader);
        throw new Error(message || 'Aura shader compilation failed.');
      }
      return shader;
    }

    function initializeGL() {
      gl = canvas.getContext('webgl', {
        alpha: true, antialias: true, depth: false, stencil: false,
        premultipliedAlpha: false, preserveDrawingBuffer: false,
        powerPreference: 'low-power'
      });
      if (!gl) throw new Error('WebGL is unavailable.');
      if (!mask) mask = createMask();

      const precision = gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.HIGH_FLOAT);
      const vertex = compile(gl.VERTEX_SHADER, vertexSource);
      const fragment = compile(gl.FRAGMENT_SHADER, fragmentSource(precision && precision.precision ? 'highp' : 'mediump'));
      const program = gl.createProgram();
      if (!program) throw new Error('Unable to allocate the Aura program.');
      gl.attachShader(program, vertex);
      gl.attachShader(program, fragment);
      gl.linkProgram(program);
      gl.deleteShader(vertex);
      gl.deleteShader(fragment);
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        throw new Error(gl.getProgramInfoLog(program) || 'Aura shader linking failed.');
      }
      gl.useProgram(program);

      const buffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
      const position = gl.getAttribLocation(program, 'aPosition');
      gl.enableVertexAttribArray(position);
      gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);

      const texture = gl.createTexture();
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, texture);
      // Typed arrays ignore UNPACK_FLIP_Y_WEBGL in WebGL 1; reverse rows once.
      const flipped = new Uint8Array(mask.data.length);
      const rowBytes = mask.width * 4;
      for (let row = 0; row < mask.height; row++) {
        flipped.set(mask.data.subarray(row * rowBytes, (row + 1) * rowBytes),
          (mask.height - row - 1) * rowBytes);
      }
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, mask.width, mask.height, 0, gl.RGBA, gl.UNSIGNED_BYTE, flipped);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.uniform1i(gl.getUniformLocation(program, 'uMask'), 0);
      gl.uniform2f(gl.getUniformLocation(program, 'uTexel'), 1 / mask.width, 1 / mask.height);
      gl.uniform2fv(gl.getUniformLocation(program, 'uMaskScale'), mask.scale);
      gl.uniform2fv(gl.getUniformLocation(program, 'uMaskOffset'), mask.offset);
      gl.disable(gl.DEPTH_TEST);
      gl.disable(gl.BLEND);
      gl.clearColor(0, 0, 0, 0);

      resources = {
        program, buffer, texture,
        time: gl.getUniformLocation(program, 'uTime'),
        intro: gl.getUniformLocation(program, 'uIntro'),
        pointer: gl.getUniformLocation(program, 'uPointer')
      };
      resizeNeeded = true;
      lastPaint = -Infinity;
      updateControls();
    }

    function fitCanvas() {
      const rect = canvas.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 1.75);
      const width = Math.max(1, Math.round(rect.width * dpr));
      const height = Math.max(1, Math.round(rect.height * dpr));
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
      }
      gl.viewport(0, 0, width, height);
      resizeNeeded = false;
    }

    function frame(timestamp) {
      raf = null;
      if (failed || lost || document.hidden || pageHidden) return;
      const moving = canAnimate();
      const delta = lastTick === null ? 0 : Math.min((timestamp - lastTick) / 1000, 0.05);
      lastTick = timestamp;
      if (moving) {
        elapsed += delta;
        const follow = 1 - Math.exp(-delta * 5.5);
        pointer.x += (pointer.targetX - pointer.x) * follow;
        pointer.y += (pointer.targetY - pointer.y) * follow;
      }

      const interval = coarsePointer.matches || window.innerWidth < 700 ? 1000 / 30 : 1000 / 60;
      if (timestamp - lastPaint >= interval - 0.75 || resizeNeeded || !revealed || !moving) {
        try {
          if (resizeNeeded) fitCanvas();
          gl.useProgram(resources.program);
          gl.uniform1f(resources.time, reducedMotion.matches ? 0 : elapsed);
          gl.uniform1f(resources.intro, reducedMotion.matches ? 1 : Math.min(elapsed / 2.4, 1));
          gl.uniform2f(resources.pointer, reducedMotion.matches ? 0 : pointer.x, reducedMotion.matches ? 0 : pointer.y);
          gl.clear(gl.COLOR_BUFFER_BIT);
          gl.drawArrays(gl.TRIANGLES, 0, 6);
          if (!revealed) {
            if (gl.isContextLost()) return;
            const error = gl.getError();
            if (error !== gl.NO_ERROR) throw new Error(`WebGL draw failed (${error}).`);
            // Never obscure the SVG before the first successful GPU frame.
            revealed = true;
            canvas.dataset.ready = 'true';
            canvas.classList.add('is-ready');
            canvas.style.opacity = '1';
            updateControls();
          }
          lastPaint = timestamp;
        } catch (error) {
          useFallback(error);
          return;
        }
      }
      if (moving) requestPaint();
      else lastTick = null;
    }

    if (toggle) toggle.addEventListener('click', () => {
      if (failed || lost || reducedMotion.matches) return;
      paused = !paused;
      stop();
      updateControls();
      requestPaint();
    });

    if (replay) replay.addEventListener('click', () => {
      if (failed || lost || reducedMotion.matches) return;
      elapsed = 0;
      paused = false;
      lastPaint = -Infinity;
      stop();
      updateControls();
      requestPaint();
    });

    sculpture.addEventListener('pointermove', (event) => {
      if (!canAnimate() || event.pointerType === 'touch') return;
      const rect = sculpture.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      pointer.targetX = Math.max(-1, Math.min(1, (event.clientX - rect.left) / rect.width * 2 - 1));
      pointer.targetY = Math.max(-1, Math.min(1, 1 - (event.clientY - rect.top) / rect.height * 2));
    }, { passive: true });
    sculpture.addEventListener('pointerleave', () => {
      pointer.targetX = 0;
      pointer.targetY = 0;
    }, { passive: true });

    function onMotionPreference() {
      stop();
      pointer.x = pointer.y = pointer.targetX = pointer.targetY = 0;
      // Returning from reduced motion resumes the finished composition.
      if (!reducedMotion.matches) elapsed = Math.max(elapsed, 2.4);
      updateControls();
      requestPaint();
    }
    if (reducedMotion.addEventListener) reducedMotion.addEventListener('change', onMotionPreference);
    else reducedMotion.addListener(onMotionPreference);

    document.addEventListener('visibilitychange', () => {
      stop();
      if (!document.hidden) requestPaint();
    });
    window.addEventListener('pagehide', () => { pageHidden = true; stop(); });
    window.addEventListener('pageshow', () => { pageHidden = false; requestPaint(); });

    canvas.addEventListener('webglcontextlost', (event) => {
      event.preventDefault();
      lost = true;
      revealed = false;
      stop();
      canvas.style.opacity = '0';
      canvas.classList.remove('is-ready');
      canvas.dataset.ready = 'false';
      updateControls();
    });
    canvas.addEventListener('webglcontextrestored', () => {
      lost = false;
      try {
        initializeGL();
        requestPaint();
      } catch (error) { useFallback(error); }
    });

    const onResize = () => {
      resizeNeeded = true;
      requestPaint();
    };
    if (typeof ResizeObserver !== 'undefined') new ResizeObserver(onResize).observe(sculpture);
    window.addEventListener('resize', onResize, { passive: true });

    try {
      initializeGL();
      requestPaint();
    } catch (error) { useFallback(error); }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();
