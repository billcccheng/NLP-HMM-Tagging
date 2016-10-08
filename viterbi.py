import sys

def read_file(file_name):
  lines = [line.rstrip('\n') for line in open(file_name)]
  return lines

def main():
  file_name = sys.argv[1]
  print read_file(file_name)
    
if __name__ == "__main__":
    main()