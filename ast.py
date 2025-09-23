"""
ALL LINES OF SEBO CODE MUST END IN A SPACE!

SEBOTLF Abstract Syntax Tree Translator v0.25 (OT-P). To be written in C++ later.
Syntax that's Easy, Bold, and Efficient
Aarik Pokras

----------------------9/22/2025----------------------
Everything is working fine. Make sure to read notes.
Working on:
* Emitting LLVM
  - Defining registers
  - Getting pointers
  - Calling clib printf
  - Need user to declare when main prog starts?

* Note that ast no longer needs to be printed. This
  should help avoid confusion when running.
----------------------OT-P---------------------------
"""

line = "print 'hello dad!' print 'hello mom!!'"

tokens = []

##################################
def bitokens(strn):
  strn = strn.strip(' ') # strip any spaces from the beginning or end of lines.
  i = 0
  quote_count = 0
  in_quote = False
  while i < len(strn): # C-style for loop.
    if (strn[i] == "'"):
      quote_count += 1
      if (quote_count % 2 != 0): # QC is odd
        in_quote = True
        strn = strn.replace("'", "!", 1)
      else:
        in_quote = False
    elif (strn[i] == " ") and (in_quote == False):
      tokens.append(strn[0:i]) # append range [0] to [i] to tokens.
      strn = strn[i:len(strn)] # trim the appended token off of strn.
      strn = strn.strip(' ') # strip spaces from edges of strn.
      i = -1
    i += 1
  tokens.append(strn) # Add the remaining bit of TLF code after which there is no space.
  j = 0
  while j < len(tokens):
    tokens[j] = tokens[j].replace("'", "")
    j += 1
##################################

amt__var = 0

class _Print:
  def __init__(self, size, content, varnum):
    self.size = size # size arg should include null terminator.
    self.content = content
    self.amt__var = varnum
  def llvm(self):
    print("%." + str(self.amt__var) + " = private constant [" + str(self.size) + " x i8] c\"" + self.content + "\\00\"")

bitokens(line)
print(tokens)

#ast = ""

# Token decider
i = 0
while i < len(tokens):
  if (tokens[i][0] == "!"): # if a string (i.e. begins with !, we'll remove this here)
    tokens[i] = tokens[i].replace("!", "", 1)
  i += 1

# Token evaluator
i = 0
while i < len(tokens):
  if (tokens[i] == "print"):
    if (len(tokens) > i+1):
      _Print(len(tokens[i+1])+1, tokens[i+1], amt__var).llvm()
      amt__var += 1
    else:
      print("SEBO ASTT Error: Unexpected token without argument")
  i += 1

#print(ast)
