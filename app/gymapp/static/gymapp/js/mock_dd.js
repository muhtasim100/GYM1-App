document.addEventListener('DOMContentLoaded', () => {
    const leaderboardData = [
        { username: "Adam", deads: 200 },
        { username: "Baker", deads: 90 },
        { username: "Cindy", deads: 180 },
        { username: "Darren", deads: 220 },
        { username: "Emmanuel", deads: 70 },
        { username: "Farhad", deads: 60 },
        { username: "Gary", deads: 90 },
        { username: "Hamm", deads: 100 },
        { username: "Isabel", deads: 140 },
        { username: "Jaheim", deads: 70 },
        { username: "Kiren", deads: 110 },
        { username: "Luke", deads: 212.5 },
    ];
        // Sort the data by deadlift descending.
        leaderboardData.sort((a, b) => b.deads - a.deads);
    
        // Get the top 5 users.
        const topUsers = leaderboardData.slice(0, 5);
    
        // Loop through the top 5 users and populate the divs.
        topUsers.forEach((user, index) => {
            const userInfoDiv = document.getElementById(`user-rank-${index + 1}`);
            const userScoreDiv = document.getElementById(`user-score-${index + 1}`);
            
            userInfoDiv.textContent = `${index + 1}. ${user.username}`;
            userScoreDiv.textContent = user.deads;
    
            // Apply styling for the top user only.
            if (index === 0) { // Check if it's the top user.
                userInfoDiv.className += " top-user-info";
                userScoreDiv.className += " top-user-score";
            }
        });
    });