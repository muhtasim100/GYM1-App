document.addEventListener('DOMContentLoaded', () => {
    const leaderboardData = [
        { username: "Adam", bench: 130 },
        { username: "Baker", bench: 90 },
        { username: "Cindy", bench: 45 },
        { username: "Darren", bench: 120 },
        { username: "Emmanuel", bench: 100 },
        { username: "Farhad", bench: 75 },
        { username: "Gary", bench: 60 },
        { username: "Hamm", bench: 60 },
        { username: "Isabel", bench: 40 },
        { username: "Jaheim", bench: 55 },
        { username: "Kiren", bench: 60 },
        { username: "Luke", bench: 60 },
    ];
        // Sort the data by benchpress descending.
        leaderboardData.sort((a, b) => b.bench - a.bench);
    
        // Get the top 5 users.
        const topUsers = leaderboardData.slice(0, 5);
    
        // Loop through the top 5 users and populate the divs.
        topUsers.forEach((user, index) => {
            const userInfoDiv = document.getElementById(`user-rank-${index + 1}`);
            const userScoreDiv = document.getElementById(`user-score-${index + 1}`);
            
            userInfoDiv.textContent = `${index + 1}. ${user.username}`;
            userScoreDiv.textContent = user.bench;
    
            // Apply styling for the top user only.
            if (index === 0) { // Check if it's the top user.
                userInfoDiv.className += " top-user-info";
                userScoreDiv.className += " top-user-score";
            }
        });
    });