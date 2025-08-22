document.addEventListener('DOMContentLoaded', () => {
    // Get all necessary elements once to improve performance
    const form = document.getElementById('careerForm');
    const resultsBox = document.getElementById('results');

    // Add a submit event listener to the form
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent default form submission

        // Collect all form data
        const formData = new FormData(form);
        const userData = {};
        for (const [key, value] of formData.entries()) {
            userData[key] = value;
        }

        // Log data for professional debugging and backend prep
        console.log("Collected User Data:", userData);

        // Display a "Processing" message with an animation
        resultsBox.innerHTML = '<p class="text-center">Processing your request...</p>';
        resultsBox.classList.add('show-results');

        // Here, you would typically make a real API call
        
        setTimeout(() => {
            const mockResult = `Based on your interests in ${userData.interests}, skills in ${userData.skills}, and aptitudes in ${userData.aptitudes}, we recommend exploring a career in **Data Science** or **Software Engineering**.`;
            resultsBox.innerHTML = `
                <h4 class="text-center mb-3">Your Personalized Career Path</h4>
                <p>${mockResult}</p>
            `;
            resultsBox.classList.add('show-results');
        }, 2000); // Simulate a 2-second API call delay
    });
});
