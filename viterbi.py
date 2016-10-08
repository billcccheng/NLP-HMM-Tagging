import sys

def get_sentence(file_name):
  word_set = set()
  with open(file_name) as f:
    for line in f:
      for word in line.split():
        word_set.add(word)
  return word_set
  # print word_set
  # lines = [line.rstrip('\n') for line in open(file_name)]
  # return lines

def main():
  file_name = sys.argv[1]
  print list(get_sentence(file_name))
    
if __name__ == "__main__":
    main()