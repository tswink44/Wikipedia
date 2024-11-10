
document.getElementById("start-button").addEventListener("click", async function() {
    const startPage = document.getElementById("start").value;
    const targetPage = document.getElementById("target").value;

    try {
        const response = await fetch(`/find_path?start=${encodeURIComponent(startPage)}&target=${encodeURIComponent(targetPage)}`);
        
        if (!response.ok) {
            document.getElementById("status").innerText = `Error: ${response.statusText}`;
            return;
        }

        const data = await response.json();

        let result = "";
        if (data.path) {
            result = `Shortest path: ${data.path.join(' -> ')}<br>Click count: ${data.clicks}`;
        } else {
            result = data.message || "No path found.";
        }
        document.getElementById("status").innerHTML = result;

    } catch (error) {
        document.getElementById("status").innerText = `Error: ${error.message}`;
    }
});
