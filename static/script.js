document.addEventListener('DOMContentLoaded', () => {
    // Function to get all songs from the API
    const getSongs = async () => {
        const response = await fetch('/songs');
        const songs = await response.json();
        renderSongs(songs);
    };

    // Function to render the list of songs
    const renderSongs = (songs) => {
        const songList = document.getElementById('songs');
        songList.innerHTML = ''; // Clear existing songs

        songs.forEach(song => {
            const trackNameWithPlus = song.track_name.replace(/ /g, '+');
            const artistNameWithPlus = song["artist(s)_name"].replace(/ /g, '+');
            const a = document.createElement('a');
            a.href = `https://www.youtube.com/results?search_query=${trackNameWithPlus}+${artistNameWithPlus}`;
            a.innerHTML = "LINK"
            a.style.textAlign = 'right';
            a.style.display = 'block';

            const li = document.createElement('li');
            li.innerHTML = `${song.track_name} - ${song['artist(s)_name']}`;
            li.onclick = () => fetchRecommendations(song.track_name, song['artist(s)_name'], li);

            li.appendChild(a);
            songList.appendChild(li);
        });
    };

    // Function to fetch recommendations based on the selected song
    const fetchRecommendations = async (trackName, artistName, songElement) => {
        console.log('Track Name:', trackName);
        console.log('Artist Name:', artistName);
        if (!trackName || !artistName) {
            console.error("Track name or artist name is missing");
            return;
        }
        // Check if recommendations are already rendered (toggle behavior)
        const existingRecommendations = songElement.querySelector('ul');
        if (existingRecommendations) {
            // If recommendations already exist, remove them
            existingRecommendations.remove();
            return; // Exit the function
        }

        try {
            const response = await fetch('/recommendations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    artist_name: artistName,
                    song_name: trackName
                }),
            });
    
            // Check if the response was successful (status code 200)
            if (!response.ok) {
                throw new Error('Failed to fetch recommendations');
            }
    
            // Parse the JSON response
            const recommendations = await response.json();
    
            // Render the recommendations directly under the clicked song
            renderRecommendations(recommendations, songElement);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    // Function to render recommended songs under the clicked song
    const renderRecommendations = (recommendations, songElement) => {
        // Check if recommendations already exist under this song
        const existingRecommendations = songElement.querySelector('ul');
        
        if (existingRecommendations) {
            // If recommendations already exist, do not append them again
            return;
        }

        // Create a new list for recommendations
        const recommendationsList = document.createElement('ul');

        
        recommendations.forEach(song => {
            const trackNameWithPlus = song.track_name.replace(/ /g, '+');
            const artistNameWithPlus = song["artist(s)_name"].replace(/ /g, '+');
            const a = document.createElement('a');
            a.href = `https://www.youtube.com/results?search_query=${trackNameWithPlus}+${artistNameWithPlus}d`;
            a.innerHTML = "LINK"
            a.style.textAlign = 'right';
            a.style.display = 'block';

            const li = document.createElement('li');
            li.innerHTML = `${song.track_name} - ${song['artist(s)_name']}`;

            li.appendChild(a);

            recommendationsList.appendChild(li);
        });

        // Append the recommendations list directly under the clicked song
        songElement.appendChild(recommendationsList);
    };

    // Load songs when the page loads
    getSongs();
});
