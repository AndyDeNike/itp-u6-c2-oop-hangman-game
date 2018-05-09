from .exceptions import *
import random 

class GuessAttempt(object):
    #default hit/miss are False 
    def __init__(self, letter_guess, hit=False, miss=False):
        #cant have hit and miss so it raises error
        if hit and miss:
            raise InvalidGuessAttempt()
        
        self.letter_guess = letter_guess 
        self.hit = hit 
        self.miss = miss
    
    def is_hit(self):
        if self.hit == True:
            return True
        return False
            
    def is_miss(self):
        if self.miss == True:
            return True
        return False
        


class GuessWord(object):
    
    def __init__(self, word):
        if word == '':
            raise InvalidWordException()
        self.answer = word.lower()
        self.masked = len(word) * "*"
        
    def perform_attempt(self, letter_guess):
        if len(letter_guess) > 1:
            raise InvalidGuessedLetterException()
        
        new_mask = ""
        lower_letter_guess = letter_guess.lower()
        
        if lower_letter_guess in self.answer: 
            for count, letter in enumerate(self.answer):
                if lower_letter_guess == letter or self.masked[count] != "*":
                    new_mask += letter
                else: 
                    new_mask += "*"
            self.masked = new_mask
            return GuessAttempt(letter_guess, True, False)
        else: 
            return GuessAttempt(letter_guess, False, True)
        
    
    
    


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word_list = word_list
        self.word = GuessWord(self.select_random_word(word_list))
        
        
    @classmethod 
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
        
    def guess(self, letter_guess):
        if self.is_finished():
            raise GameFinishedException()
        else:
            self.previous_guesses.append(letter_guess.lower())
            
            if self.word.perform_attempt(letter_guess).is_hit():
                if self.is_won():
                    raise GameWonException()
                return self.word.perform_attempt(letter_guess)

            else: 
                self.remaining_misses -= 1
                if self.is_lost():
                    raise GameLostException()
                return self.word.perform_attempt(letter_guess)
        
            
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True 
    
    def is_won(self):
        if "*" not in self.word.masked:
            return True 
        return False
    
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False
         
        