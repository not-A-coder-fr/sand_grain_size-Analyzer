// --- DOM Element References ---
const video = document.getElementById("video");
const snapBtn = document.getElementById("snapBtn");
const capturedImage = document.getElementById("capturedImage");
const processedImage = document.getElementById("processedImage");
const analyzeBtn = document.getElementById("analyzeBtn");
const downloadBtn = document.getElementById("downloadBtn");
const darkModeToggle = document.getElementById("darkModeToggle");
const statusEl = document.querySelector(".status");
const API_BASE = "http://localhost:5000"; // Change to your Pi's IP if remote

/**
 * Requests and starts the webcam stream.
 */
function startWebcam() {
    statusEl.textContent = "Initializing camera...";
    
    // Check if the browser supports media devices API
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
                statusEl.textContent = "Camera ready! Tap 'Take Snapshot' to capture.";
                snapBtn.disabled = false;
                console.log("Webcam stream started successfully.");
            })
            .catch(error => {
                console.error("Camera access error: ", error);
                statusEl.textContent = "Error: Camera access denied. Check permissions.";
                statusEl.style.color = "var(--primary-color)";
                snapBtn.disabled = true;
            });
    } else {
        statusEl.textContent = "Error: Browser doesn't support webcam access.";
        statusEl.style.color = "var(--primary-color)";
        snapBtn.disabled = true;
    }
}

/**
 * Captures a single frame from the video stream and sends to backend for analysis.
 */
async function takeSnapshot() {
    statusEl.textContent = "Capturing image...";
    snapBtn.disabled = true;
    
    // Set canvas dimensions to match the video
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw the video frame onto the canvas
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas data to Blob
    canvas.toBlob(async (blob) => {
        try {
            // Send image to backend for analysis
            const formData = new FormData();
            formData.append("image", blob, "snapshot.jpg");
            
            const response = await fetch(`${API_BASE}/capture`, {
                method: "POST",
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Update UI with results
                capturedImage.src = URL.createObjectURL(blob);
                capturedImage.style.display = "block";
                processedImage.src = `/images/${data.image}`;
                processedImage.style.display = "block";
                
                // Update data table
                document.getElementById("grainCount").textContent = data.result.count;
                document.getElementById("avgSize").textContent = data.result.avg_size_mm;
                document.getElementById("stdDev").textContent = data.result.std_dev_mm;
                document.getElementById("latitude").textContent = data.result.lat;
                document.getElementById("longitude").textContent = data.result.lon;
                document.getElementById("timestamp").textContent = data.result.timestamp;
                
                statusEl.textContent = `Analysis complete! ${data.result.count} grains detected.`;
                statusEl.style.color = "var(--primary-color)";
                analyzeBtn.disabled = true;
                downloadBtn.disabled = false;
            } else {
                throw new Error(data.error || "Unknown error");
            }
        } catch (error) {
            console.error("Analysis error:", error);
            statusEl.textContent = `Error: ${error.message}`;
            statusEl.style.color = "var(--primary-color)";
        } finally {
            snapBtn.disabled = false;
        }
    }, "image/jpeg");
}

/**
 * Downloads the analysis results as CSV.
 */
function downloadData() {
    statusEl.textContent = "Preparing download...";
    
    try {
        // Get current results
        const results = {
            grainCount: document.getElementById("grainCount").textContent,
            avgSize: document.getElementById("avgSize").textContent,
            stdDev: document.getElementById("stdDev").textContent,
            latitude: document.getElementById("latitude").textContent,
            longitude: document.getElementById("longitude").textContent,
            timestamp: document.getElementById("timestamp").textContent
        };
        
        // Create CSV
        let csv = "Metric,Value\n";
        csv += `Grain Count,${results.grainCount}\n`;
        csv += `Avg Size (mm),${results.avgSize}\n`;
        csv += `Std Dev (mm),${results.stdDev}\n`;
        csv += `Latitude,${results.latitude}\n`;
        csv += `Longitude,${results.longitude}\n`;
        csv += `Timestamp,${results.timestamp}\n`;
        
        // Download
        const blob = new Blob([csv], { type: "text/csv" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `shore_scan_${new Date().toISOString().replace(/[:.]/g, "-")}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        statusEl.textContent = "Data downloaded successfully!";
        statusEl.style.color = "var(--primary-color)";
    } catch (error) {
        console.error("Download error:", error);
        statusEl.textContent = `Download error: ${error.message}`;
        statusEl.style.color = "var(--primary-color)";
    }
}

// --- Dark Mode Toggle ---
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("darkMode", document.body.classList.contains("dark-mode"));
}

// --- Event Listeners and Initial Setup ---
snapBtn.addEventListener("click", takeSnapshot);
analyzeBtn.addEventListener("click", takeSnapshot);
downloadBtn.addEventListener("click", downloadData);
darkModeToggle.addEventListener("change", toggleDarkMode);

document.addEventListener("DOMContentLoaded", () => {
    // Check for and apply saved dark mode preference on page load
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
        darkModeToggle.checked = true;
    }
    
    // Start the webcam once the page is fully loaded
    startWebcam();
});