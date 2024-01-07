import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger
from sklearn.metrics.pairwise import cosine_similarity
import cufflinks as cf

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from gensim.models import Word2Vec
from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger
import numpy as np

LOGGING = "logs.log"
FORMAT = "{time}{level}{message}"
logger.add(LOGGING, format=FORMAT)

# Стоп-слова
stop_words = stopwords.words("russian")
stop_words.extend(
    [
        "что",
        "это",
        "так",
        "вот",
        "быть",
        "как",
        "в",
        "—",
        "к",
        "за",
        "из",
        "из-за",
        "на",
        "ок",
        "кстати",
        "который",
        "мочь",
        "весь",
        "еще",
        "также",
        "свой",
        "ещё",
        "самый",
        "ул",
        "комментарий",
        "английский",
        "язык",
    ]
)

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

RND_STATE = 73


@logger.catch
def text_prep(text) -> str:
    doc = Doc(text)  # Преобразуем текст в объект класса документ
    doc.segment(segmenter)  # Сегментация
    doc.tag_morph(morph_tagger)

    for token in doc.tokens:  # Токенизация
        token.lemmatize(morph_vocab)

    lemmas = [_.lemma for _ in doc.tokens]  # Лемматизация
    words = [lemma for lemma in lemmas if lemma.isalpha() and len(lemma) > 2]
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)


@logger.catch
def prep(df):
    df["title_clean"] = df.title.apply(text_prep)
    df["abstract_clean"] = df.abstract.apply(text_prep)
    df["text_clean"] = df.text.apply(text_prep)
    return df


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
            lambda: max_idf, [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()]
        )

        return self

    def transform(self, X):
        return np.array(
            [
                np.mean(
                    [
                        self.word2vec.get_vector(w) * self.word2weight[w]
                        for w in words
                        if w in self.word2vec
                    ]
                    or [np.zeros(self.dim)],
                    axis=0,
                )
                for words in X
            ]
        )


def LogR(df):
    X_train, X_test, y_train, y_test = train_test_split(
        df.text_clean.str.split(), df.regions.values, random_state=RND_STATE
    )

    model = Word2Vec(
        sentences=X_train, vector_size=200, min_count=10, window=2, seed=RND_STATE
    )
    Log_Tf_Idf = Pipeline(
        [
            ("w2v", TfidfEmbeddingVectorizer(model)),
            ("clf", LogisticRegression(random_state=RND_STATE, max_iter=10000)),
        ]
    )
    Log_Tf_Idf.fit(X_train, y_train)
    return Log_Tf_Idf


def predict(df, Log_Tf_Idf):
    x_text = df.text_clean.str.split()

    df["regions"] = Log_Tf_Idf.predict(x_text)
    df = df.replace(
        ["asia-pacific", "americas", "africa", "middle-east", "europe"],
        ["Asia", "America", "Africa", "Middle East", "Europe"],
    )
    return df


def hist(df, DATE):
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(6, 4))
    sns.countplot(
        x=df["regions"],
        palette="tab10",
        ax=ax,
        order=df["regions"].value_counts(ascending=False).index,
    )
    plt.title(
        "Распределение новостей (n="
        + str(len(df))
        + ") за "
        + ".".join(DATE.split("-")[::-1])
        + " по регионам мира"
    )
    return fig


def cosine_sim(df, theme):
    theme_prep = text_prep(theme)
    df2 = df.copy()
    df2.loc[len(df)] = theme_prep
    # Создание объекта TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()
    # Применение TF-IDF к текстовым данным
    tfidf_matrix = tfidf_vectorizer.fit_transform(list(df2.text_clean))
    # Матрица попарных значений косинусного сходства между векторами текстов
    X = cosine_similarity(tfidf_matrix)
    # Индекс столбца с максимальным значением косинусного сходства - индекс искомой статьи
    index = list(X[len(df2) - 1]).index(max(X[-1][:-1]))
    precent = str(round(max(X[-1][:-1]) * 100, 2)) + "%"
    return [index, precent]
