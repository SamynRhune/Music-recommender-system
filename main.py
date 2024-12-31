from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from pydantic import BaseModel
import os
from fastapi import Request
from Modules.data_extractor import Extractor
from Modules.data_preprocessor import Preprocessor
from Modules.forecaster import Forecaster

# Setup Jinja2 Templates
templates = Jinja2Templates(directory="templates")

data_extractor = Extractor()
data_preprocessor = Preprocessor(data_extractor.get_df())
agglo_model = Forecaster()

app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Request and response models
class Song(BaseModel):
    artists_name: str = Field(..., alias="artist(s)_name")
    track_name: str
    cover_url: str

class RecommendationRequest(BaseModel):
    artist_name: str
    song_name:str

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    # Get all songs from the database
    songs = data_extractor.get_all_songs()
    
    # Render index.html with the songs data
    return templates.TemplateResponse("index.html", {"request": request, "songs": songs})

@app.get("/songs", response_model=List[Song])
def list_songs():
    """Get the list of all songs."""
    
    
    return data_extractor.get_all_songs()
    #return FileResponse(os.path.join("static", "index.html"))

@app.post("/recommendations", response_model=List[Song])
def recommend_songs(request: RecommendationRequest):
    full_song = data_extractor.get_song_by_artist_and_name(request.artist_name,request.song_name)
    print(f"FULL SONG {full_song}")
    ml_song = data_preprocessor.song_preprocessing(full_song)
    return_song = agglo_model.get_prediction(ml_song,3,data_extractor.get_preprocessed_df(),data_extractor.get_clustered_df())
    
    #get_artist_from_preprocessed(return_song)
    
    recommended_songs = []
    for _, this_song in return_song.iterrows():
        # Get the index of the current row
        song_id = this_song.name  # Access the row index, not the method
        
        # Call the function to get the song by ID
        current_song = data_extractor.get_song_from_id(song_id)
        
        # Process current_song as before
        response = {
            "artist(s)_name": current_song["artist(s)_name"],
            "track_name": current_song["track_name"],
            "cover_url": current_song["cover_url"]
        }
        recommended_songs.append(response)

    print(recommended_songs)

    return recommended_songs

