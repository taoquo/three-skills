import * as THREE from 'three/webgpu';
import { vec3, Fn, time, texture3D, screenUV, uniform, screenCoordinate, pass, color, uv, mix, sin } from 'three/tsl';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { ImprovedNoise } from 'three/addons/math/ImprovedNoise.js';
import { bayer16 } from 'three/addons/tsl/math/Bayer.js';
import { gaussianBlur } from 'three/addons/tsl/display/GaussianBlurNode.js';
import { TeapotGeometry } from 'three/addons/geometries/TeapotGeometry.js';
import { GUI } from 'lil-gui';

const effectTitle = 'Volumetric Lighting (Froxel-based)';
const canvas = document.getElementById('app');
const status = document.getElementById('status');
const size = new THREE.Vector2();
window.__REPLICATOR_STARTER_BOOTED__ = true;

const params = {
  dpr: Math.min(window.devicePixelRatio, 2),
  exposure: 2.0,
  speed: 1.0,
  paused: false,
  autoRotate: false,
  smokeAmount: 2,
  lightIntensity: 3,
  spotIntensity: 100,
  fogIntensity: 1,
  resolution: 0.25,
  denoiseStrength: 0.6,
  denoise: true,
  steps: 12,
  background: '#050608',
};

const scene = new THREE.Scene();
scene.background = new THREE.Color(params.background);

const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 100);
camera.position.set(-8, 1, -6);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.enablePan = false;
controls.enableZoom = true;
controls.maxDistance = 40;
controls.minDistance = 2;

let renderer, volumetricMesh, teapot, pointLight, spotLight, renderPipeline;
let volumetricLightingIntensity, smokeAmountUniform, denoiseStrengthUniform;

function createTexture3D() {
  let i = 0;
  const size = 128;
  const data = new Uint8Array(size * size * size);
  const scale = 10;
  const perlin = new ImprovedNoise();
  const repeatFactor = 5.0;

  for (let z = 0; z < size; z++) {
    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        const nx = (x / size) * repeatFactor;
        const ny = (y / size) * repeatFactor;
        const nz = (z / size) * repeatFactor;
        const noiseValue = perlin.noise(nx * scale, ny * scale, nz * scale);
        data[i] = 128 + 128 * noiseValue;
        i++;
      }
    }
  }

  const texture = new THREE.Data3DTexture(data, size, size, size);
  texture.format = THREE.RedFormat;
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.unpackAlignment = 1;
  texture.needsUpdate = true;
  return texture;
}

function setStatus(message, isError = false) {
  status.textContent = message;
  status.style.display = 'block';
  status.style.borderColor = isError ? 'rgba(248, 113, 113, 0.35)' : 'rgba(103, 232, 249, 0.22)';
}

function clearStatus() {
  status.style.display = 'none';
  window.__REPLICATOR_STARTER_RENDERER_READY__ = true;
}

function withInitTimeout(promise, label, timeoutMs = 4000) {
  let timer;
  const timeoutPromise = new Promise((_, reject) => {
    timer = window.setTimeout(() => {
      reject(new Error(`${label} timed out after ${timeoutMs}ms`));
    }, timeoutMs);
  });
  return Promise.race([promise, timeoutPromise]).finally(() => {
    window.clearTimeout(timer);
  });
}

function resize() {
  size.set(window.innerWidth, window.innerHeight);
  camera.aspect = size.x / Math.max(size.y, 1);
  camera.updateProjectionMatrix();
  if (!renderer) return;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, params.dpr));
  renderer.setSize(size.x, size.y, false);
}

async function init() {
  try {
    setStatus('Initializing WebGPU renderer...');
    renderer = new THREE.WebGPURenderer({
      canvas,
      antialias: true,
      alpha: false,
      powerPreference: 'high-performance',
    });
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.NeutralToneMapping;
    renderer.toneMappingExposure = params.exposure;
    renderer.shadowMap.enabled = true;
    await withInitTimeout(renderer.init(), 'WebGPU renderer init');

    // Volumetric Fog Area
    const LAYER_VOLUMETRIC_LIGHTING = 10;
    const noiseTexture3D = createTexture3D();

    smokeAmountUniform = uniform(params.smokeAmount);
    volumetricLightingIntensity = uniform(params.fogIntensity);
    denoiseStrengthUniform = uniform(params.denoiseStrength);

    const volumetricMaterial = new THREE.VolumeNodeMaterial();
    volumetricMaterial.steps = params.steps;
    volumetricMaterial.offsetNode = bayer16(screenCoordinate);
    volumetricMaterial.scatteringNode = Fn(({ positionRay }) => {
      const timeScaled = vec3(time, 0, time.mul(0.3));
      const sampleGrain = (scale, timeScale = 1) => texture3D(noiseTexture3D, positionRay.add(timeScaled.mul(timeScale)).mul(scale).mod(1), 0).r.add(0.5);
      let density = sampleGrain(0.1);
      density = density.mul(sampleGrain(0.05, 1));
      density = density.mul(sampleGrain(0.02, 2));
      return smokeAmountUniform.mix(1, density);
    });

    volumetricMesh = new THREE.Mesh(new THREE.BoxGeometry(20, 10, 20), volumetricMaterial);
    volumetricMesh.receiveShadow = true;
    volumetricMesh.position.y = 2;
    volumetricMesh.layers.disableAll();
    volumetricMesh.layers.enable(LAYER_VOLUMETRIC_LIGHTING);
    scene.add(volumetricMesh);

    // Objects
    teapot = new THREE.Mesh(
      new TeapotGeometry(0.8, 18),
      new THREE.MeshStandardMaterial({ color: 0xffffff, side: THREE.DoubleSide })
    );
    teapot.castShadow = true;
    scene.add(teapot);

    const floor = new THREE.Mesh(
      new THREE.PlaneGeometry(100, 100),
      new THREE.MeshStandardMaterial({ color: 0xffffff })
    );
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = -3;
    floor.receiveShadow = true;
    scene.add(floor);

    // Lights
    pointLight = new THREE.PointLight(0xf9bb50, params.lightIntensity, 100);
    pointLight.castShadow = true;
    pointLight.position.set(0, 1.4, 0);
    pointLight.layers.enable(LAYER_VOLUMETRIC_LIGHTING);
    scene.add(pointLight);

    spotLight = new THREE.SpotLight(0xffffff, params.spotIntensity);
    spotLight.position.set(2.5, 5, 2.5);
    spotLight.angle = Math.PI / 6;
    spotLight.penumbra = 1;
    spotLight.decay = 2;
    spotLight.distance = 0;
    spotLight.castShadow = true;
    spotLight.shadow.intensity = 0.98;
    spotLight.shadow.mapSize.width = 1024;
    spotLight.shadow.mapSize.height = 1024;
    spotLight.shadow.camera.near = 1;
    spotLight.shadow.camera.far = 15;
    spotLight.shadow.focus = 1;
    spotLight.layers.enable(LAYER_VOLUMETRIC_LIGHTING);
    scene.add(spotLight);

    // Post-Processing
    // Temporary replacement for RenderPipeline - direct rendering
    renderPipeline = {
      outputNode: null,
      render: () => renderer.render(scene, camera)
    };
    const volumetricLayer = new THREE.Layers();
    volumetricLayer.disableAll();
    volumetricLayer.enable(LAYER_VOLUMETRIC_LIGHTING);

    // Scene Pass
    const scenePass = pass(scene, camera);
    const sceneDepth = scenePass.getTextureNode('depth');
    volumetricMaterial.depthNode = sceneDepth.sample(screenUV);

    // Volumetric Lighting Pass
    const volumetricPass = pass(scene, camera, { depthBuffer: false });
    volumetricPass.name = 'Volumetric Lighting';
    volumetricPass.setLayers(volumetricLayer);
    // volumetricPass.setResolutionScale(params.resolution); // Method not available in current version

    // Compose and Denoise
    const blurredVolumetricPass = gaussianBlur(volumetricPass, denoiseStrengthUniform);
    const scenePassColor = scenePass.add(blurredVolumetricPass.mul(volumetricLightingIntensity));
    renderPipeline.outputNode = scenePassColor;

    // GUI
    const gui = new GUI({ title: effectTitle, width: 320 });
    const rendererFolder = gui.addFolder('Renderer');
    rendererFolder.add(params, 'dpr', 0.5, 2, 0.25).onChange(resize);
    rendererFolder.add(params, 'exposure', 0.2, 2.4, 0.01).onChange(() => {
      renderer.toneMappingExposure = params.exposure;
    });
    rendererFolder.add(params, 'paused');
    rendererFolder.add(params, 'autoRotate').onChange((value) => {
      controls.autoRotate = value;
    });
    rendererFolder.open();

    const styleFolder = gui.addFolder('Style');
    styleFolder.add(params, 'smokeAmount', 0, 3, 0.01).onChange((value) => {
      smokeAmountUniform.value = value;
    });
    styleFolder.add(params, 'fogIntensity', 0, 2, 0.01).onChange((value) => {
      volumetricLightingIntensity.value = value;
    });
    styleFolder.addColor(params, 'background').onChange((value) => {
      scene.background.set(value);
    });

    const raymarchFolder = gui.addFolder('Raymarch');
    raymarchFolder.add(params, 'resolution', 0.1, 1, 0.01).onChange((value) => {
      volumetricPass.setResolutionScale(value);
    });
    raymarchFolder.add(params, 'steps', 2, 16, 1).onChange((value) => {
      volumetricMaterial.steps = value;
    });
    raymarchFolder.add(params, 'denoiseStrength', 0, 1, 0.01).onChange((value) => {
      denoiseStrengthUniform.value = value;
    });
    raymarchFolder.add(params, 'denoise').onChange((value) => {
      const volumetric = value ? blurredVolumetricPass : volumetricPass;
      const scenePassColor = scenePass.add(volumetric.mul(volumetricLightingIntensity));
    // renderPipeline.outputNode = scenePassColor; // Disabled for now
      renderPipeline.needsUpdate = true;
    });

    const lightingFolder = gui.addFolder('Lighting');
    lightingFolder.add(pointLight, 'intensity', 0, 6, 0.1).onChange((value) => {
      params.lightIntensity = value;
    });
    lightingFolder.add(spotLight, 'intensity', 0, 200, 1).onChange((value) => {
      params.spotIntensity = value;
    });

    const animationFolder = gui.addFolder('Animation');
    animationFolder.add(params, 'speed', 0, 3, 0.01);

    window.addEventListener('resize', resize);
    resize();
    clearStatus();
    render();
  } catch (error) {
    window.__REPLICATOR_STARTER_RENDERER_READY__ = false;
    console.error(error);
    setStatus(
      `WebGPU starter failed to initialize. Try the WebGL2 fallback template or a raw shader path if this browser or environment cannot create the required GPU context. ${error.message ?? ''}`.trim(),
      true
    );
  }
}

function render(now = 0) {
  requestAnimationFrame(render);
  if (!renderer || !renderPipeline) return;

  if (!params.paused) {
    const t = now * 0.001 * params.speed;
    const scale = 2.4;
    pointLight.position.x = Math.sin(t * 0.7) * scale;
    pointLight.position.y = Math.cos(t * 0.5) * scale;
    pointLight.position.z = Math.cos(t * 0.3) * scale;
    spotLight.position.x = Math.cos(t * 0.3) * scale;
    spotLight.lookAt(0, 0, 0);
    teapot.rotation.y = t * 0.2;
  }

  controls.update();
  renderPipeline.render();
}

init();