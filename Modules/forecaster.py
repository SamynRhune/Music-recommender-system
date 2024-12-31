import pickle
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,MinMaxScaler
import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances

class Forecaster():
    def __init__(self):
        with open('./Models/agglo_model.pkl', 'rb') as file:
            self.model = pickle.load(file)

    def get_prediction(self,liked_song, count, preprocessed_df, clustered_df):
        # preprocess the new song
        df = preprocessed_df

        #getting the centroids
        centroids = []
        agglo_labels = self.model.labels_
        for cluster_id in np.unique(agglo_labels):
            cluster_points = df[agglo_labels == cluster_id]
            centroids.append(cluster_points.mean(axis=0))
        centroids = np.array(centroids)

        #finding closest cluster
        new_data_point = liked_song #.reshape(1, -1)
        distances = pairwise_distances(new_data_point, centroids)
        closest_cluster = np.argmin(distances)

        #adding labels, finding label and selecting labels
        df_clus = clustered_df
        cluster_songs = df_clus[df_clus["clusters"] == closest_cluster]

        return cluster_songs.sample(n=count)