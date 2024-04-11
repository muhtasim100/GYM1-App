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
    
    const leaderboardContainer = document.querySelector('.leaderboard-container');
    leaderboardData.sort((a, b) => b.attendance - a.attendance); 

    leaderboardData.forEach((user, index) => {
        const leaderboardRow = document.createElement('div');
        leaderboardRow.className = 'leaderboard-row leaderboard-card'; // Use both classes
        
        const userInfo = document.createElement('div');
        userInfo.className = 'user-info';
        userInfo.innerHTML = `<strong>${index + 1}. ${user.username}</strong>`;
        
        const userScore = document.createElement('div');
        userScore.className = 'user-score';
        userScore.textContent = user.attendance;
        
        leaderboardRow.appendChild(userInfo);
        leaderboardRow.appendChild(userScore);
        
        leaderboardContainer.appendChild(leaderboardRow);
    });
});