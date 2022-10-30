import math
from collections import Counter


class CountVectorizer:
    """Convert a text corpus to a matrix of words counts."""

    def __init__(self):
        self.feature_names = {}

    def get_feature_names(self) -> list[str]:
        """
        Return a list of unique words from text corpus
        :return: list of words
        """
        return list(self.feature_names)

    def set_feature_names(self, corpus: list[str]) -> dict[str, int]:
        """
        Retrieves a list of unique words from text corpus
        :param corpus: list of strings
        :return: list of words
        """
        idx = 0
        for sentence in corpus:
            sentence = sentence.lower().split(' ')
            for word in sentence:
                if word not in self.feature_names:
                    self.feature_names[word] = idx
                    idx += 1
        return self.feature_names

    def fit_transform(self, corpus: list[str]) -> list[list[int]]:
        """
        Generate count matrix, each row corresponds to sentence in corpus,
        each column corresponds to unique words from corpus
        :param corpus: list of strings
        :return: count matrix for corpus
        """
        matrix = []
        self.set_feature_names(corpus)
        for sentence in corpus:
            sentence = sentence.lower().split(' ')
            feature_freq = [0] * len(self.feature_names)
            cnt = Counter(sentence)
            for k in cnt.keys():
                feature_freq[self.feature_names[k]] = cnt[k]
            matrix.append(feature_freq)
        return matrix


class TfidfTransformer:
    """ Convert a count matrix to a tf-idf matrix."""
    def tf_transform(self, count_matrix: list[list[int]]) -> list[list[float]]:
        """
        Generate term frequency matrix from count matrix
        :param count_matrix: count matrix for corpus
        :return: tf matrix
        """
        tf_matrix = []
        for vector in count_matrix:
            word_cnt = sum(vector)
            tf_row = [round(i / word_cnt, 3) for i in vector]
            tf_matrix.append(tf_row)
        return tf_matrix

    def idf_transform(self, count_matrix: list[list[int]]) -> list[float]:
        """
        Generate inverse document frequency matrix from count matrix
        :param count_matrix: count matrix for corpus
        :return: idf vector
        """
        n_docs = len(count_matrix)
        word_freq = [0] * len(count_matrix[0])
        for vector in count_matrix:
            word_freq = [j + bool(k) for j, k in zip(word_freq, vector)]
        return [round(math.log((n_docs + 1) / (word + 1)) + 1, 3) for word in word_freq]

    def fit_transform(self, count_matrix: list[list[int]]) -> list[list[float]]:
        """
        TfIdf = Tf * Idf
        :param count_matrix: count matrix for corpus
        :return: tf-idf matrix
        """
        tf = self.tf_transform(count_matrix)
        idf = self.idf_transform(count_matrix)
        tfidf_matrix = [[round(x * y, 3) for x, y in zip(tf_vec, idf)] for tf_vec in tf]
        return tfidf_matrix


class TfidfVectorizer(CountVectorizer):
    """ Convert a text corpus to a matrix of TF-IDF features."""
    def __init__(self):
        super().__init__()
        self.tf_idf = TfidfTransformer()

    def fit_transform(self, corpus: list[str]) -> list[list[float]]:
        """
        Generate tf-idf matrix from corpus
        :param corpus: list of strings
        :return: tf-idf matrix for corpus
        """
        count_matrix = super().fit_transform(corpus)
        return self.tf_idf.fit_transform(count_matrix)


if __name__ == '__main__':
    corpus = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    vectorizer1 = CountVectorizer()
    corpus1 = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    count_matrix1 = vectorizer1.fit_transform(corpus1)
    assert vectorizer1.get_feature_names() == [
        'crock', 'pot', 'pasta', 'never', 'boil', 'again', 'pomodoro',
        'fresh', 'ingredients', 'parmesan', 'to', 'taste']
    assert count_matrix1 == [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]]

    transformer = TfidfTransformer()
    tf_matrix = transformer.tf_transform(count_matrix1)
    assert tf_matrix == [
        [0.143, 0.143, 0.286, 0.143, 0.143, 0.143, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.143, 0.0, 0.0, 0.0, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143]]
    idf_matrix = transformer.idf_transform(count_matrix1)
    assert idf_matrix == [1.405, 1.405, 1.0, 1.405, 1.405, 1.405, 1.405, 1.405, 1.405, 1.405, 1.405, 1.405]
    tfidf_matrix1 = transformer.fit_transform(count_matrix1)
    assert tfidf_matrix1 == [
        [0.201, 0.201, 0.286, 0.201, 0.201, 0.201, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.143, 0.0, 0.0, 0.0, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201]]

    vectorizer2 = TfidfVectorizer()
    tfidf_matrix2 = vectorizer2.fit_transform(corpus)
    assert vectorizer2.get_feature_names() == [
        'crock', 'pot', 'pasta', 'never', 'boil', 'again', 'pomodoro',
        'fresh', 'ingredients', 'parmesan', 'to', 'taste']
    assert tfidf_matrix2 == [
        [0.201, 0.201, 0.286, 0.201, 0.201, 0.201, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.143, 0.0, 0.0, 0.0, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201]]
