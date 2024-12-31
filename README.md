# Spotify Agglomerative Clustering Website

This repository hosts a website that serves an agglomerative clustering model. The model predicts 3 possible songs you might like based on the song you select. The model is trained on the "Spotify Most Streamed Songs" dataset.

## Features

Agglomerative Clustering: Provides song recommendations using a clustering-based approach.

Interactive Website: Allows users to explore and select songs directly through the browser.

## Setup Instructions

### Step 1: Clone the Repository

First, clone this repository to your local machine:
```bash
git clone https://github.com/SamynRhune/Music-recommender-system.git
cd Music-recommender-system
```

### Step 2: Build the Docker Image

Build the Docker image using the following command:
```bash
docker build -t fastapi-app .
```

### Step 3: Run the Docker Container

Run a container from the built image:
```bash
docker run -p 8000:8000 fastapi-app:latest
```

### Step 4: Access the Website

Open your web browser and navigate to:
```bash
127.0.0.1:8000
```

## Dataset

The model is trained on the Spotify Most Streamed Songs dataset. This dataset includes a wide variety of popular songs, making the predictions relevant and engaging for users.

## Notes

Ensure Docker is installed and running on your machine before executing the commands.

For further customization or model retraining, you can modify the source code as needed.

Enjoy exploring your music preferences!
