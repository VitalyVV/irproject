from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
from matplotlib import pyplot


# define training data
with open('text.txt') as inp:
    sentences = [x.strip().lower().split() for x in inp.readlines()[:1000]]

# Defining the structure of our word2vec model

# Size is the dimentionality feature of the model
model_1 = Word2Vec(size=300, min_count=1)
#Feeding Our coupus
model_1.build_vocab(sentences)
#Lenth of the courpus
total_examples = model_1.corpus_count
#traning our model
model_1.train(sentences, total_examples=total_examples, epochs=model_1.epochs)

# X holds the vectors of n dimentions for each word in our vocab
X = model_1[model_1.wv.vocab]
model_1.save('model.h')
import pickle
pickle.dump(X, open('vectors.bin', 'wb'))