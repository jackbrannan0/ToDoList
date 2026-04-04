window.onload = function(){
                const mainForm = document.getElementById(mainForm)
                mainForm.onsubmit = function(event){
                    event.preventDefault();
                    fetch("/add", {
                        method: 'GET'
                    })
                    .then(response => {
                        
                    } )
                }
            }