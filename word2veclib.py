
import sys

from gensim.models.word2vec import Word2Vec
model = Word2Vec.load_word2vec_format('./google.bin', binary=True)
model.most_similar("test")
