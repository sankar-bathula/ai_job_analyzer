# import all required modules
from gensim.models import Word2Vec, KeyedVectors
from pattern import es
import textract
from os import listdir
from os.path import isfile, join
import numpy as np
from scipy import spatial
from sklearn import decomposition
import matplotlib.pyplot as plt
import pickle

def read_all_resume(file):
	text = textract.process(file)
	return text.decode('utf-8')

#Next, we define a function to parse the documents (CVs) and save the word embeddings as follows:
def preprocess_training_data1(dir_cvs, dir_model_name):    
    dircvs = [join(dir_cvs, f) for f in listdir(dir_cvs) if isfile(join(dir_cvs, f))]
    alltext = ' '  
    for cv in dircvs:
        yd = read_All_CV(cv)
        alltext += yd + " "    
    alltext = alltext.lower()
    vector = []
    for sentence in es.parsetree(alltext, tokenize=True, lemmata=True, tags=True):
        temp = []
        for chunk in sentence.chunks:
            for word in chunk.words:
                if word.tag == 'NN' or word.tag == 'VB':
                    temp.append(word.lemma)
        vector.append(temp)
    global model
    model = Word2Vec(vector, size=200, window=5, min_count=3, workers=4)
    model.save(dir_model_name)

