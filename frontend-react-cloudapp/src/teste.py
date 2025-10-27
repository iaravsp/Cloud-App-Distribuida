from english_words import get_english_words_set
import random

web2lowerset = get_english_words_set(['web2'], lower=True)
i = random.randint(0, len(web2lowerset) - 1)
print(list(web2lowerset)[i])