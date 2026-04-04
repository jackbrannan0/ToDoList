document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            // 1. Stop the browser from doing its own thing
            e.preventDefault();
            
            const formData = new FormData(this);
            const route = this.action;

            try {
                // 2. Send the request to Flask in the background
                const response = await fetch(route, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    // 3. SUCCESS! Now we reload to show the new Jinja2 data
                    window.location.reload(); 
                } else {
                    console.error("Server responded with an error.");
                }
            }
            catch (err) {
                console.error("Connection error:", err);
            }
        });
    });
});