from abc import *

class Preprocessor:
    def __correct_abstract_error(self, _abstract):
        try:
            for i in range(len(_abstract)):
                if (_abstract[i] == '.' or _abstract[i].islower()) and _abstract[i + 1].isupper():
                    return _abstract[i + 1:]
        except:
            pass
        return _abstract

class Regularizer(Preprocessor, metaclass = ABCMeta):
    def __regularize_abstract(self, _abstract):
        pass

    def tokenize(self, _abstract):
        pass