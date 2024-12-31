import pandas as pd
from Logs.logging_config import setup_logger

# Set up logger
logger = setup_logger(__name__, 'data_preprocessor.log')

class Extractor():
    """
    A class to extract data from csv files.
    """

    def get_df(self, path="./database/Spotify_Most_Streamed_Songs.csv"):
        """
        Returns fully and cleaned dataset.
        """
        df = pd.read_csv(path)
        df = self.clean_df(df)
        logger.info("Succesfully loaded dataset")
        return df

    def get_preprocessed_df(self, path="./database/clustered_songs.csv"):
        """
        Returns preprocessed dataset.
        """
        df = pd.read_csv(path)
        df = df.drop("clusters",axis=1)
        logger.info("Succesfully loaded dataset preprocessed")
        return df

    def get_clustered_df(self, path="./database/clustered_songs.csv"):
        """
        Returns clustered dataset.
        """
        df = pd.read_csv(path)
        logger.info("Succesfully loaded dataset clustered")
        return df

    def get_all_songs(self):
        """
        Returns all songs from dataset.
        """
        columns = ["artist(s)_name", "track_name", "cover_url"]
        df = self.get_df()
        
        # Convert the DataFrame to a list of dictionaries (records)
        songs = df[columns].to_dict(orient='records')
        logger.info("Succesfully returned all songs")
        return songs

    def get_song_from_id(self, id):
        """
        Return songs based on their id.
        """
        df = self.get_df()
        print(f"ID:{id}, DF:{len(df)}")

        if(id > len(df) or id < 0):
            logger.error("Index out of bounds exception")
        else:
            return df.iloc[id]
    
    def clean_df(self,df):
        """
        Clean dataset from wrong values.
        """
        wrong_value = 'BPM110KeyAModeMajorDanceability53Valence75Energy69Acousticness7Instrumentalness0Liveness17Speechiness3'

        copy = df.copy()
        df_minus = copy[copy['streams'] != wrong_value].reset_index(drop=True)
        df_minus["streams"] = df_minus["streams"].astype("int")
        mean_streams = str(df_minus["streams"].median())

        df.loc[df['streams'] == wrong_value, 'streams'] = mean_streams
        df["streams"] = df["streams"].astype("float").astype("int")
        logger.info("Succesfully cleaned dataset")
        return df
        
    def get_song_by_artist_and_name(self, artist_name: str, song_name: str):
        """
        Retrieve a song from the DataFrame based on artist name and song name.
        """
        df = self.get_df()  # Get the full DataFrame without filtering columns
        
        # Filter the DataFrame based on the provided artist name and song name
        filtered_song = df[
            (df["artist(s)_name"].str.lower() == artist_name.lower()) &
            (df["track_name"].str.lower() == song_name.lower())
        ]

        # Check if any matching rows exist
        if filtered_song.empty:
            return None  # No matching song found
        else:
            return filtered_song.iloc[0]


                        