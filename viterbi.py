import sys
from collections import defaultdict

def get_word(file_name):
  word_set = set()
  sentences = []
  with open(file_name) as f:
    for line in f:
      sentences.append(line.rstrip('\n'))
      for word in line.split():
        word_set.add(word)
  return word_set, sentences
  # print word_set
  # lines = [line.rstrip('\n') for line in open(file_name)]
  # return lines

def get_matrix(file_name, words, tags):
  transition, emission = defaultdict(dict), defaultdict(dict)
  for tag in tags: 
    for word in words:  
      emission[tag][word] = 0.0001

  for tag_x in tags:
    for tag_y in tags:
      transition[tag_x][tag_y] = 0.0001

  with open(file_name) as f:
    for line in f:
      data = line.rstrip('\n').split(" ")
      if data[0] in words:
        emission[data[1]][data[0]] = float(data[2])
      else:
        transition[data[1]][data[0]] = float(data[2])
  return transition, emission

def viterbi(sentences, transition, emission, tags):
  for sentence in sentences:
    sentence = sentence.split(" ")
    dp = [defaultdict(dict) for _ in range(len(sentence))]
    # print dp
    for i in range(0,len(sentence)):
      if(i == 0):
        for tag in tags:
          dp[0][tag] = transition["phi"][tag]
      else:
        word = sentence[i-1]
        for tag in tags:
          dp[i][tag] = 0
          for tag_prev in tags:
            # print dp[i-1][tag_prev], transition[tag_prev][tag], emission[tag_prev][word], dp[i-1][tag_prev] * transition[tag_prev][tag] * emission[tag_prev][word]
            dp[i][tag] = max(dp[i][tag], dp[i-1][tag_prev] * transition[tag_prev][tag] * emission[tag_prev][word])
    res = 0
    for tag in tags:
      res = max(res, dp[-1][tag]*transition[tag]["fin"] * emission[tag_prev][sentence[-1]])
    print dp, res
    # print
    # print transition
    # print
    # print emission


def main():
  file_sents = sys.argv[1]
  file_probs = sys.argv[2]
  words, sentences = get_word(file_sents)
  tags = ["A","B", "phi", "fin"]
  # tags = ["noun","verb", "inf", "prep", "phi", "fin"]
  transition, emission = get_matrix(file_probs, words, tags)
  tags_normal = ["A", "B"]
  # tags_normal = ["noun","verb", "inf", "prep"]
  viterbi(sentences, transition, emission, tags_normal)
  # print emission

if __name__ == "__main__":
    main()