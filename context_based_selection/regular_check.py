from jellyfish import levenshtein_distance as dist
from tqdm import tqdm
import numpy as np
import gensim


model = gensim.models.Word2Vec.load('model.h')


def rawCheckOnDist(str_list):
    corrected = []
    for word in tqdm(str_list):
        word = word.replace('\n', '')
        dists = []
        for vecs in model.wv.vocab:
            dists.append( (vecs, dist(vecs, word)) )

        v = model.wv[min(dists, key=lambda x: x[1])[0]]
        sim = model.most_similar(positive=[v], topn=1)
        corrected.append(sim[0][0])

    return corrected