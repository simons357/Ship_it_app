import React, { useEffect, useRef } from "react";
import * as THREE from "three";

// ── Math helpers ───────────────────────────────────────────────────
const N_SHELLS = 12;
const REF_MU = (() => {
  const raw = Array.from({ length: N_SHELLS }, (_, j) => Math.exp(-0.35 * j) * 0.6);
  const sum = raw.reduce((a, b) => a + b, 0);
  return raw.map(v => v / sum);
})();

const ZEROS = [14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919,
  43.327, 48.005, 49.774, 52.970, 56.446, 59.347, 60.832, 65.113];

export default function Explorer3DCanvas({ layers, params, setParams, crossSection, onMeasure }) {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const frameRef = useRef(null);
  const timeRef = useRef(0);
  const objectsRef = useRef({});
  const measureGroupRef = useRef(null);

  useEffect(() => {
    const mount = mountRef.current;
    const W = mount.clientWidth, H = mount.clientHeight;

    // ── Renderer ──
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(W, H);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setClearColor(0x04050a);
    mount.appendChild(renderer.domElement);

    // ── Scene ──
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.fog = new THREE.Fog(0x04050a, 30, 80);

    // ── Camera ──
    const camera = new THREE.PerspectiveCamera(55, W / H, 0.1, 200);
    camera.position.set(8, 6, 14);
    camera.lookAt(0, 0, 0);

    // ── Lights ──
    scene.add(new THREE.AmbientLight(0x111122, 1.5));
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(5, 10, 7);
    scene.add(dirLight);
    const ptLight = new THREE.PointLight(0x22d3ee, 1, 30);
    ptLight.position.set(-4, 4, 4);
    scene.add(ptLight);

    // ── Grid ──
    const grid = new THREE.GridHelper(20, 20, 0x111827, 0x0d1117);
    grid.position.y = -4;
    scene.add(grid);

    // ── Axes ──
    const axesMat = (color) => new THREE.LineBasicMaterial({ color });
    const axLine = (a, b, mat) => {
      const g = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(...a), new THREE.Vector3(...b)]);
      return new THREE.Line(g, mat);
    };
    const axisGroup = new THREE.Group();
    axisGroup.add(axLine([0,0,0],[6,0,0], axesMat(0x374151)));
    axisGroup.add(axLine([0,0,0],[0,6,0], axesMat(0x374151)));
    axisGroup.add(axLine([0,0,0],[0,0,6], axesMat(0x374151)));
    scene.add(axisGroup);

    // ── Object groups ──
    const groups = {
      simplex:     new THREE.Group(),
      spectral:    new THREE.Group(),
      cascade:     new THREE.Group(),
      zeros:       new THREE.Group(),
      snd:         new THREE.Group(),
      connections: new THREE.Group(),
    };
    Object.values(groups).forEach(g => scene.add(g));
    objectsRef.current = groups;

    // ── SIMPLEX — shell bars rising from y=-4 ──
    const simplexBars = [];
    for (let j = 0; j < N_SHELLS; j++) {
      const geo = new THREE.CylinderGeometry(0.18, 0.22, 1, 8);
      const mat = new THREE.MeshPhongMaterial({
        color: new THREE.Color(0x22d3ee),
        emissive: new THREE.Color(0x0a4a55),
        transparent: true, opacity: 0.85,
        shininess: 80,
      });
      const mesh = new THREE.Mesh(geo, mat);
      const angle = (j / N_SHELLS) * Math.PI * 2;
      const radius = 4;
      mesh.position.set(Math.cos(angle) * radius, 0, Math.sin(angle) * radius);
      mesh.userData = { type: "simplex", shell: j, label: `Shell P_${j+1}` };
      groups.simplex.add(mesh);
      simplexBars.push(mesh);

      // Shell label sprite
      const ring = new THREE.Mesh(
        new THREE.TorusGeometry(0.22, 0.02, 8, 20),
        new THREE.MeshBasicMaterial({ color: 0x22d3ee, transparent: true, opacity: 0.3 })
      );
      ring.position.copy(mesh.position);
      ring.rotation.x = Math.PI / 2;
      groups.simplex.add(ring);
    }

    // ── SPECTRAL — curved surface λ_min over (η, t) plane ──
    const SPEC_U = 30, SPEC_V = 30;
    const specGeo = new THREE.PlaneGeometry(8, 8, SPEC_U - 1, SPEC_V - 1);
    const specMat = new THREE.MeshPhongMaterial({
      color: 0xa78bfa, wireframe: false,
      transparent: true, opacity: 0.3,
      side: THREE.DoubleSide,
    });
    const specMesh = new THREE.Mesh(specGeo, specMat);
    specMesh.rotation.x = -Math.PI / 2;
    specMesh.position.set(-5, -1, -5);
    specMesh.userData = { type: "spectral", label: "λ_min surface" };
    groups.spectral.add(specMesh);

    // Hard floor plane
    const floorGeo = new THREE.PlaneGeometry(12, 12);
    const floorMat = new THREE.MeshBasicMaterial({
      color: 0xef4444, transparent: true, opacity: 0.08, side: THREE.DoubleSide,
    });
    const floorMesh = new THREE.Mesh(floorGeo, floorMat);
    floorMesh.rotation.x = -Math.PI / 2;
    floorMesh.position.y = -3.5;
    floorMesh.userData = { type: "spectral", label: "Hard Floor λ = −½" };
    groups.spectral.add(floorMesh);

    // Hard floor grid lines
    const floorLine = new THREE.LineSegments(
      new THREE.EdgesGeometry(new THREE.PlaneGeometry(12, 12, 6, 6)),
      new THREE.LineBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.15 })
    );
    floorLine.rotation.x = -Math.PI / 2;
    floorLine.position.y = -3.5;
    groups.spectral.add(floorLine);

    // ── CASCADE — diagonal pipes along z axis ──
    const cascadeArrows = [];
    for (let j = 0; j < 10; j++) {
      const t = j / 9;
      const energy = Math.pow(0.7, j);
      const geo = new THREE.CapsuleGeometry(0.1 + energy * 0.15, energy * 1.5, 6, 12);
      const r = j < 3 ? 0x22d3ee : j < 7 ? 0xa78bfa : 0xf59e0b;
      const mat = new THREE.MeshPhongMaterial({ color: r, emissive: r, emissiveIntensity: 0.2, transparent: true, opacity: 0.8 });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(j * 1.1 - 5.5, -2 + energy * 1.5, 5);
      mesh.userData = { type: "cascade", shell: j, label: `Cascade P_${j+1}` };
      groups.cascade.add(mesh);
      cascadeArrows.push(mesh);

      // Flow connector
      if (j < 9) {
        const pts = [
          new THREE.Vector3(j * 1.1 - 5.5, -2 + energy * 1.5, 5),
          new THREE.Vector3((j + 1) * 1.1 - 5.5, -2 + Math.pow(0.7, j + 1) * 1.5, 5),
        ];
        const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
        const lineMat = new THREE.LineBasicMaterial({ color: r, transparent: true, opacity: 0.25 });
        groups.cascade.add(new THREE.Line(lineGeo, lineMat));
      }
    }

    // ── ZEROS — spheres along critical line ──
    const zeroBalls = [];
    ZEROS.forEach((t, i) => {
      const geo = new THREE.SphereGeometry(0.18, 16, 16);
      const mat = new THREE.MeshPhongMaterial({
        color: 0xec4899, emissive: 0x7d1042, transparent: true, opacity: 0.9, shininess: 120
      });
      const mesh = new THREE.Mesh(geo, mat);
      // Map Im(t) → z, Re(s)=½ → x=0 line
      mesh.position.set(-8, (t / 80) * 8 - 4, -3);
      mesh.userData = { type: "zeros", zero: t, label: `ζ(½ + ${t.toFixed(3)}i) = 0` };
      groups.zeros.add(mesh);
      zeroBalls.push(mesh);
    });
    // Critical line
    const critPts = [new THREE.Vector3(-8, -4, -3), new THREE.Vector3(-8, 4, -3)];
    const critLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(critPts),
      new THREE.LineBasicMaterial({ color: 0x22d3ee, transparent: true, opacity: 0.3 })
    );
    groups.zeros.add(critLine);

    // ── SND TUBE ——
    const tubeGeo = new THREE.CylinderGeometry(1.8, 1.8, 8, 32, 1, true);
    const tubeMat = new THREE.MeshBasicMaterial({
      color: 0x34d399, transparent: true, opacity: 0.08, side: THREE.DoubleSide, wireframe: false
    });
    const tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
    tubeMesh.position.set(0, 0, 0);
    const tubeEdge = new THREE.LineSegments(
      new THREE.EdgesGeometry(new THREE.CylinderGeometry(1.8, 1.8, 8, 16, 1, true)),
      new THREE.LineBasicMaterial({ color: 0x34d399, transparent: true, opacity: 0.2 })
    );
    tubeEdge.position.set(0, 0, 0);
    groups.snd.add(tubeMesh);
    groups.snd.add(tubeEdge);

    // ── CONNECTIONS — lines linking simplex shells to spectral surface ──
    for (let j = 0; j < N_SHELLS; j++) {
      const angle = (j / N_SHELLS) * Math.PI * 2;
      const r = 4;
      const pts = [
        new THREE.Vector3(Math.cos(angle) * r, REF_MU[j] * 10 - 4, Math.sin(angle) * r),
        new THREE.Vector3(-5 + (j / N_SHELLS) * 8, -1 - REF_MU[j] * 2, -5 + (j / N_SHELLS) * 8),
      ];
      const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
      const lineMat = new THREE.LineBasicMaterial({ color: 0x6366f1, transparent: true, opacity: 0.2 });
      groups.connections.add(new THREE.Line(lineGeo, lineMat));
    }

    // ── Orbit controls (manual) ──
    let isDragging = false, isRight = false;
    let prevMouse = { x: 0, y: 0 };
    let spherical = { theta: 0.5, phi: 0.9, radius: 18 };
    let panOffset = new THREE.Vector3();

    function updateCamera() {
      const x = spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
      const y = spherical.radius * Math.cos(spherical.phi);
      const z = spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
      camera.position.set(x + panOffset.x, y + panOffset.y, z + panOffset.z);
      camera.lookAt(panOffset);
    }
    updateCamera();

    const onMouseDown = e => {
      isDragging = true;
      isRight = e.button === 2;
      prevMouse = { x: e.clientX, y: e.clientY };
    };
    const onMouseUp = () => { isDragging = false; };
    const onMouseMove = e => {
      if (!isDragging) return;
      const dx = e.clientX - prevMouse.x;
      const dy = e.clientY - prevMouse.y;
      prevMouse = { x: e.clientX, y: e.clientY };
      if (!isRight) {
        spherical.theta -= dx * 0.008;
        spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi + dy * 0.008));
      } else {
        const right = new THREE.Vector3();
        const up = new THREE.Vector3(0, 1, 0);
        right.crossVectors(camera.getWorldDirection(new THREE.Vector3()), up).normalize();
        panOffset.addScaledVector(right, -dx * 0.02);
        panOffset.addScaledVector(up, dy * 0.02);
      }
      updateCamera();
    };
    const onWheel = e => {
      spherical.radius = Math.max(5, Math.min(50, spherical.radius + e.deltaY * 0.03));
      updateCamera();
    };
    const onContextMenu = e => e.preventDefault();

    // Click to measure
    const raycaster = new THREE.Raycaster();
    const onClick = e => {
      const rect = mount.getBoundingClientRect();
      const mouse = new THREE.Vector2(
        ((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1,
      );
      raycaster.setFromCamera(mouse, camera);
      const allMeshes = [];
      Object.values(groups).forEach(g => g.traverse(o => { if (o.isMesh) allMeshes.push(o); }));
      const hits = raycaster.intersectObjects(allMeshes);
      if (hits.length > 0) {
        const hit = hits[0];
        onMeasure({
          label: hit.object.userData.label || "Object",
          type: hit.object.userData.type,
          shell: hit.object.userData.shell,
          zero: hit.object.userData.zero,
          point: hit.point.clone(),
          distance: hit.distance,
        });
        // Highlight
        if (measureGroupRef.current) scene.remove(measureGroupRef.current);
        const mg = new THREE.Group();
        const sphere = new THREE.Mesh(
          new THREE.SphereGeometry(0.25, 16, 16),
          new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.6 })
        );
        sphere.position.copy(hit.point);
        mg.add(sphere);
        const ring = new THREE.Mesh(
          new THREE.TorusGeometry(0.5, 0.04, 8, 32),
          new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.3 })
        );
        ring.position.copy(hit.point);
        mg.add(ring);
        scene.add(mg);
        measureGroupRef.current = mg;
      }
    };

    mount.addEventListener("mousedown", onMouseDown);
    mount.addEventListener("mouseup", onMouseUp);
    mount.addEventListener("mousemove", onMouseMove);
    mount.addEventListener("wheel", onWheel, { passive: true });
    mount.addEventListener("contextmenu", onContextMenu);
    mount.addEventListener("click", onClick);

    // ── Animate ──
    let lastTime = 0;
    function animate(now) {
      frameRef.current = requestAnimationFrame(animate);
      const dt = Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;

      if (params.animating) timeRef.current += dt;
      const t = timeRef.current;

      // Update simplex bar heights
      const bars = groups.simplex.children.filter(c => c.isMesh && c.userData.type === "simplex");
      bars.forEach((bar, j) => {
        if (j >= N_SHELLS) return;
        const anim = REF_MU[j] * (1 + 0.2 * Math.sin(t * 1.2 + j * 0.7));
        const h = Math.max(0.1, anim * 10);
        bar.scale.y = h;
        bar.position.y = h / 2 - 4;
        bar.material.emissiveIntensity = 0.1 + 0.3 * Math.sin(t + j);
      });

      // Update spectral surface
      const specPos = specMesh.geometry.attributes.position;
      for (let ui = 0; ui < SPEC_U; ui++) {
        for (let vi = 0; vi < SPEC_V; vi++) {
          const idx = ui * SPEC_V + vi;
          const eta = (ui / (SPEC_U - 1)) * 0.5;
          const time_wave = 0.05 * Math.sin(t * 0.8 + ui * 0.3 + vi * 0.4);
          const lam = 0.3 - 1.5 * eta + time_wave;
          // z is up (plane is rotated)
          specPos.setZ(idx, lam * 3);
        }
      }
      specPos.needsUpdate = true;
      specMesh.geometry.computeVertexNormals();

      // Update cascade
      const cBars = groups.cascade.children.filter(c => c.isMesh && c.userData.type === "cascade");
      cBars.forEach((bar, j) => {
        const e = Math.pow(0.7, j) * (1 + 0.15 * Math.sin(t * 1.4 + j));
        bar.scale.y = Math.max(0.1, e);
        bar.material.emissiveIntensity = 0.1 + 0.2 * Math.sin(t * 0.9 + j * 0.5);
      });

      // Pulse zeros
      groups.zeros.children.filter(c => c.isMesh).forEach((ball, i) => {
        const pulse = 1 + 0.15 * Math.sin(t * 0.7 + i * 1.3);
        ball.scale.setScalar(pulse);
        ball.material.emissiveIntensity = 0.2 + 0.4 * Math.sin(t * 0.5 + i);
      });

      // Cross-section clipping
      const plane = new THREE.Plane();
      const norm = crossSection.axis === "x" ? new THREE.Vector3(1, 0, 0)
        : crossSection.axis === "y" ? new THREE.Vector3(0, 1, 0)
        : new THREE.Vector3(0, 0, 1);
      plane.set(norm, -crossSection.value);
      renderer.clippingPlanes = crossSection.value !== 0 ? [plane] : [];
      renderer.localClippingEnabled = crossSection.value !== 0;

      // Layer visibility
      Object.entries(groups).forEach(([key, g]) => {
        g.visible = layers[key]?.on ?? true;
      });

      renderer.render(scene, camera);
    }
    frameRef.current = requestAnimationFrame(animate);

    // Resize
    const onResize = () => {
      const W = mount.clientWidth, H = mount.clientHeight;
      camera.aspect = W / H;
      camera.updateProjectionMatrix();
      renderer.setSize(W, H);
    };
    window.addEventListener("resize", onResize);

    return () => {
      cancelAnimationFrame(frameRef.current);
      mount.removeEventListener("mousedown", onMouseDown);
      mount.removeEventListener("mouseup", onMouseUp);
      mount.removeEventListener("mousemove", onMouseMove);
      mount.removeEventListener("wheel", onWheel);
      mount.removeEventListener("contextmenu", onContextMenu);
      mount.removeEventListener("click", onClick);
      window.removeEventListener("resize", onResize);
      mount.removeChild(renderer.domElement);
      renderer.dispose();
    };
  }, []); // only mount once

  // ── Reactively sync params / layers / crossSection via refs ──
  const paramsRef = useRef(params);
  const layersRef = useRef(layers);
  const csRef = useRef(crossSection);
  paramsRef.current = params;
  layersRef.current = layers;
  csRef.current = crossSection;

  return <div ref={mountRef} className="w-full h-full" style={{ touchAction: "none" }} />;
}