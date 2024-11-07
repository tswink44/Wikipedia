// Wait for the DOM to be ready
document.getElementById("start-button").addEventListener("click", async function() {
    // Get the values from the input fields
    const startPage = document.getElementById("start").value;
    const targetPage = document.getElementById("target").value;

    try {
        // Send a GET request to the Flask server
        const response = await fetch(`/find_path?start=${encodeURIComponent(startPage)}&target=${encodeURIComponent(targetPage)}`);
        
        if (!response.ok) {
            // If the response is not OK (status code 2xx), display an error message
            document.getElementById("status").innerText = `Error: ${response.statusText}`;
            return;
        }

        // Parse the JSON response from the Flask server
        const data = await response.json();

        // If there is a valid path, display the result
        let result = "";
        if (data.path) {
            result = `Shortest path: ${data.path.join(' -> ')}<br>Click count: ${data.clicks}`;
        } else {
            result = data.message || "No path found.";
        }
        document.getElementById("status").innerHTML = result;

    } catch (error) {
        // If there was an error making the request, display an error message
        document.getElementById("status").innerText = `Error: ${error.message}`;
    }
});
