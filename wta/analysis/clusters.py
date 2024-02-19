import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

# from wta.analysis.speeds import SpeedAnnotationService


class ClusterAnalysisService:
    
    @staticmethod
    def get_clusters(speed_df: pd.DataFrame, percentage: float) -> tuple[pd.DataFrame, pd.DataFrame]:
        minimum_cluster_size = np.round(speed_df.shape[0] * percentage)

        clusterer = DBSCAN(eps=2/6371., min_samples=10, n_jobs=-1, metric='haversine', algorithm='ball_tree')


        # clusterer = DBSCAN()
        clusterer.fit(speed_df[['Lon', 'Lat']])

        print(clusterer.core_sample_indices_[:5])

        labels = pd.Series(clusterer.labels_, index=speed_df.index)

        noise = speed_df.loc[labels == -1, ['Lon', 'Lat']]

        clusters = speed_df.loc[speed_df.index.difference(noise.index), ['Lon', 'Lat']]

        return clusters, noise



