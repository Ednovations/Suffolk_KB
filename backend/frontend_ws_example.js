// Example JS for frontend integration with backend WebSocket updates
// Add this to your main HTML/JS frontend
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = function(event) {
    if (event.data === 'update') {
        // Reload or re-fetch the knowledge base JSON
        fetch('/kb')
            .then(res => res.json())
            .then(data => {
                // Update your UI with new data
                updateKnowledgeBaseUI(data);
            });
    }
};
ws.onclose = function() {
    // Optionally, try to reconnect after a delay
    setTimeout(() => location.reload(), 3000);
};

function updateKnowledgeBaseUI(data) {
    // Implement this to update your dynamic content
    console.log('KB updated:', data);
}
