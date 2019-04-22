from sklearn.metrics.pairwise import cosine_similarity

def cosSim(x, y):
    return cosine_similarity(x, y)
