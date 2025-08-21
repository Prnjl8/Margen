document.getElementById('careerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Stop the form from submitting in the traditional way

    // Collect data from the form
    const interests = document.getElementById('interests').value;
    const skills = document.getElementById('skills').value;
    const aptitudes = document.getElementById('aptitudes').value;
    const education = document.getElementById('education').value;

    // Create a data object to send to the backend
    const userData = {
        interests: interests,
        skills: skills,
        aptitudes: aptitudes,
        education: education
    };

    // At this point, the data is ready! 
    // You will later use this `userData` object to make an API call to your backend.
    // For now, let's just log it to the console to see if it works.
    console.log("Collected User Data:", userData);

    // You can also display a simple message on the page.
    document.getElementById('results').innerHTML = `<p>Processing your request...</p>`;

    // **Next Step:** You will replace the console.log with a function that sends this data 
    // to your backend server, which will then interact with the Google Generative AI API.
    // This is part of the next phase.
});