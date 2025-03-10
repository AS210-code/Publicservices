document.addEventListener('DOMContentLoaded', function () {
    // Update session information in MongoDB via an API endpoint.
    // (This assumes a backend API exists at '/api/update_session' that handles the session update.)
    function updateSession() {
      fetch('/api/update_session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ lastVisited: new Date().toISOString() })
      })
        .then(response => response.json())
        .then(data => console.log('Session updated', data))
        .catch(err => console.error('Session update failed:', err));
    }
    updateSession();
  
    // Search functionality: redirect to a search results page with the query.
    document.getElementById('search-btn').addEventListener('click', function () {
      const query = document.getElementById('search-input').value;
      if (query.trim() !== '') {
        window.location.href = 'search.html?q=' + encodeURIComponent(query);
      }
    });
  });
  