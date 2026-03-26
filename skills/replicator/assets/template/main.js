import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { GUI } from "lil-gui";

const effectTitle = "__EFFECT_TITLE__";
const canvas = document.getElementById("app");
const clock = new THREE.Clock();
const pointer = new THREE.Vector2();
const size = new THREE.Vector2();

const params = {
  dpr: Math.min(window.devicePixelRatio, 2),
  exposure: 1.0,
  bloomStrength: 0.28,
  bloomRadius: 0.45,
  bloomThreshold: 0.78,
  speed: 1.0,
  paused: false,
  autoRotate: false,
  wobble: 0.18,
  wobbleScale: 0.28,
  hueShift: 0.0,
  background: "#050608",
  glow: "#67e8f9",
  fill: "#a78bfa",
};

const renderer = new THREE.WebGLRenderer({
  canvas,
  antialias: true,
  alpha: false,
  powerPreference: "high-performance",
});
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = params.exposure;

const scene = new THREE.Scene();
scene.background = new THREE.Color(params.background);
scene.fog = new THREE.FogExp2(params.background, 0.08);

const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 40);
camera.position.set(0, 0.3, 4.8);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.enablePan = false;
controls.enableZoom = true;

const uniforms = {
  uTime: { value: 0 },
  uPointer: { value: pointer.clone() },
  uWobble: { value: params.wobble },
  uWobbleScale: { value: params.wobbleScale },
  uHueShift: { value: params.hueShift },
  uColorA: { value: new THREE.Color(params.glow) },
  uColorB: { value: new THREE.Color(params.fill) },
};

const geometry = new THREE.IcosahedronGeometry(1.3, 64);
const material = new THREE.ShaderMaterial({
  uniforms,
  vertexShader: /* glsl */ `
    uniform float uTime;
    uniform float uWobble;
    uniform float uWobbleScale;

    varying vec3 vNormal;
    varying vec3 vWorldPosition;

    float wave(vec3 p) {
      return sin(p.x * 2.8 + uTime * 1.2)
        * sin(p.y * 3.6 - uTime * 0.8)
        * cos(p.z * 3.1 + uTime * 0.6);
    }

    void main() {
      vec3 transformed = position + normal * wave(position * (1.0 + uWobbleScale)) * uWobble;
      vec4 world = modelMatrix * vec4(transformed, 1.0);
      vNormal = normalize(mat3(modelMatrix) * normal);
      vWorldPosition = world.xyz;
      gl_Position = projectionMatrix * viewMatrix * world;
    }
  `,
  fragmentShader: /* glsl */ `
    uniform float uHueShift;
    uniform vec2 uPointer;
    uniform vec3 uColorA;
    uniform vec3 uColorB;

    varying vec3 vNormal;
    varying vec3 vWorldPosition;

    vec3 hueRotate(vec3 color, float angle) {
      float s = sin(angle);
      float c = cos(angle);
      mat3 m = mat3(
        0.299 + 0.701 * c + 0.168 * s, 0.587 - 0.587 * c + 0.330 * s, 0.114 - 0.114 * c - 0.497 * s,
        0.299 - 0.299 * c - 0.328 * s, 0.587 + 0.413 * c + 0.035 * s, 0.114 - 0.114 * c + 0.292 * s,
        0.299 - 0.300 * c + 1.250 * s, 0.587 - 0.588 * c - 1.050 * s, 0.114 + 0.886 * c - 0.203 * s
      );
      return clamp(m * color, 0.0, 1.0);
    }

    void main() {
      vec3 normal = normalize(vNormal);
      vec3 viewDir = normalize(cameraPosition - vWorldPosition);
      float fresnel = pow(1.0 - max(dot(normal, viewDir), 0.0), 2.8);
      float bands = 0.5 + 0.5 * sin(vWorldPosition.y * 2.4 + uPointer.x * 2.0);
      vec3 color = mix(uColorA, uColorB, bands);
      color = hueRotate(color, uHueShift);
      color += fresnel * 0.85;
      gl_FragColor = vec4(color, 1.0);
    }
  `,
});

const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

const glow = new THREE.PointLight(params.glow, 25, 10, 2);
glow.position.set(2.2, 2.4, 2.8);
scene.add(glow);

const fill = new THREE.PointLight(params.fill, 18, 12, 2);
fill.position.set(-2.8, -1.5, -1.4);
scene.add(fill);

const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
const bloomPass = new UnrealBloomPass(new THREE.Vector2(1, 1), params.bloomStrength, params.bloomRadius, params.bloomThreshold);
const outputPass = new OutputPass();
composer.addPass(renderPass);
composer.addPass(bloomPass);
composer.addPass(outputPass);

const gui = new GUI({ title: effectTitle, width: 320 });

const rendererFolder = gui.addFolder("Renderer");
rendererFolder.add(params, "dpr", 0.5, 2, 0.25).onChange(resize);
rendererFolder.add(params, "exposure", 0.2, 2.4, 0.01).onChange(() => {
  renderer.toneMappingExposure = params.exposure;
});
rendererFolder.add(params, "paused");
rendererFolder.add(params, "autoRotate").onChange((value) => {
  controls.autoRotate = value;
});
rendererFolder.open();

const postFolder = gui.addFolder("Post");
postFolder.add(params, "bloomStrength", 0, 2, 0.01).onChange((value) => {
  bloomPass.strength = value;
});
postFolder.add(params, "bloomRadius", 0, 1, 0.01).onChange((value) => {
  bloomPass.radius = value;
});
postFolder.add(params, "bloomThreshold", 0, 1.2, 0.01).onChange((value) => {
  bloomPass.threshold = value;
});

const styleFolder = gui.addFolder("Style");
styleFolder.addColor(params, "background").onChange((value) => {
  scene.background.set(value);
  scene.fog.color.set(value);
});
styleFolder.addColor(params, "glow").onChange((value) => {
  uniforms.uColorA.value.set(value);
  glow.color.set(value);
});
styleFolder.addColor(params, "fill").onChange((value) => {
  uniforms.uColorB.value.set(value);
  fill.color.set(value);
});
styleFolder.add(params, "hueShift", -Math.PI, Math.PI, 0.01).onChange((value) => {
  uniforms.uHueShift.value = value;
});

const animationFolder = gui.addFolder("Animation");
animationFolder.add(params, "speed", 0, 3, 0.01);
animationFolder.add(params, "wobble", 0, 0.6, 0.01).onChange((value) => {
  uniforms.uWobble.value = value;
});
animationFolder.add(params, "wobbleScale", 0, 0.8, 0.01).onChange((value) => {
  uniforms.uWobbleScale.value = value;
});

window.addEventListener("pointermove", (event) => {
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
  uniforms.uPointer.value.copy(pointer);
});

window.addEventListener("resize", resize);

resize();
render();

function resize() {
  size.set(window.innerWidth, window.innerHeight);
  camera.aspect = size.x / Math.max(size.y, 1);
  camera.updateProjectionMatrix();

  renderer.setPixelRatio(Math.min(window.devicePixelRatio, params.dpr));
  renderer.setSize(size.x, size.y, false);
  composer.setSize(size.x, size.y);
  bloomPass.resolution.set(size.x, size.y);
}

function render() {
  requestAnimationFrame(render);

  const dt = clock.getDelta();
  if (!params.paused) {
    uniforms.uTime.value += dt * params.speed;
    mesh.rotation.y += dt * 0.25 * params.speed;
    mesh.rotation.x = Math.sin(uniforms.uTime.value * 0.35) * 0.18;
  }

  glow.position.x = 2.2 + pointer.x * 0.9;
  glow.position.y = 2.4 + pointer.y * 0.6;
  fill.position.x = -2.8 - pointer.x * 0.6;

  controls.update();
  composer.render();
}
