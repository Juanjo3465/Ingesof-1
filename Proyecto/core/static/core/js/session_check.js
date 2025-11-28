window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        fetch(window.SESSION_VERIFY_URL, {cache: 'no-cache'})
            .then(r => r.json())
            .then(data => {
                if (!data.authenticated) {
                    window.location.href = window.INITIAL_PAGE_URL;
                }
            });
    }
});