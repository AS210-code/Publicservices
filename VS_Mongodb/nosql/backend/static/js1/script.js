document.addEventListener("DOMContentLoaded", function() {
    let serviceDropdown = document.getElementById("service");
    let applyForm = document.getElementById("apply-form");
    let servicesList = document.getElementById("services-list");

    // Fetch available services and populate the list & dropdown
    fetch("/api/services")
    .then(response => response.json())
    .then(data => {
        let servicesList = document.getElementById("services-list");
        let serviceDropdown = document.getElementById("service");
        if (data.length > 0) {
            applyForm.style.display = "block";
            data.forEach(service => {
                let li = document.createElement("li");
                li.textContent = service.name;
                servicesList.appendChild(li);

                let option = document.createElement("option");
                option.value = service._id;
                option.textContent = service.name;
                serviceDropdown.appendChild(option);
            });
        } else {
            servicesList.innerHTML = "<p>No services available.</p>";
        }
    });

    // Handle form submission for service application
    applyForm.addEventListener("submit", function(event) {
        event.preventDefault();
        let selectedService = serviceDropdown.value;

        fetch("/api/apply-service", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ service_id: selectedService })
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error("Error:", error));
    });
});

