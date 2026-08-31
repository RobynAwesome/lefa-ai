import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import type { SystemState } from '../types';

interface Aether3DSceneProps {
  state: SystemState;
  reducedMotion?: boolean;
}

export const Aether3DScene: React.FC<Aether3DSceneProps> = ({ state, reducedMotion = false }) => {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Dimensions
    const width = container.clientWidth || 400;
    const height = container.clientHeight || 400;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.z = 6;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Root Group
    const rootGroup = new THREE.Group();
    scene.add(rootGroup);

    // 1. Core Sphere (Luminous Metallic Core)
    const coreGeo = new THREE.SphereGeometry(1.2, 64, 64);
    const coreMat = new THREE.MeshStandardMaterial({
      color: 0x111116,
      roughness: 0.15,
      metalness: 0.95,
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    rootGroup.add(coreMesh);

    // 2. Geodesic Wireframe Shell
    const shellGeo = new THREE.IcosahedronGeometry(1.28, 2);
    const shellMat = new THREE.MeshStandardMaterial({
      color: 0xd4af37,
      emissive: 0x854d0e,
      emissiveIntensity: 0.6,
      wireframe: true,
      transparent: true,
      opacity: 0.75,
    });
    const shellMesh = new THREE.Mesh(shellGeo, shellMat);
    rootGroup.add(shellMesh);

    // 3. Ring A (Gold Horizontal Gyroscope)
    const ringAGeo = new THREE.TorusGeometry(1.65, 0.015, 16, 100);
    const ringAMat = new THREE.MeshBasicMaterial({
      color: 0xd4af37,
      transparent: true,
      opacity: 0.5,
      blending: THREE.AdditiveBlending,
    });
    const ringA = new THREE.Mesh(ringAGeo, ringAMat);
    ringA.rotation.x = Math.PI / 2;
    rootGroup.add(ringA);

    // 4. Ring B (Emerald/Cyan Vertical Gyroscope)
    const ringBGeo = new THREE.TorusGeometry(1.85, 0.012, 16, 100);
    const ringBMat = new THREE.MeshBasicMaterial({
      color: 0x10b981,
      transparent: true,
      opacity: 0.4,
      blending: THREE.AdditiveBlending,
    });
    const ringB = new THREE.Mesh(ringBGeo, ringBMat);
    ringB.rotation.y = Math.PI / 2;
    rootGroup.add(ringB);

    // 5. Starfield / Ambient Floating Embers
    const particleCount = 200;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount * 3; i += 3) {
      particlePositions[i] = (Math.random() - 0.5) * 8;
      particlePositions[i + 1] = (Math.random() - 0.5) * 8;
      particlePositions[i + 2] = (Math.random() - 0.5) * 8;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    const particleMat = new THREE.PointsMaterial({
      color: 0xfef08a,
      size: 0.035,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xd4af37, 3, 20);
    pointLight.position.set(4, 4, 4);
    scene.add(pointLight);

    const secondaryLight = new THREE.PointLight(0x10b981, 2, 20);
    secondaryLight.position.set(-4, -2, -2);
    scene.add(secondaryLight);

    // Mouse tracking with smooth lerp
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      targetX = y * 0.8;
      targetY = x * 0.8;
    };

    window.addEventListener('mousemove', handleMouseMove);

    // Resize Handler
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    // Animation Loop
    let animationFrameId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      const delta = clock.getDelta();
      const time = clock.getElapsedTime();

      // State-specific physics & colors
      if (state === 'observing') {
        shellMat.color.setHex(0x10b981);
        shellMat.emissive.setHex(0x047857);
        ringBMat.color.setHex(0x34d399);
        pointLight.color.setHex(0x10b981);
      } else if (state === 'ledgered') {
        shellMat.color.setHex(0xd4af37);
        shellMat.emissive.setHex(0xb45309);
        ringAMat.color.setHex(0xfde047);
        pointLight.color.setHex(0xf59e0b);
      } else if (state === 'hold') {
        shellMat.color.setHex(0xf59e0b);
        shellMat.emissive.setHex(0xb45309);
        ringAMat.color.setHex(0xf97316);
        pointLight.color.setHex(0xef4444);
      } else if (state === 'reveal') {
        shellMat.color.setHex(0x38bdf8);
        shellMat.emissive.setHex(0x0284c7);
        ringBMat.color.setHex(0x7dd3fc);
        pointLight.color.setHex(0x38bdf8);
      } else {
        // disconnected
        shellMat.color.setHex(0x71717a);
        shellMat.emissive.setHex(0x27272a);
        ringAMat.color.setHex(0x52525b);
        pointLight.color.setHex(0x71717a);
      }

      if (!reducedMotion) {
        // Smooth Cursor Tilt
        mouseX = THREE.MathUtils.lerp(mouseX, targetX, 0.05);
        mouseY = THREE.MathUtils.lerp(mouseY, targetY, 0.05);
        rootGroup.rotation.x = mouseX;
        rootGroup.rotation.y = mouseY;

        // Core Rotations
        shellMesh.rotation.y += delta * (state === 'observing' ? 0.6 : 0.2);
        shellMesh.rotation.x += delta * 0.1;
        coreMesh.rotation.y -= delta * 0.15;

        // Gyroscope Rotations
        ringA.rotation.z += delta * 0.35;
        ringB.rotation.z -= delta * 0.45;

        // Breathing pulse
        const pulse = 1.0 + Math.sin(time * 2.2) * 0.025;
        rootGroup.scale.set(pulse, pulse, pulse);

        // Particle Drift
        particles.rotation.y = time * 0.04;
      }

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      if (renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
      coreGeo.dispose();
      coreMat.dispose();
      shellGeo.dispose();
      shellMat.dispose();
      ringAGeo.dispose();
      ringAMat.dispose();
      ringBGeo.dispose();
      ringBMat.dispose();
      particleGeo.dispose();
      particleMat.dispose();
    };
  }, [state, reducedMotion]);

  return (
    <div className="relative w-full h-[320px] sm:h-[400px] flex items-center justify-center overflow-hidden">
      {/* 3D WebGL Canvas Mount */}
      <div ref={mountRef} className="absolute inset-0 cursor-grab active:cursor-grabbing" />

      {/* Atmospheric Glow Radial Behind Orb */}
      <div
        className={`pointer-events-none absolute w-72 h-72 rounded-full blur-3xl opacity-25 transition-all duration-700 ${
          state === 'observing'
            ? 'bg-emerald-500'
            : state === 'ledgered'
            ? 'bg-amber-500'
            : state === 'hold'
            ? 'bg-orange-500'
            : state === 'reveal'
            ? 'bg-cyan-500'
            : 'bg-zinc-700'
        }`}
      />
    </div>
  );
};
