from .exceptions import *
import random


class GuessAttempt(object):
    
    def __init__(self,guess,hit=None ,miss=None):
        self.hit = hit
        self.miss = miss
        
        if hit and miss:
            raise InvalidGuessAttempt()    
        if hit :
            self.miss = False
        elif miss:
            self.hit = False
    

    def is_hit(self):
        return self.hit
    
    def is_miss(self):
        return self.miss


class GuessWord(object):
    
    def __init__(self,guess_word): 
        self.answer = guess_word
        self.masked = len(guess_word) * "*"
        
        if not guess_word:
            raise InvalidWordException()
    

    def perform_attempt(self,letter):
        if not len(letter) == 1 :
            raise InvalidGuessedLetterException()
            
        if letter.lower() in self.answer.lower():
            masked = ""
            for position,item in enumerate(self.answer.lower()):
                if letter.lower() == item:
                    masked += item
                else:
                    masked += self.masked[position]
            self.masked = masked
        
            return GuessAttempt(letter,hit=True)
        else:
            return GuessAttempt(letter,miss=True)


class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self,word_list=None, number_of_guesses=5):
        
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        if not word_list:
            word_list = self.WORD_LIST
        chosen_word = self.select_random_word(word_list)
        self.word = GuessWord(chosen_word)
        self.won = False
        self.finished = False
        self.lost = False
        
    @classmethod
    def select_random_word(self,list_of_words=None):
        if not list_of_words:
            raise InvalidListOfWordsException()
        return random.choice(list_of_words)
        
    def guess(self,letter):
        self.previous_guesses.append(letter.lower())
        
        if self.remaining_misses == 0 :            
            raise GameFinishedException()
            
        if self.word.answer == self.word.masked :
            raise GameFinishedException()
        
        result = self.word.perform_attempt(letter)
        if result.is_miss():
            self.remaining_misses -= 1
    
        if self.word.answer == self.word.masked :
            self.finished = True
            self.won = True
            raise GameWonException()        
        
        if self.remaining_misses == 0 :
            
            self.finished = True
            self.lost = True

            raise GameLostException()

        return result
        
    def is_finished(self):
        return self.finished
        
    def is_lost(self):
        return self.lost
    
    def is_won(self):
        return self.won
        
        
