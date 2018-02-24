import random
import string
import math
import read
import special_responses

#output without punctuation and all lowercase
def simplify(in_string):
  # define punctuation
  punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
  
  # To take input from the user
  # my_str = input("Enter a string: ")
  
  # remove punctuation from the string
  no_punct = ""
  for char in in_string:
     if char not in punctuations:
         no_punct = no_punct + char
  
  # display the unpunctuated string
  return(no_punct.lower())

class Line():
  def __init__(self, string):
    self.string = string
    self.simplified_string = simplify(string)
    
    self.word_list = self.string.split(" ")
    self.simplified_word_list = self.simplified_string.split(" ")
    
    #ranks connected to string
    self.word_rank_list = []
    
    self.follow_lines = []
    
    #rank var used when ranking lines
    self.current_rank = 0
    
  def add_follow(self,followline):
    self.follow_lines.append(followline)

  def rank_words(self, lines):
    updated_list = []
    
    for word in self.word_list:
      #simlify the word
      word = read.simplify(word)
      
      #occurrences in this string
      occur_here = self.simplified_word_list.count(word)
      #number of total lines
      total_lines = len(lines)
      #total number of lines with this word
      lines_with_word = 0 #placeholder
      
      #update placeholder value
      for key in lines:
        line = lines[key]
        if word in line.simplified_word_list:
          lines_with_word += 1
      
      #put it all together
      updated_list.append(occur_here * 10 * math.log(total_lines/lines_with_word))
    
    self.word_rank_list = updated_list
    