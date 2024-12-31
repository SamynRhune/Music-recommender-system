from sklearn.preprocessing import OneHotEncoder,LabelEncoder,MinMaxScaler
import pandas as pd
from Logs.logging_config import setup_logger

# Set up logger
logger = setup_logger(__name__, 'data_preprocessor.log')

class Preprocessor():

    def __init__(self,dataframe):
        """
        Initializes the Preprocessor class by deleting unnecessary columns,
        applying one-hot encoding, label encoding, and min-max scaling to the dataframe.
        """
        #deleting unnessesary columns
        dataframe = self.pre_delete_columns(dataframe)
        logger.info("Data preprocessor initializing: deleted columns 25% ")


        #fit_transform one hot encoder
        categorical_columns = ["key", "mode"]
        self.one_hot_encoder = OneHotEncoder()
        one_hot_encoded = self.one_hot_encoder.fit_transform(dataframe[categorical_columns])
        dataframe = self.clean_after_one_hot_encoding(dataframe, one_hot_encoded, categorical_columns)
        logger.info("Data preprocessor initializing: initialized one hot encoder 50%")
        

        #fit_transform label encoder
        label_columns = ["main_artist"]
        dataframe = self.set_only_first_artist(dataframe)
        self.label_encoder = LabelEncoder()
        dataframe["main_artist"] = self.label_encoder.fit_transform(dataframe[label_columns])
        logger.info("Data preprocessor initializing: initialized label encoder 75%")
        logger.info(f"Dataframe shape: {dataframe.shape}")
        
        #fit_transform min max scaler
        self.min_max_scaler = MinMaxScaler()
        dataframe = self.min_max_scaler.fit_transform(dataframe)

        logger.info("Data preprocessor fully initialized")


    def song_preprocessing(self,full_song):
        """
        Preprocesses a single song by applying column deletion, categorical encoding,
        artist selection, and scaling.
        """
        logger.info("Started song preprocessing")
        full_song = full_song.to_frame().T
        full_song = self.pre_delete_columns(full_song)
        full_song = self.pre_encode_categorical(full_song)
        full_song = self.pre_set_artist(full_song)
        full_song = self.pre_scale_song(full_song)
        logger.info("Succesfully processed song")
        return full_song



    def pre_delete_columns(self,full_song):
        """
        Deletes unnecessary columns from the dataframe to reduce noise and improve efficiency.
        """
        try:
            full_song = full_song.drop("track_name",axis=1)
            full_song = full_song.drop("released_year",axis=1)
            full_song = full_song.drop("released_month",axis=1)
            full_song = full_song.drop("released_day",axis=1)
            full_song = full_song.drop("in_spotify_playlists",axis=1)
            full_song = full_song.drop("in_spotify_charts",axis=1)
            full_song = full_song.drop("in_apple_charts",axis=1)
            full_song = full_song.drop("in_apple_playlists",axis=1)
            full_song = full_song.drop("in_deezer_playlists",axis=1)
            full_song = full_song.drop("in_deezer_charts",axis=1)
            full_song = full_song.drop("in_shazam_charts",axis=1)
            full_song = full_song.drop("cover_url",axis=1)
            return full_song
        except:
            logger.error("couldn't delete a column")

    def pre_encode_categorical(self,full_song):
        """
        Applies one-hot encoding to categorical columns ("key" and "mode").
        """
        try:
            categorical_columns = ["key", "mode"]
            one_hot_encoded = self.one_hot_encoder.transform(full_song[categorical_columns])
            
            return self.clean_after_one_hot_encoding(full_song,one_hot_encoded, categorical_columns)
        except:
            logger.error("couldn't one hot encode song", exc_info=True)
            
            
    def clean_after_one_hot_encoding(self,full_song,one_hot_encoded, categorical_columns):
        """
        Cleans the dataframe after one-hot encoding by removing original categorical columns,
        adding one-hot encoded data, and dropping any NaN columns created during the process.
        """
        try:
            logger.info(f"one_hot_encoded shape: {one_hot_encoded.shape}")
            column_names = self.one_hot_encoder.get_feature_names_out(categorical_columns)
            one_hot_full_song = pd.DataFrame(
                one_hot_encoded.toarray(),
                columns=column_names
                ,index=full_song.index
                )
            logger.info("One_hot_full transformed to dataframe")        
            #cleaning new song
            one_hot_full_song = one_hot_full_song.drop("key_nan",axis=1)
            logger.info("dropped NaN column")

            # Drop original categorical columns from `full_song`
            full_song = full_song.drop(categorical_columns, axis=1)

            # Concatenate original data with one-hot-encoded data
            full_song = pd.concat([full_song, one_hot_full_song], axis=1)
            return full_song
        except:
            logger.error("could not clean data after one hot encoding", exc_info=True)

    def pre_set_artist(self,full_song):
        """
        Extracts and encodes the main artist's name from the "artist(s)_name" column.
        """
        try:
            pd.set_option('display.max_rows', None)  # Show all rows
            pd.set_option('display.max_columns', None)  # Show all columns
            pd.set_option('display.width', None)  # Avoid line wrapping
            pd.set_option('display.max_colwidth', None)
            logger.info(f"logger receives {full_song}")
            
            
            full_song = self.set_only_first_artist(full_song)

            #encode the artist as number
            label_columns = [ "main_artist"]
            
            full_song['main_artist'] = self.label_encoder.transform(full_song[label_columns])
            return full_song
        except:
            logger.error("label encode the song", exc_info=True)
        
    def set_only_first_artist(self,full_song):
        """
        Selects the first artist from the "artist(s)_name" column and creates a new column "main_artist".
        """
        try:
            full_song["artist(s)_name"] = full_song["artist(s)_name"].astype(str)
            full_song["main_artist"] = full_song["artist(s)_name"].str.split(",").str[0]

            # Drop the "artist(s)_name" column as it's no longer needed
            return full_song.drop("artist(s)_name", axis=1)
        except:
            logger.error("could not select the first artist in data", exc_info=True)

    def pre_scale_song(self,full_song):
        """
        Applies Min-Max scaling to normalize numerical features in the dataframe.
        """
        try:
            logger.info(full_song[:10])
            full_song = pd.DataFrame(self.min_max_scaler.transform(full_song), columns=full_song.columns)
            return full_song
        except:
            logger.error("could not min max scale the data")
