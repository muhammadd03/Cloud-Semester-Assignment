import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

document.addEventListener('DOMContentLoaded', () => {
    // Set up the scene, camera, and renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

    const renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setClearColor(0x041204); // Set background color to white

    // Append renderer to the correct div
    const container = document.querySelector('.hero-model');
    if (!container) {
        console.error('Could not find .hero-model element');
        return;
    }
    container.appendChild(renderer.domElement);

    // Set the canvas styles
    const canvas = renderer.domElement;
    canvas.style.display = 'block';
    canvas.style.width = '604px';
    canvas.style.height = '249px';

    camera.position.z = 5;

    // Add OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Enable damping (inertia)
    controls.dampingFactor = 0.25; // Damping factor

    // Variable to store the loaded model
    let model;

    // Load the GLTF model
    const loader = new GLTFLoader();
    loader.load('/static/myapp/models/scene.gltf', function (gltf) {
        model = gltf.scene;

        // Adjust model properties
        model.scale.set(40, 40, 40); // Increase the scale of the model
        model.position.set(0, -1, 0); // Position the model in the scene
        model.rotation.y = Math.PI / 2; // Rotate the model if needed

        scene.add(model);
    }, undefined, function (error) {
        console.error(error);
    });

    // Resize the renderer and update the camera aspect ratio
    function resizeRenderer() {
        const width = container.clientWidth;
        const height = container.clientHeight;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    }

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);

        // Rotate the model if it has been loaded and not being controlled by the user
        if (model && !controls.isDragging) {
            model.rotation.y += 0.01; // Adjust the rotation speed as needed
        }

        controls.update();
        renderer.render(scene, camera);
    }

    // Start the animation loop
    animate();

    // Adjust the scene and camera on window resize
    window.addEventListener('resize', resizeRenderer);
    resizeRenderer(); // Initial resize to fit the container
});
