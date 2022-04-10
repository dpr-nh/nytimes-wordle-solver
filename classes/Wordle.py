import csv
from classes.Browser import Browser

letter_frequencies = {
    "a": 8.4966,
    "b": 2.0720,
    "c": 4.5388,
    "d": 3.3844,
    "e": 11.1607,
    "f": 1.8121,
    "g": 2.4705,
    "h": 3.0034,
    "i": 7.5448,
    "j": 0.1965,
    "k": 1.1016,
    "l": 5.4893,
    "m": 3.0129,
    "n": 6.6544,
    "o": 7.1635,
    "p": 3.1671,
    "q": 0.1962,
    "r": 7.5809,
    "s": 5.7351,
    "t": 6.9509,
    "u": 3.6308,
    "v": 1.0074,
    "w": 1.2899,
    "x": 0.2902,
    "y": 1.7779,
    "z": 0.2722,
}

class Wordle:
    def __init__(self):
        self.absent_letters = []
        self.present_letters = []
        self.correct_letters = [
            "",
            "",
            "",
            "",
            "",
            ""
        ]
        self.words = self.read_words()
        self.browser = Browser()
        self.solved = False

    def read_words(self):
        words = []

        with open('data/words.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                words.append(row[0])

        return words
 
    def rate_words(self):
        rated_words = {}

        # filter words
        ## 1: by absent letters
        filtered_by_absent = []
        for word in self.words:
            has_letter = False

            for letter in list(word):

                for absent_letter in self.absent_letters:
                    if letter == absent_letter:
                        has_letter = True

            if has_letter == False:
                filtered_by_absent.append(word)


        ## 2: by present letters
        filtered_by_present = []
        if len(self.present_letters):
            for word in filtered_by_absent:
                has_letter = False

                for letter in list(word):
                    for present_letter in self.present_letters:
                        if letter == present_letter:
                            has_letter = True

                if has_letter == True:
                    filtered_by_present.append(word)
        else:
            filtered_by_present = filtered_by_absent

        ## 3: by correct letters
        filtered = []
        for word in filtered_by_present:
            word_is_ok = True

            for index, letter in enumerate(list(word)):
                if self.correct_letters[index] != "" and letter != self.correct_letters[index]:
                    word_is_ok = False
            
            if word_is_ok == True:
                filtered.append(word)

        for word in filtered:
            score = 0
            used_letters = []

            for letter in word:
                if letter not in used_letters:
                    score += letter_frequencies[letter]
                    used_letters.append(letter)

            rated_words[word] = score
        
        max_score = 0
        for key in rated_words:
            if rated_words[key] > max_score:
                max_word = key
                max_score = rated_words[key]

        return max_word
        

    def add_word_to_letter_lists(self, word, results):
        for index, result in enumerate(results):
            letter = word[index]

            if result == "correct":
                self.present_letters.append(letter)
                self.correct_letters[index] = letter
            elif result == "present":
                self.present_letters.append(letter)
            elif result == "absent":
                self.absent_letters.append(letter)

    def enter_word(self, word):
        results = self.browser.get_word_results(word)
        self.solved = all(elem == "correct" for elem in results)
        self.add_word_to_letter_lists(word, results)

    def solve_wordle(self):
        words_entered = 0
        while (not self.solved) and words_entered < 6:
            word = self.rate_words()
            self.enter_word(word)
            words_entered += 1
