import json

indicators = {"^^^", "%%%", "///"}

#input file_name, output list of all lines
def read(file_name):
  file_list = []
  file = open(file_name, "r")
  file_list = file.read().split("\n")
  file.close()
  return(file_list)

#take out punctuation and convert to lowercase
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

#copy data from txt to json
def convert_to_json(file_name, output_file_name):
  data = {}
  data["lines"] = []
  
  for line in read(file_name):
    #line written as dict with attributes string and indicator
    line_write = {}
    indicator = ""
    line_string = line
    
    if line[-3:] in indicators:
      indicator = line[-3:]
      line_string = line[:-3]
      
    line_write["string"] = line_string
    line_write["indicator"] = indicator
    
    data["lines"].append(line_write)

  with open(output_file_name, 'w') as outfile:
    json.dump(data, outfile)
    
#input file_name output data as dict
def read_json(file_name):
  data = json.load(open(file_name))
  return(data)

def write_json(data, file_name):
  with open(file_name, 'w') as outfile:
    json.dump(data, outfile)

convert_to_json("con_log.txt","con_log.json")
  
  
  