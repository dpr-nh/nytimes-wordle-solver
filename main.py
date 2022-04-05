import csv

letter_frequencies = {
    "a": 8.34,
    "b": 1.54,
    "c": 2.73,
    "d": 4.14,
    "e": 12.6,
    "f": 2.03,
    "g": 1.92,
    "h": 6.11,
    "i": 6.71,
    "j": 0.23,
    "k": 0.87,
    "l": 4.24,
    "m": 2.53,
    "n": 6.8,
    "o": 7.7,
    "p": 1.66,
    "q": 0.09,
    "r": 5.68,
    "s": 6.11,
    "t": 9.37,
    "u": 2.85,
    "v": 1.06,
    "w": 2.34,
    "x": 0.2,
    "y": 2.04,
    "z": 0.06,
}

def read_words():
    words = []

    with open('words.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            words.append(row[0])

    return words
 
def rate_words(words):
    rated_words = {}

    for word in words:
        score = 0
        used_letters = []

        for letter in word:
            if letter not in used_letters:
                score += letter_frequencies[letter]
                used_letters.append(letter)

        rated_words[word] = score
    
    return rated_words
        

words = read_words()
rated_words = rate_words(words)

max_score = 0

for key in rated_words:
    if rated_words[key] > max_score:
        max_word = key
        max_score = rated_words[key]

print(max_word)
print(max_score)
