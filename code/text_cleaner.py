from nltk.stem import PorterStemmer       
from nltk.stem import WordNetLemmatizer
from functools import reduce
import progressbar

class text_cleaner:

    ps = PorterStemmer()
    wl = WordNetLemmatizer()

    def __init__(self, stop_words = []):
        self.stop_words = set(stop_words)

    def apply_to_all(self, sentences):
        function_list = [self.remove_stop_word, self.decontraction, self.epytruc,
            self.replace_number, self.stemming, self.lemmatize]
        cleaned_sentences = []
        with progressbar.ProgressBar(max_value=len(sentences)) as bar:
            for i,sentence in enumerate(sentences):
                cleaned_words = [self.apply(word, function_list) for word in sentence.split()]
                cleaned_sentences.append(' '.join(cleaned_words))
                bar.update(i)
        return cleaned_sentences

    def apply(self, word, functions):
        return reduce(lambda w, f: f(w), functions, word)

    def remove_stop_word(self, word):
        return word if word not in self.stop_words else ''

    def decontraction(self, word):
        word = word.replace("don't", "do not")
        word = word.replace("won't", "will not")
        word = word.replace("'t", " not")
        word = word.replace("'m", " am")
        word = word.replace("'ve", " have")
        word = word.replace("'ll", " will")
        word = word.replace("'d", " would")
        word = word.replace("n'd", " not")
        return word

    def epytruc(self, word):
        if word == 'rt':
            word = 'real talk'
        if word == 'im':
            word == 'i am'
        return word

    def replace_number(self, word):
        try: 
            float(word)
            return '<number>'
        except ValueError:
            return word    
    
    def stemming(self, word):
        return self.ps.stem(word)

    def lemmatize(self, word):
        return self.wl.lemmatize(word)
