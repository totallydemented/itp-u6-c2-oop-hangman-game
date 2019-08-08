from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, char, hit = False, miss = False):
        self.char = char
        self.hit = hit
        self.miss = miss
        if self.miss and self.hit:
            raise InvalidGuessAttempt()
        
    def is_hit(self):
        return self.hit
    
    def is_miss(self):
        return self.miss

class GuessWord():
    def __init__(self, answer):
        if answer == '':
            raise InvalidWordException()
        
        self.answer = answer.lower()
        self.masked = '*' * len(answer)
    
    def perform_attempt(self, guess):
        if len(guess) > 1:
            raise InvalidGuessedLetterException()
        
        small_guess = guess.lower()
        temp_list_answer = list(self.answer)
        temp_list_masked = list(self.masked)
        
        attempt_hit = small_guess in temp_list_answer
        attempt_miss = small_guess not in temp_list_answer
        
        for idx, letter in enumerate(temp_list_answer):
            if small_guess == letter:
                temp_list_masked[idx] = small_guess
        self.masked = "".join(temp_list_masked)
            
        guess_attempt = GuessAttempt(small_guess, attempt_hit, attempt_miss)
        
        return guess_attempt
            
        
            
class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word = None, number_of_guesses = 5):
        if not word:
            self.word = GuessWord(HangmanGame.select_random_word(HangmanGame.WORD_LIST))
        else:
            self.word = GuessWord(HangmanGame.select_random_word(word))
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
    
    @classmethod
    def select_random_word(cls, words):
        if words == []:
            raise InvalidListOfWordsException()
            
        return random.choice(words)
    
    def guess(self, letter):
        
        if self.is_lost() or self.is_won():
            raise GameFinishedException()
        
        small_letter = letter.lower()
        self.previous_guesses.append(small_letter)
        check = self.word.perform_attempt(small_letter)
        
        if check.is_miss():
            self.remaining_misses -= 1
            
        if '*' not in self.word.masked:
            raise GameWonException()
        
        if self.remaining_misses == 0:
            raise GameLostException()
        return check
            
        
    def is_finished(self):
        if '*' not in self.word.masked or self.remaining_misses == 0:
            return True
        return False

    def is_won(self):
        if self.is_finished() and '*' not in self.word.masked:
            return True
        return False
    
    def is_lost(self):
        if self.is_finished() and self.remaining_misses == 0:
            return True
        return False
