import string

lowercase_letters = list(string.ascii_lowercase)
numbers = list(range(100))
prepositions: list[str] = [
    "about", "above", "across", "after", "against", "along", "among", "around",
    "at", "before", "behind", "below", "beneath", "beside", "between", "by",
    "down", "during", "for", "from", "in", "inside", "into", "near", "of",
    "off", "on", "out", "over", "through", "to", "under", "up", "with", "without"
]
articles: list[str] = ['the', 'a', 'an']
verbs: list[str] = ['can', 'have', 'do', 'use', 'go', 'take', 'make', 'see']
common_words: list[str] = [
    'and', 'is', 'that', 'this', 'you', 'it', 'as', 'are', 'be', 'but', 'not', 'or', 'if',
    'how', 'so', 'there', 'these', 'all', 'your', 'some', 'other', 'what', 'its', 'will', 'one', 'two',
    'my', 'here', 'don', 'here', 'had', 'no', 'yes', 'first', 'more', 'we', 'they', 'she'
]

BLACK_LIST: list[str] = lowercase_letters + numbers + prepositions + articles + verbs + common_words
