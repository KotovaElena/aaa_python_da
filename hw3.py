class CountVectorizer:
    """Convert a text corpus to a matrix of words counts."""

    def __init__(self):
        self.feature_names = []

    def get_feature_names(self) -> list[str]:
        """
        Return a list of unique words from text corpus
        :return: list of words
        """
        return self.feature_names

    def set_feature_names(self, corpus: list[str]) -> list[str]:
        """
        Retrieves a list of unique words from text corpus
        :param corpus: list of strings
        :return: list of words
        """
        for sentence in corpus:
            sentence = sentence.lower().split(' ')
            for word in sentence:
                if word not in self.feature_names:
                    self.feature_names.append(word)
        return self.feature_names

    def fit_transform(self, corpus: list[str]) -> list[list[int]]:
        """
        Generate count matrix, each row corresponds to sentence in corpus,
        each column corresponds to unique words from corpus
        :param corpus: list of strings
        :return: count matrix for corpus
        """
        matrix = []
        for sentence in corpus:
            sentence = sentence.lower().split(' ')
            feature_freq = []
            for feature in self.set_feature_names(corpus):
                feature_freq.append(sentence.count(feature))
            matrix.append(feature_freq)
        return matrix


if __name__ == '__main__':
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

    vectorizer2 = CountVectorizer()
    corpus2 = [
        'This is the first document',
        'This document is the second document',
        'And this is the third one',
        'Is this the first document'
    ]
    count_matrix2 = vectorizer2.fit_transform(corpus2)
    assert vectorizer2.get_feature_names() == [
        'this', 'is', 'the', 'first', 'document',
        'second', 'and', 'third', 'one']
    assert count_matrix2 == [
        [1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 2, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0]
    ]

    vectorizer3 = CountVectorizer()
    corpus3 = ['Avito']
    count_matrix3 = vectorizer3.fit_transform(corpus3)
    assert vectorizer3.get_feature_names() == ['avito']
    assert count_matrix3 == [[1]]

    vectorizer4 = CountVectorizer()
    corpus4 = ['Avito Avito Avito', 'Avito Otiva']
    count_matrix4 = vectorizer4.fit_transform(corpus4)
    assert vectorizer4.get_feature_names() == ['avito', 'otiva']
    assert count_matrix4 == [[3, 0], [1, 1]]

    vectorizer5 = CountVectorizer()
    corpus5 = []
    count_matrix5 = vectorizer5.fit_transform(corpus5)
    assert vectorizer5.get_feature_names() == []
    assert count_matrix5 == []
