     // Get the CSRF token from the form
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Get references to DOM elements
    const categoryCreateUrl = document.getElementById('category-create-url').getAttribute('data-url');
    const categoryList=document.getElementById('category-list').getAttribute('data-url');
    const button = document.getElementById('btn-registro');
    const name1 = document.getElementById("name");
    const desc = document.getElementById('desc');

    // Add an event listener to the registration button
    button.addEventListener("click", (e) => {
        // Prevent the default form submission
        e.preventDefault();
        // Create a FormData object with the form data
        const formData = new FormData();
        formData.append('name', name1.value);
        formData.append('desc', desc.value);

        // If the name field is empty, show an alert
        if (name1.value === "") {
            return Swal.fire('Please enter the category name');
        }
        // Display a confirmation dialog to the user
        Swal.fire({
            icon: 'question',
            title: 'Are you sure?',
            text: `Do you want to register the category "${name1.value}"?`,
            showCancelButton: true,
            confirmButtonText: 'Yes, register it!',
            cancelButtonText: 'No, cancel',
        }).then(result => {
            // The "result" object contains the user's response (confirmation or cancellation)
            console.log(result);
            if (result.isConfirmed) {
                // Create the URL for the AJAX endpoint (replace with your actual URL)
                const url=categoryCreateUrl;
                // Perform an AJAX request to register the category
                fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {
                    'X-CSRFToken': csrfToken, // Include the csrf_token in the header
                    }
                }).then(response => response.json())
                  .then(data => {
                    console.log(data)
                    if (data.Error === "Category exixsts already") {
                        // The category already exists, show an error alert
                        Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Category exists already'
                        });
                    }else{  
                        // The category has been successfully registered, show a success message
                        Swal.fire({
                        icon: 'success',
                        title: 'Success!',
                        text: `The category "${data.name}" has been registered successfully!`,
                        }).then((result) => {
                        // Redirect to the category list page
                            if(result.isConfirmed){
                                window.location.href = categoryList;
                            }
                        });
                        }
                    })
                    .catch(error => {
                    console.log("Error:", error);
                });
                }
            });
        });

