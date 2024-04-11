document.addEventListener('DOMContentLoaded', () => {
    const leaderboardData = [
        { username: "A", attendance: 12 },
        { username: "B", attendance: 9 },
        { username: "C", attendance: 15 },
        { username: "D", attendance: 12 },
        { username: "E", attendance: 9 },
        { username: "F", attendance: 15 },
        { username: "G", attendance: 12 },
        { username: "H", attendance: 10 },
        { username: "I", attendance: 1 },
        { username: "J", attendance: 2 },
        { username: "K", attendance: 8 },
        { username: "L", attendance: 20 },
    ];
        // Sort the data by attendance descending.
        leaderboardData.sort((a, b) => b.attendance - a.attendance);
    
        // Get the top 5 users.
        const topUsers = leaderboardData.slice(0, 5);
    
        // Loop through the top 5 users and populate the divs.
        topUsers.forEach((user, index) => {
            document.getElementById(`user-rank-${index + 1}`).textContent =`${index + 1}. ${user.username}`;
            document.getElementById(`user-score-${index + 1}`).textContent = user.attendance;
        });
    });
    