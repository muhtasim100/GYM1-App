document.addEventListener('DOMContentLoaded', () => {
    const leaderboardData = [
        { username: "Adam", squat: 150 },
        { username: "Baker", squat: 90 },
        { username: "Cindy", squat: 180 },
        { username: "Darren", squat: 120 },
        { username: "Emmanuel", squat: 70 },
        { username: "Farhad", squat: 60 },
        { username: "Gary", squat: 90 },
        { username: "Hamm", squat: 100 },
        { username: "Isabel", squat: 140 },
        { username: "Jaheim", squat: 70 },
        { username: "Kiren", squat: 110 },
        { username: "Luke", squat: 200 },
    ];
        // Sort the data by squat descending.
        leaderboardData.sort((a, b) => b.squat - a.squat);
    
        // Get the top 5 users.
        const topUsers = leaderboardData.slice(0, 5);
    
        // Loop through the top 5 users and populate the divs.
        topUsers.forEach((user, index) => {
            const userInfoDiv = document.getElementById(`user-rank-${index + 1}`);
            const userScoreDiv = document.getElementById(`user-score-${index + 1}`);
            
            userInfoDiv.textContent = `${index + 1}. ${user.username}`;
            userScoreDiv.textContent = user.squat;
    
            // Apply styling for the top user only.
            if (index === 0) { // Check if it's the top user.
                userInfoDiv.className += " top-user-info";
                userScoreDiv.className += " top-user-score";
            }
        });
    });