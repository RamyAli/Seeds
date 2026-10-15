/* Lumo 3D scenes (concept). Requires THREE (r149) loaded first.
   Lumo3D.mount(canvas, { scene: 'home'|'panel'|'coin', theme: 'day'|'night'|'cloudy', mirror: bool, still: bool })
   returns { dispose() } or null when WebGL is unavailable. */
(function () {
  var T = window.THREE;
  if (!T) return;

  var C = {
    solar: 0xFFA51F, battery: 0x8FD920, grid: 0x3D8BFF, ev: 0x111315, lime: 0xA6F23C
  };

  var THEMES = {
    day: { hemiSky: 0xffffff, hemiGround: 0xdfe3e8, hemi: 0.95, sun: 0xfff1dc, sunI: 1.35, ground: 0xF7F8FA, rim: 0xE4E6EA,
      wall: 0xFCFCFB, wall2: 0xF0EEEA, glass: 0x2A3646, glassEm: 0x000000, glassEmI: 0, leaf: 0x58B04E, trunk: 0xB58A5E, pool: 0x5EC2FF, exposure: 1.05 },
    night: { hemiSky: 0x5a6a9a, hemiGround: 0x101420, hemi: 0.55, sun: 0x9fb4ff, sunI: 0.35, ground: 0x23262C, rim: 0x2E3238,
      wall: 0xC9CCD3, wall2: 0xB5B9C2, glass: 0x3B2E1A, glassEm: 0xFFC46B, glassEmI: 1.4, leaf: 0x2F5E33, trunk: 0x6B5038, pool: 0x1E6FB8, exposure: 1.0 },
    cloudy: { hemiSky: 0xe9edf2, hemiGround: 0xc9ced6, hemi: 1.0, sun: 0xeef2f7, sunI: 0.55, ground: 0xF2F3F5, rim: 0xE0E2E6,
      wall: 0xF6F6F5, wall2: 0xE9E8E5, glass: 0x3A4655, glassEm: 0x000000, glassEmI: 0, leaf: 0x5E9E57, trunk: 0xA88560, pool: 0x7FB6D9, exposure: 1.0 }
  };

  function std(color, o) {
    return new T.MeshStandardMaterial(Object.assign({ color: color, roughness: 0.62, metalness: 0 }, o || {}));
  }
  function box(w, h, d, m) {
    var mesh = new T.Mesh(new T.BoxGeometry(w, h, d), m);
    mesh.castShadow = true; mesh.receiveShadow = true;
    return mesh;
  }
  function at(o, x, y, z) { o.position.set(x, y, z); return o; }

  function panelTexture() {
    var c = document.createElement('canvas'); c.width = 192; c.height = 128;
    var g = c.getContext('2d');
    g.fillStyle = '#18263D'; g.fillRect(0, 0, 192, 128);
    g.strokeStyle = '#4C6A96'; g.lineWidth = 2;
    for (var i = 1; i < 6; i++) { g.beginPath(); g.moveTo(i * 32, 0); g.lineTo(i * 32, 128); g.stroke(); }
    for (var j = 1; j < 4; j++) { g.beginPath(); g.moveTo(0, j * 32); g.lineTo(192, j * 32); g.stroke(); }
    var gr = g.createLinearGradient(0, 0, 192, 128);
    gr.addColorStop(0, 'rgba(255,255,255,0.18)'); gr.addColorStop(0.5, 'rgba(255,255,255,0)'); gr.addColorStop(1, 'rgba(255,255,255,0.06)');
    g.fillStyle = gr; g.fillRect(0, 0, 192, 128);
    var t = new T.CanvasTexture(c); t.encoding = T.sRGBEncoding; t.anisotropy = 4;
    return t;
  }

  function solarPanel(tex, w, d) {
    var frame = std(0xDCE0E5, { roughness: 0.4, metalness: 0.3 });
    var face = std(0xffffff, { map: tex, roughness: 0.25, metalness: 0.35 });
    var m = new T.Mesh(new T.BoxGeometry(w, 0.05, d), [frame, frame, face, frame, frame, frame]);
    m.castShadow = true; m.receiveShadow = true;
    return m;
  }

  function palm(th) {
    var g = new T.Group();
    var trunkM = std(th.trunk, { roughness: 0.9 });
    var y = 0, x = 0;
    for (var i = 0; i < 6; i++) {
      var seg = new T.Mesh(new T.CylinderGeometry(0.09 - i * 0.008, 0.11 - i * 0.008, 0.42, 10), trunkM);
      seg.position.set(x, y + 0.21, 0); seg.rotation.z = -0.06 * i; seg.castShadow = true;
      g.add(seg); y += 0.4; x += 0.035 * i;
    }
    var leafM = std(th.leaf, { roughness: 0.8, side: T.DoubleSide });
    for (var k = 0; k < 8; k++) {
      var leaf = new T.Mesh(new T.ConeGeometry(0.16, 1.25, 4, 1), leafM);
      leaf.scale.set(1, 1, 0.22);
      var holder = new T.Group();
      leaf.position.y = 0.6; leaf.rotation.x = 0;
      holder.add(leaf);
      holder.position.set(x, y, 0);
      holder.rotation.y = (k / 8) * Math.PI * 2;
      holder.rotation.z = 1.05 + (k % 2) * 0.25;
      leaf.castShadow = true;
      g.add(holder);
    }
    return g;
  }

  function car(th, theme) {
    var g = new T.Group();
    var body = box(1.7, 0.42, 0.86, std(theme === 'night' ? 0xD8DBE0 : 0xF7F7F8, { roughness: 0.3, metalness: 0.35 }));
    at(body, 0, 0.42, 0); g.add(body);
    var cab = box(0.98, 0.36, 0.78, std(0x1D2531, { roughness: 0.15, metalness: 0.5 }));
    at(cab, -0.1, 0.8, 0); g.add(cab);
    var wm = std(0x15171A, { roughness: 0.7 });
    [[-0.55, 0.43], [0.55, 0.43], [-0.55, -0.43], [0.55, -0.43]].forEach(function (p) {
      var w = new T.Mesh(new T.CylinderGeometry(0.19, 0.19, 0.14, 18), wm);
      w.rotation.x = Math.PI / 2; w.position.set(p[0], 0.2, p[1]); w.castShadow = true; g.add(w);
    });
    var light = box(0.04, 0.06, 0.6, std(0xffffff, { emissive: 0xffffff, emissiveIntensity: theme === 'night' ? 1 : 0.2 }));
    at(light, 0.86, 0.5, 0); g.add(light);
    return g;
  }

  function pylon() {
    var g = new T.Group();
    var m = std(0x9AA3AD, { roughness: 0.5, metalness: 0.4 });
    var legs = [[-0.22, -0.22], [0.22, -0.22], [-0.22, 0.22], [0.22, 0.22]];
    legs.forEach(function (l) {
      var leg = box(0.05, 2.7, 0.05, m);
      leg.position.set(l[0] * 0.55, 1.35, l[1] * 0.55);
      leg.rotation.z = -l[0] * 0.18; leg.rotation.x = l[1] * 0.18;
      g.add(leg);
    });
    [1.9, 2.45].forEach(function (y, i) { g.add(at(box(1.3 - i * 0.3, 0.05, 0.05, m), 0, y, 0)); });
    [-0.6, 0.6].forEach(function (x) { g.add(at(box(0.04, 0.16, 0.04, std(0x3D8BFF, { emissive: 0x3D8BFF, emissiveIntensity: 0.4 })), x, 1.82, 0)); });
    return g;
  }

  function flowArc(a, b, lift) {
    var mid = new T.Vector3().addVectors(a, b).multiplyScalar(0.5);
    mid.y += lift;
    return new T.QuadraticBezierCurve3(a, mid, b);
  }

  function makeFlow(group, curve, color, kw, active) {
    var tubeM = new T.MeshBasicMaterial({ color: active ? color : 0xA9AFB7, transparent: true, opacity: active ? 0.28 : 0.35 });
    var tube = new T.Mesh(new T.TubeGeometry(curve, 48, 0.022 + Math.min(kw, 9) * 0.004, 8, false), tubeM);
    group.add(tube);
    var dots = [];
    if (active && kw > 0) {
      var n = Math.max(3, Math.min(12, Math.round(kw * 1.4)));
      var r = 0.05 + Math.min(kw, 9) * 0.008;
      var dm = new T.MeshBasicMaterial({ color: color });
      var geo = new T.SphereGeometry(r, 12, 10);
      for (var i = 0; i < n; i++) {
        var d = new T.Mesh(geo, dm); group.add(d);
        dots.push({ m: d, o: i / n });
      }
      var glow = new T.PointLight(color, 0.35, 2.2);
      group.add(glow); dots.glow = glow;
    }
    return { curve: curve, dots: dots, speed: 0.1 + Math.min(kw, 9) * 0.045 };
  }

  function buildHome(scene, theme) {
    var th = THEMES[theme] || THEMES.day;
    var world = new T.Group(); scene.add(world);

    var plat = new T.Mesh(new T.CylinderGeometry(4.6, 4.6, 0.28, 72), std(th.ground, { roughness: 0.9 }));
    plat.position.y = -0.14; plat.receiveShadow = true; world.add(plat);
    var ring = new T.Mesh(new T.TorusGeometry(4.6, 0.025, 8, 96), std(th.rim));
    ring.rotation.x = Math.PI / 2; world.add(ring);

    var wall = std(th.wall, { roughness: 0.75 });
    var wall2 = std(th.wall2, { roughness: 0.75 });
    var slab = std(0xffffff, { roughness: 0.6 });
    var glass = std(th.glass, { roughness: 0.12, metalness: 0.55, emissive: th.glassEm, emissiveIntensity: th.glassEmI });

    world.add(at(box(4.2, 1.5, 3.0, wall), 0, 0.75, 0));
    world.add(at(box(4.6, 0.12, 3.4, slab), 0, 1.56, 0));
    world.add(at(box(2.6, 1.2, 2.4, wall2), -0.6, 2.22, -0.2));
    world.add(at(box(3.0, 0.12, 2.8, slab), -0.6, 2.88, -0.2));

    world.add(at(box(2.2, 1.0, 0.04, glass), 0.65, 0.72, 1.51));
    world.add(at(box(1.6, 0.7, 0.04, glass), -0.55, 2.2, 1.01));
    var side = box(0.04, 0.9, 1.6, glass); world.add(at(side, 2.11, 0.75, 0.2));
    world.add(at(box(0.62, 1.15, 0.05, std(0xC8A27A, { roughness: 0.7 })), -1.35, 0.58, 1.52));
    if (theme === 'night') {
      var warm = new T.PointLight(0xFFC46B, 1.2, 5); warm.position.set(0.6, 0.9, 2.2); world.add(warm);
    }

    var tex = panelTexture();
    var panels = [];
    [-1.35, -0.6, 0.15].forEach(function (x) {
      [-0.85, -0.12].forEach(function (z) {
        var p = solarPanel(tex, 0.68, 0.56); p.position.set(x, 3.05, z); p.rotation.x = 0.32; world.add(p); panels.push(p);
      });
    });
    [1.2, 1.9].forEach(function (x) {
      [-0.95, -0.25].forEach(function (z) {
        var p = solarPanel(tex, 0.62, 0.56); p.position.set(x, 1.75, z); p.rotation.x = 0.32; world.add(p); panels.push(p);
      });
    });

    var pool = new T.Mesh(new T.BoxGeometry(2.0, 0.06, 1.15), std(th.pool, { roughness: 0.08, metalness: 0.2, emissive: theme === 'night' ? 0x1E6FB8 : 0x000000, emissiveIntensity: 0.5 }));
    pool.position.set(1.9, 0.02, 2.45); pool.receiveShadow = true; world.add(pool);
    world.add(at(box(2.2, 0.04, 1.35, std(0xE9ECEF)), 1.9, 0.0, 2.45));

    var p1 = palm(th); p1.position.set(-3.0, 0, 1.9); world.add(p1);
    var p2 = palm(th); p2.position.set(-3.5, 0, -0.6); p2.scale.setScalar(0.8); p2.rotation.y = 1.3; world.add(p2);

    var batOffline = theme === 'cloudy';
    var bat = box(0.56, 0.95, 0.28, std(batOffline ? 0xD5D8DD : 0xFFFFFF, { roughness: 0.4 }));
    bat.position.set(-2.3, 0.55, 0.45); world.add(bat);
    var led = box(0.08, 0.62, 0.02, std(batOffline ? 0x9AA0A8 : C.battery, { emissive: batOffline ? 0x000000 : C.battery, emissiveIntensity: 0.9 }));
    led.position.set(-2.3, 0.6, 0.6); world.add(led);

    var ev = car(th, theme); ev.position.set(2.85, 0, -1.95); ev.rotation.y = 0.35; world.add(ev);
    var post = box(0.16, 0.85, 0.16, std(0xFFFFFF)); post.position.set(2.05, 0.43, -2.85); world.add(post);
    var postLed = box(0.1, 0.1, 0.02, std(C.lime, { emissive: C.lime, emissiveIntensity: theme === 'night' ? 1.6 : 0.6 }));
    postLed.position.set(2.05, 0.7, -2.76); world.add(postLed);

    var py = pylon(); py.position.set(-2.55, 0, -2.85); world.add(py);

    var clouds = [];
    if (theme === 'cloudy') {
      var cm = std(0xffffff, { roughness: 1, transparent: true, opacity: 0.96 });
      [[-1.2, 4.3, -0.6, 1], [1.6, 4.0, 0.6, 0.8]].forEach(function (c) {
        var cg = new T.Group();
        [[0, 0, 0, 0.55], [0.55, -0.08, 0.1, 0.42], [-0.55, -0.1, 0, 0.4], [0.2, 0.25, -0.1, 0.42]].forEach(function (s) {
          var sp = new T.Mesh(new T.SphereGeometry(s[3], 20, 16), cm); sp.position.set(s[0], s[1], s[2]); sp.castShadow = true; cg.add(sp);
        });
        cg.position.set(c[0], c[1], c[2]); cg.scale.setScalar(c[3]); world.add(cg); clouds.push(cg);
      });
    }

    var hub = new T.Vector3(0.3, 2.0, 1.75);
    var hubRing = new T.Mesh(new T.TorusGeometry(0.2, 0.035, 10, 40), std(theme === 'night' ? 0xF3F4F5 : 0x111315, { roughness: 0.3 }));
    hubRing.position.copy(hub); world.add(hubRing);

    var cfg = {
      day: [['solar', 5.4, true], ['battery', 2.1, true, 'out'], ['grid', 0.7, true], ['ev', 0, false]],
      night: [['solar', 0, false], ['battery', 1.8, true, 'in'], ['grid', 8.2, true], ['ev', 7.4, true]],
      cloudy: [['solar', 1.1, true], ['battery', 0, false], ['grid', 3.4, true], ['ev', 0, false]]
    }[theme] || [];
    var P = {
      solar: new T.Vector3(-0.6, 3.15, -0.5),
      battery: new T.Vector3(-2.3, 1.1, 0.5),
      grid: new T.Vector3(-2.55, 2.45, -2.85),
      ev: new T.Vector3(2.05, 0.95, -2.85)
    };
    var col = { solar: C.solar, battery: C.battery, grid: C.grid, ev: theme === 'night' ? 0xF3F4F5 : 0x111315 };
    var flows = cfg.map(function (f) {
      var key = f[0], kw = f[1], active = f[2];
      var toHome = key === 'solar' || key === 'grid' || (key === 'battery' && f[3] === 'in');
      var curve = toHome ? flowArc(P[key], hub, 1.0) : flowArc(hub, P[key], 1.0);
      return makeFlow(world, curve, col[key], kw, active);
    });

    return {
      world: world, flows: flows, clouds: clouds, hubRing: hubRing,
      camera: { pos: [8.6, 7.0, 10.6], look: [0, 1.25, 0], fov: 29 }
    };
  }

  function buildPanel(scene, theme) {
    var world = new T.Group(); scene.add(world);
    var plat = new T.Mesh(new T.CylinderGeometry(3.2, 3.2, 0.22, 64), std(0xF7F8FA, { roughness: 0.9 }));
    plat.position.y = -0.11; plat.receiveShadow = true; world.add(plat);
    var tex = panelTexture();
    var frameM = std(0xC9CED4, { roughness: 0.4, metalness: 0.5 });
    var rig = new T.Group(); rig.position.y = 1.0; rig.rotation.x = -0.55; world.add(rig);
    for (var r = 0; r < 3; r++) for (var c = 0; c < 4; c++) {
      var p = solarPanel(tex, 0.95, 0.68); p.position.set(-1.5 + c * 1.0, 0, -0.73 + r * 0.73); rig.add(p);
    }
    [-1.4, 1.4].forEach(function (x) {
      world.add(at(box(0.08, 1.0, 0.08, frameM), x, 0.5, 0.35));
      world.add(at(box(0.08, 1.6, 0.08, frameM), x, 0.8, -0.6));
    });
    var inv = box(0.5, 0.6, 0.3, std(0xFFFFFF, { roughness: 0.4 })); inv.position.set(2.3, 0.3, 0.9); world.add(inv);
    world.add(at(box(0.06, 0.36, 0.02, std(C.lime, { emissive: C.lime, emissiveIntensity: 0.8 })), 2.3, 0.35, 1.06));
    var sun = new T.Mesh(new T.SphereGeometry(0.42, 32, 24), new T.MeshBasicMaterial({ color: 0xFFB230 }));
    world.add(sun);
    var halo = new T.Mesh(new T.SphereGeometry(0.75, 32, 24), new T.MeshBasicMaterial({ color: 0xFFD27A, transparent: true, opacity: 0.25 }));
    sun.add(halo);
    var flow = makeFlow(world, flowArc(new T.Vector3(0.6, 1.4, 0.4), new T.Vector3(2.3, 0.65, 0.9), 0.9), C.solar, 5.4, true);
    return { world: world, flows: [flow], sun: sun, camera: { pos: [5.6, 4.6, 6.8], look: [0, 0.9, 0], fov: 32 } };
  }

  function starShape(R, r) {
    var s = new T.Shape();
    for (var i = 0; i < 10; i++) {
      var a = Math.PI / 2 + (i * Math.PI) / 5, rad = i % 2 ? r : R;
      var x = Math.cos(a) * rad, y = Math.sin(a) * rad;
      if (i === 0) s.moveTo(x, y); else s.lineTo(x, y);
    }
    s.closePath();
    return s;
  }

  function buildCoin(scene) {
    var world = new T.Group(); scene.add(world);
    var coin = new T.Group(); world.add(coin);
    var lime = std(C.lime, { roughness: 0.28, metalness: 0.45 });
    var edge = std(0x7CC21A, { roughness: 0.3, metalness: 0.5 });
    var disc = new T.Mesh(new T.CylinderGeometry(1.25, 1.25, 0.26, 72), [edge, lime, lime]);
    disc.rotation.x = Math.PI / 2; disc.castShadow = true; coin.add(disc);
    var rim1 = new T.Mesh(new T.TorusGeometry(1.08, 0.05, 12, 72), edge); rim1.position.z = 0.13; coin.add(rim1);
    var rim2 = rim1.clone(); rim2.position.z = -0.13; coin.add(rim2);
    var starG = new T.ExtrudeGeometry(starShape(0.62, 0.27), { depth: 0.08, bevelEnabled: true, bevelSize: 0.03, bevelThickness: 0.03, bevelSegments: 2 });
    var starM = std(0x111315, { roughness: 0.35, metalness: 0.2 });
    var s1 = new T.Mesh(starG, starM); s1.position.z = 0.12; coin.add(s1);
    var s2 = new T.Mesh(starG, starM); s2.rotation.y = Math.PI; s2.position.z = -0.12; coin.add(s2);
    var sparkM = new T.MeshBasicMaterial({ color: 0xFFFFFF });
    var sparks = [];
    for (var i = 0; i < 6; i++) {
      var sp = new T.Mesh(new T.OctahedronGeometry(0.07 + (i % 3) * 0.03), i % 2 ? sparkM : new T.MeshBasicMaterial({ color: C.lime }));
      world.add(sp); sparks.push({ m: sp, a: (i / 6) * Math.PI * 2, r: 1.8 + (i % 2) * 0.35, y: (i % 3 - 1) * 0.6 });
    }
    var shadow = new T.Mesh(new T.CircleGeometry(1.1, 48), new T.MeshBasicMaterial({ color: 0x111315, transparent: true, opacity: 0.08 }));
    shadow.rotation.x = -Math.PI / 2; shadow.position.y = -1.7; world.add(shadow);
    return { world: world, coin: coin, sparks: sparks, flows: [], camera: { pos: [0, 0.6, 6.4], look: [0, 0, 0], fov: 34 } };
  }

  function mount(canvas, opts) {
    opts = opts || {};
    var w = canvas.clientWidth || +canvas.getAttribute('width') || 300;
    var h = canvas.clientHeight || +canvas.getAttribute('height') || 200;
    var renderer;
    try {
      renderer = new T.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, powerPreference: 'low-power' });
    } catch (e) { return null; }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(w, h, false);
    renderer.outputEncoding = T.sRGBEncoding;
    renderer.toneMapping = T.ACESFilmicToneMapping;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = T.PCFSoftShadowMap;

    var theme = opts.theme || 'day';
    var th = THEMES[theme] || THEMES.day;
    renderer.toneMappingExposure = th.exposure;
    var scene = new T.Scene();
    scene.add(new T.HemisphereLight(th.hemiSky, th.hemiGround, opts.scene === 'coin' ? 1.0 : th.hemi));
    var key = new T.DirectionalLight(opts.scene === 'home' ? th.sun : 0xfff1dc, opts.scene === 'home' ? th.sunI : 1.3);
    key.position.set(5, 10, 6); key.castShadow = true;
    key.shadow.mapSize.set(1024, 1024);
    key.shadow.camera.left = -7; key.shadow.camera.right = 7; key.shadow.camera.top = 7; key.shadow.camera.bottom = -7;
    key.shadow.bias = -0.0005; key.shadow.radius = 4;
    scene.add(key);
    var fill = new T.DirectionalLight(0xdfe9ff, 0.35); fill.position.set(-6, 4, -3); scene.add(fill);

    var built = opts.scene === 'panel' ? buildPanel(scene, theme) : opts.scene === 'coin' ? buildCoin(scene) : buildHome(scene, theme);
    if (opts.mirror) built.world.scale.x = -1;

    var cam = new T.PerspectiveCamera(built.camera.fov, w / h, 0.1, 100);
    cam.position.set(built.camera.pos[0], built.camera.pos[1], built.camera.pos[2]);
    if (opts.mirror) cam.position.x *= -1;
    var look = new T.Vector3(built.camera.look[0], built.camera.look[1], built.camera.look[2]);
    cam.lookAt(look);
    if (opts.zoom) cam.zoom = opts.zoom;
    if (opts.shift) {
      var sx = opts.mirror ? -opts.shift[0] : opts.shift[0];
      cam.setViewOffset(w, h, -sx * w, -opts.shift[1] * h, w, h);
    }
    cam.updateProjectionMatrix();

    var reduce = opts.still || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var yaw = 0, drag = null, raf = 0, last = 0, t0 = performance.now();
    function onDown(e) { drag = { x: e.clientX, yaw: yaw }; }
    function onMove(e) { if (drag) yaw = drag.yaw + (e.clientX - drag.x) * 0.008; }
    function onUp() { drag = null; }
    canvas.addEventListener('pointerdown', onDown);
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);

    function place(t) {
      var sway = reduce ? 0 : Math.sin(t * 0.18) * 0.14;
      if (opts.scene === 'coin') {
        built.coin.rotation.y = reduce ? 0.5 : t * 1.1;
        built.coin.position.y = reduce ? 0 : Math.sin(t * 1.6) * 0.08;
        built.sparks.forEach(function (s, i) {
          var a = s.a + (reduce ? 0 : t * 0.5);
          s.m.position.set(Math.cos(a) * s.r, s.y + (reduce ? 0 : Math.sin(t * 2 + i) * 0.1), Math.sin(a) * s.r * 0.4);
          s.m.rotation.y = t * 2;
        });
      } else {
        built.world.rotation.y = yaw + sway;
      }
      if (built.sun) {
        var sa = 0.9 + (reduce ? 0.3 : Math.sin(t * 0.25) * 0.35);
        built.sun.position.set(Math.cos(sa) * 3.6, 2.6 + Math.sin(sa) * 1.4, -1.6);
      }
      (built.clouds || []).forEach(function (c, i) { c.position.x += reduce ? 0 : Math.sin(t * 0.3 + i) * 0.002; });
      built.flows.forEach(function (f) {
        f.dots.forEach(function (d) {
          var u = reduce ? d.o : (d.o + t * f.speed) % 1;
          f.curve.getPointAt(u, d.m.position);
          var s = Math.sin(u * Math.PI); d.m.scale.setScalar(0.4 + s * 0.8);
        });
        if (f.dots.glow) f.curve.getPointAt(reduce ? 0.5 : (t * f.speed * 0.5) % 1, f.dots.glow.position);
      });
    }

    function frame(now) {
      raf = requestAnimationFrame(frame);
      if (document.hidden || now - last < 30) return;
      last = now;
      place((now - t0) / 1000);
      renderer.render(scene, cam);
    }
    if (reduce) { place(0); renderer.render(scene, cam); }
    else raf = requestAnimationFrame(frame);

    return {
      dispose: function () {
        cancelAnimationFrame(raf);
        canvas.removeEventListener('pointerdown', onDown);
        window.removeEventListener('pointermove', onMove);
        window.removeEventListener('pointerup', onUp);
        scene.traverse(function (o) {
          if (o.geometry) o.geometry.dispose();
          if (o.material) [].concat(o.material).forEach(function (m) { if (m.map) m.map.dispose(); m.dispose(); });
        });
        renderer.dispose();
      }
    };
  }

  window.Lumo3D = { mount: mount };
})();
