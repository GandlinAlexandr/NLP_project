from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger
import cufflinks as cf
import pandas as pd
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
import cloudpickle
import matplotlib.pyplot as plt
import seaborn as sns

from loguru import logger
LOGGING = 'logs.log'
FORMAT = "{time}{level}{message}"
logger.add(LOGGING, format = FORMAT)

# Стоп-слова
stop_words = stopwords.words('russian')
stop_words.extend(['что', 'это', 'так',
                    'вот', 'быть', 'как',
                    'в', '—', 'к', 'за', 'из', 'из-за',
                    'на', 'ок', 'кстати',
                    'который', 'мочь', 'весь',
                    'еще', 'также', 'свой',
                    'ещё', 'самый', 'ул', 'комментарий',
                    'английский', 'язык'])

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

#-----
RND_STATE = 73
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

import gensim.downloader
from gensim.models import Word2Vec, KeyedVectors
from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger

from plotly.offline import iplot
import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
import numpy as np
#-----

@logger.catch
def text_prep(text) -> str:
    doc = Doc(text) # Преобразуем текст в объект класса документ
    doc.segment(segmenter) # Сегментация
    doc.tag_morph(morph_tagger)

    for token in doc.tokens:  # Токенизация
        token.lemmatize(morph_vocab)

    lemmas = [_.lemma for _ in doc.tokens]  # Лемматизация
    words = [lemma for lemma in lemmas if lemma.isalpha() and len(lemma) > 2]
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)

@logger.catch
def prep(df):
    df['title_clean'] = df.title.apply(text_prep)
    df['abstract_clean'] = df.abstract.apply(text_prep)
    df['text_clean'] = df.text.apply(text_prep)
    return df
#-----
class TfidfEmbeddingVectorizer(object):
    """Get tfidf weighted vectors"""
    def __init__(self, model):
        self.word2vec = model.wv
        self.word2weight = None
        self.dim = model.vector_size

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
                np.mean([self.word2vec.get_vector(w) * self.word2weight[w]
                         for w in words if w in self.word2vec] or
                        [np.zeros(self.dim)], axis=0)
                for words in X
            ])
def LogR(df):
    X_train, X_test, y_train, y_test = train_test_split(df.text_clean.str.split(),
                                                        df.regions.values,
                                                        random_state=RND_STATE)

    model = Word2Vec(sentences=X_train,
                     vector_size=200,
                     min_count=10,
                     window=2,
                     seed=RND_STATE)
    Log_Tf_Idf = Pipeline([('w2v', TfidfEmbeddingVectorizer(model)),
                           ('clf', LogisticRegression(random_state=RND_STATE,
                                                      max_iter=10000))])
    Log_Tf_Idf.fit(X_train, y_train)
    return Log_Tf_Idf
#-----
def predict(df):
    Log_Tf_Idf = pd.read_pickle(open('Log_Tf_Idf.pkl', 'rb'))
    x_text = df.text_clean.str.split()

    df['Regions'] = Log_Tf_Idf.predict(x_text) #!!!!!!!
    df = df.replace(['asia-pacific', 'americas', 'africa', 'middle-east', 'europe'],['Asia', 'America', 'Africa', 'Midle East', 'Europe'])
    return df

def hist(df):
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(6,4))
    sns.countplot(y=df["Regions"], palette='tab10', ax=ax, order=df['Regions'].value_counts(ascending=False).index)
    plt.title('Number of news by regions')
    return fig