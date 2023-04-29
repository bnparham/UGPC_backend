
// Set the countdown end date and time
const countdownDate = new Date("2023-05-11T00:00:00Z").getTime();

// Update the countdown timer every 1 second
const countdownInterval = setInterval(() => {
    // Get the current date and time
    const now = new Date().getTime();

    // Calculate the time remaining until the countdown end date and time
    const timeRemaining = countdownDate - now;

    // Calculate the days, hours, minutes, and seconds remaining
    const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

    // Display the countdown timer
    document.getElementById("days").textContent = `${days.toString().padStart(2, "0")}`;
    document.getElementById("hours").textContent = `${hours.toString().padStart(2, "0")}`;
    document.getElementById("minutes").textContent = `${minutes.toString().padStart(2, "0")}`;
    document.getElementById("seconds").textContent = `${seconds.toString().padStart(2, "0")}`;

    // Check if the countdown has ended
    if (timeRemaining <= 0) {
    clearInterval(countdownInterval);
    document.getElementById("timer").textContent = "Countdown Ended";
    }
}, 1000); // Update the countdown timer every 1 second