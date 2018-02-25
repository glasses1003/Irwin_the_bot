import read
import classes
import random
import special_responses


json_file_name = "con_log.json"
context_file_name = "context_data.json"
#json object
data = "placeholder"

lines = {}

def add_line(string):
  if not string in lines:
    lines[string] = classes.Line(string)

def update_lines_dict():
  lines_from_file = data["lines"] #list
  
  for i in range(len(lines_from_file)):
    line = lines_from_file[i]
    string = line["string"]
    indicator = line["indicator"]
    
    #indicator ^^^ means line not added
    #indicator %%% means end follow is added
    
    if indicator == "":
      add_line(string)
      follow = lines_from_file[i + 1]
      
      lines[string].add_follow(follow)
    elif indicator == "%%%":
      add_line(string)
      follow = "%%%"
      
      lines[string].add_follow(follow)
    elif indicator == "///":
      pass
    elif indicator == "^^^":
      pass
  
#rank words within the object
def rank_words():
  #rank every word
  for key in lines:
    line = lines[key]
    line.rank_words(lines)

def create_user(recipient_id):
  data_dict = {}
  data_dict["conversation"] = []
  data_dict["math"] = []
  data_dict["name"] = ""
  return(data_dict)

def get_data(recipient_id):
  #if user exists
  if not recipient_id in context:
    print("New user created " + recipient_id)
    user_data = create_user(recipient_id)
    context[recipient_id] = user_data
    userdata = context[recipient_id]
  else:
    print("Returning user " + recipient_id)
    userdata = context[recipient_id]

  return(userdata)
    
def start(recipient_id):
  #get data
  global data, context, userdata
  data = read.read_json(json_file_name)
  context = read.read_json(context_file_name)
  #update_line dict
  update_lines_dict()
  #rank all words
  rank_words()
  #gets or creates data
  userdata = get_data(recipient_id)
  
#rank all lines for similarity
def rank_lines(inp):
  simlified_input = read.simplify(inp)
  input_simlified_word_list = simlified_input.split(" ")
  
  #rank all responses
  for key in lines:
    line = lines[key]
    #the words in the input and in the line
    intersection_strings = []
    intersection = []
    
    #reset current rank
    line.current_rank = 0
    
    for i in range(len(line.simplified_word_list)):
      word = line.simplified_word_list[i]
      rank = line.word_rank_list[i]
      
      if (word in input_simlified_word_list):
        intersection_strings.append(word)
        intersection.append(rank)
      
    #combine  
    rank_to_be = 1
    for i in intersection:
      rank_to_be = rank_to_be * i
    #extra weight towards percentage of overlap
    dilute = 1 #take away certain power from the overlap function
    sum_len = (len(line.simplified_word_list) + len(input_simlified_word_list))
    rank_to_be = rank_to_be * (len(intersection)/sum_len)

    line.current_rank = rank_to_be
def respond_to(inp):
  simplified_inp = read.simplify(inp)
  
  rank_lines(inp)

  #pick highest ranking response
  highest = 0
  highest_obj = []
  
  for key in lines:
    line = lines[key]
    if line.current_rank > highest:
      highest = line.current_rank
      highest_obj = [line]
    elif line.current_rank == highest:
      highest_obj.append(line)
      
  #follow lines to choose from
  followline_choice = []
  for obj in highest_obj:
    followline_choice += obj.follow_lines

  response_obj = random.choice(followline_choice)
  response_string = response_obj["string"]
  #check for special responses
  if response_obj["indicator"] == "///":
    response_string = special_responses.functions[response_string](inp)

  userdata["conversation"].append(inp)
  userdata["conversation"].append(response_string)

  #write context back to json
  read.write_json(context, context_file_name)
  return(response_string)
def test():
  start()
  while True:
    user_input = input("?: ")
    print(respond_to(user_input))
