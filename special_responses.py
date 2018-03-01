import datetime
import read
import math
import classes
from PyDictionary import PyDictionary
dictionary = PyDictionary()

#transfer all variables global variables to special_responses file

functions = {}

def sin(inp):
  return (math.sin(math.radians(inp)))
functions["sin"] = sin
functions["sine"] = sin
def cos(inp):
  return (math.cos(math.radians(inp)))
functions["cos"] = cos
functions["cosine"] = cos
def tan(inp):
  return (math.tan(math.radians(inp)))
functions["tan"] = tan
functions["tangent"] = tan


#just for use in math functions
def find_nums(inp):
  numbers = []
  num_chars = "1234567890."

  num_part = ""
  for letter in inp:
    if letter in num_chars:
      num_part += letter
    else:
      try:
        numbers.append(float(num_part))
      except:
        pass
      num_part = ""
  try:
    numbers.append(float(num_part))
  except:
    pass
  return(numbers)

def calculate(inp):
  output = 0
  #list of every number and operation in order as strings
  operation_list = []
  numbers = find_nums(inp)
  #numbers searched separately because of issues with order
  oper_char = "+/-*v^()]"
  multi_char = ["sin", "cos", "tan"]
  multi_implied = ["]("]
  all_list = oper_char

  num_part = ""

  #break into operators and numbers
  for i in range(len(inp)):
    char = inp[i]
    num_part += char
    #print("char is " + char + " num_part is " + num_part)
    if num_part in all_list:
      operation_list.append(num_part)
      num_part = ""
    else:
      if float(num_part) == numbers[0]:
        operation_list.append(num_part)
        num_part = ""
        numbers.pop(0)

  #add multiplication where it is assumed as in 2(4 + 6) to become 2 * (4 + 6)
  for i in range(len(operation_list)):
    current = operation_list[i]

    if i != 0 and current in multi_implied:
      previous = operation_list[i - 1]

      if previous not in oper_char:
        operation_list.insert(i,"*")

  #combine to str and solve parenthesis
  open_count = 0
  closed_count = 0
  cut = [0,0]
  for i in range(len(operation_list)):
    current = operation_list[i]

    if current == "(":
      open_count += 1
      #make sure it's the only the first parenthesis
      cut[0] = i
    elif current == ")":
      closed_count += 1

    if open_count == closed_count and not open_count == 0:
      cut[1] = i + 1
      open_count = 0
      closed_count = 0
      string = ("").join(operation_list[cut[0]:cut[1]])
      new_num = calculate(string[1:len(string) - 1]) #take out parenthesis
      operation_list = operation_list[:cut[0]] + [new_num] + operation_list[cut[1]:] #combine where needed

  #solve exponents
  for i in range(len(operation_list)):
    current = operation_list[i]
    if i != 0 and i != (len(operation_list) - 1) and (current == "^"):
      previous = operation_list[i - 1]
      next = operation_list[i + 1]
      cut = [i-1, i+2]
      number = str(math.pow(float(previous),float(next)))
      operation_list = operation_list[:cut[0]] + ["placeholder", number,"placeholder"] + operation_list[cut[1]:]
  operation_list = [c for c in operation_list if c != 'placeholder']

  #solve roots
  for i in range(len(operation_list)):
    current = operation_list[i]
    if i != (len(operation_list) - 1) and current == "]":
      next = operation_list[i + 1]
      cut = [i, i + 2]
      number = str(math.pow(float(next), 0.5))
      operation_list = operation_list[:cut[0]] + ["placeholder", number,"placeholder"] + operation_list[cut[1]:]
  operation_list = [c for c in operation_list if c != 'placeholder']

  #solve multiplication and division
  for i in range(len(operation_list)):
    current = operation_list[i]
    if i != 0 and i != (len(operation_list) - 1):
      previous = operation_list[i - 1]
      next = operation_list[i + 1]
      cut = [i-1, i+2]
      if current == "*":
        number = str(float(previous)*float(next))
        operation_list = operation_list[:cut[0]] + ["placeholder", number, "placeholder"] + operation_list[cut[1]:]
      if current == "/":
        number = str(float(previous)/float(next))
        operation_list = operation_list[:cut[0]] + ["placeholder", number, "placeholder"] + operation_list[cut[1]:]
  operation_list = [c for c in operation_list if c != 'placeholder']

  #solve addition and subtraction
  operator = "+"
  for i in range(len(operation_list)):
    current = operation_list[i]
    if current in oper_char:
      operator = current
    else:
      output += float(("").join([operator, current]))

  return(str(output))

#function definitions
def now_date(inp):
  now = datetime.datetime.now()
  month = str(now.month)
  day = str(now.day)
  year = str(now.year)
  return("today's date is " + month + "/" + day + "/" + year)
functions["date"] = now_date

def add(inp):
  sum_of_nums = 0
  numbers = find_nums(inp)
  for i in numbers:
    sum_of_nums += i
  return(sum_of_nums)
functions["add"] = add

def subtract(inp):
  difference = 0
  numbers = find_nums(inp)
  difference += 2*numbers[0]
  for i in numbers:
    difference = difference - i
  return(difference)
functions["subtract"] = subtract

def multiply(inp):
  product_of_nums = 1
  numbers = find_nums(inp)
  for i in numbers:
    product_of_nums = product_of_nums*i
  return(product_of_nums)
functions["multiply"] = multiply

def divide(inp):
  quotient = 1
  numbers = find_nums(inp)
  for i in numbers:
    product_of_nums = quotient/i
  return(quotient)
functions["divide"] = divide

def do_math(inp):
  #doing math in words
  numbers = find_nums(inp)
  if len(numbers) == 0:
    return("My math function couldn't find any numbers.")

  keywords = ["add", "plus", "minus", "times", "subtract", "multipl", "divide", "root", "sin", "cos", "tan"]
  current_keywords = []

  for i in keywords:
    if i in inp:
      current_keywords.append(i)

  if "add" in current_keywords or "plus" in current_keywords:
    return(add(inp))
  if "minus" in current_keywords or "subtract" in current_keywords:
    return(subtract(inp))
  if "times" in current_keywords or "multipl" in current_keywords:
    return(multiply(inp))
  if "divide" in current_keywords:
    return(divide(inp))
  if "root" in current_keywords:
    return(root(inp))
  if "sin" in current_keywords or "cos" in current_keywords or "tan" in current_keywords:
    return(trig_func(inp))

  #main math solver
  num_char = "1234567890.+()-*/^]"
  numbers_and_stuff = ""
  for i in inp:
    if i in num_char:
      numbers_and_stuff += i
  if numbers_and_stuff.count("(") == numbers_and_stuff.count(")"):
    solution = str(calculate(numbers_and_stuff))
    return("The solution is " + solution)
  else:
    return("I'm sorry, your input doesn't have the same number of ( and ).")
functions["math"] = do_math

def trig_func(inp):
  function = ""
  function_list = "sin sine cos cosine tan tangent".split(" ")
  number = 0

  for i in function_list:
    if i in inp:
      function = i

  try:
    number = find_nums(inp)[0]
  except:
    return("Trig function error.")

  if function == "":
    return("I couldn't understand what you were trying to say.")

  return("The " + function + " of " + str(number) + " is " + str(functions[function](number)))
functions["trig"] = trig_func

def root(inp):
  nth_root = 2
  operating_number = 0

  nth_root_list = ["gibberish_placeholder12321","square","cub","four","fi","six","seven","eight"]
  for i in range(len(nth_root_list)):
    look_root = i + 1
    string = nth_root_list[i]

    if string in inp:
      nth_root = look_root

  numbers = find_nums(inp)
  if len(numbers) > 1:
    nth_root = numbers[0]
    operating_number = numbers[1]
  else:
    operating_number = numbers[0]

  return(str(nth_root) + " root of " + str(operating_number) + " is " + str(math.pow(operating_number,1/nth_root)))
functions["root"] = root

def area(inp):
  simlified = read.simplify(inp)
  two_dim = ["square", "triangle", "circle", "rectangle" , "rect", "tri", "radius", "diameter"]
  word_list = two_dim
  numbers = find_nums(inp)

  key_words = []

  for i in word_list:
    if i in simlified:
      key_words.append(i)

  try:
    if "square" in key_words or "rectangle" in key_words or "rect" in key_words:
      area = numbers[0] * numbers[1]
      return(str(area) + ": area of rectangle  b/h " + str(numbers[0]) + "/" + str(numbers[1]))
    if "triangle" in key_words or "tri" in key_words:
      area = numbers[0]*numbers[1] * 0.5
      return(str(area) + ": area of triangle b/h " + str(numbers[0]) + "/" + str(numbers[1]))
    if "circle" in key_words:
      radius = numbers[0]
      pi = math.pi

      if "diameter" in key_words:#account for radius and diameter options
        radius = radius/2
      if 3.14 in numbers: #account for more standard version of pi
        pi = 3.14

      unrounded_area_string = str(radius**2) + " * pi"
      rounded_area_string = str(pi * radius * radius)

      return(rounded_area_string + ", " + unrounded_area_string + ": area of circle " + str(pi) + " as pi and radius " + str(radius))

  except:
    return("Did you want to find area? Specify the shape and provide two numbers.")
functions["area"] = area

def define(inp):
  simlified_inp = read.simplify(inp)
  simlified_word_list = simlified_inp.split(" ")

  word = simlified_word_list[0]

  keywords = ["def","define", "of", "word", "definition"]

  for i in range(len(keywords)):
    if keywords[i] in simlified_word_list:
      index = simlified_word_list.index(keywords[i]) + 1
      try:
        word = simlified_word_list[index]
        break
      except:
        break

  definition_dict = dictionary.meaning(word)
  response = "The word " + word + " means "

  for key in definition_dict:
    definition_list = definition_dict[key]
    response += "as a " + key + " "
    response += ", ".join(definition_list)
    response += "; "

  return(response)
functions["define"] = define

def synonym(inp):
  simlified_inp = read.simplify(inp)
  simlified_word_list = simlified_inp.split(" ")

  word = simlified_word_list[0]

  keywords = ["of", "synonym","synonyms", "word"]

  for i in range(len(keywords)):
    if keywords[i] in simlified_word_list:
      index = simlified_word_list.index(keywords[i]) + 1
      try:
        word = simlified_word_list[index]
        break
      except:
        break

  definition_dict = dictionary.synonym(word)
  response = "Synonyms of " + word + " are "
  response += ", ".join(definition_dict)

  return(response)
functions["synonym"] = synonym

def antonym(inp):
  simlified_inp = read.simplify(inp)
  simlified_word_list = simlified_inp.split(" ")

  word = simlified_word_list[0]

  keywords = ["of", "antonym", "antonyms","word"]

  for i in range(len(keywords)):
    if keywords[i] in simlified_word_list:
      index = simlified_word_list.index(keywords[i]) + 1
      try:
        word = simlified_word_list[index]
        break
      except:
        break

  definition_dict = dictionary.antonym(word)
  response = "Antonyms of " + word + " are "
  response += ", ".join(definition_dict)

  return(response)
functions["antonym"] = antonym