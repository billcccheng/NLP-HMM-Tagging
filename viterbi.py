import sys
from collections import defaultdict

def get_word(file_name):
  word_set = set()
  sentences = []
  with open(file_name) as f:
    for line in f:
      sentences.append(line.rstrip('\n'))
      for word in line.split():
        word_set.add(word.lower())
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

def get_best_tag_sequence(bkptr, bkptr_list):
  bkptr_tag_list = [] 
  bkptr_tag = bkptr['end']
  bkptr_tag_list.append(bkptr_tag)
  for dict_pointer in bkptr_list[::-1]:
    bkptr_tag = dict_pointer[bkptr_tag]
    bkptr_tag_list.insert(0,bkptr_tag)
  return bkptr_tag_list

def viterbi(sentences, transition, emission, tags):
  for sentence in sentences:
    print "PROCESSING SENTENCE:" + sentence + '\n'
    
    sentence = sentence.split(" ")
    bkptr_list = []
    final_viterbi_network = [];
    dp = [defaultdict(dict) for _ in range(len(sentence))]
    for i in range(0,len(sentence)):
      word = sentence[i].lower()
      if(i == 0):
        for tag in tags:
          dp[i][tag] = transition["phi"][tag]
          final_viterbi_network.append([word, tag, dp[i][tag]])
          # print "P(%s=%s) = %f" %(word, tag, dp[i][tag])
      else:
        bkptr = {}
        for tag in tags:
          dp_prev = []
          dp_prev_tag = []
          for tag_prev in tags:
            dp_prev.append(dp[i-1][tag_prev] * transition[tag_prev][tag] * emission[tag][word])
            dp_prev_tag.append(tag_prev)
          dp[i][tag] = max(dp_prev)
          bkptr[tag] = dp_prev_tag[dp_prev.index(dp[i][tag])]
          final_viterbi_network.append([word, tag, dp[i][tag]])
        bkptr_list.append(bkptr)
    res = 0
    temp_tag = ""
    bkptr = {}
    # Last word e(word|STOP)
    for tag in tags:
      if res < dp[-1][tag]*transition[tag]["fin"] * emission[tag_prev][sentence[-1]]:
        res = dp[-1][tag]*transition[tag]["fin"] * emission[tag_prev][sentence[-1]]
        temp_tag = tag;
      bkptr['end'] = temp_tag

    print "FINAL VITERBI NETWORK"
    for node in final_viterbi_network:
      print "P(%s=%s) = %e" %(node[0], node[1], node[2])
    
    print

    print "FINAL BACKPTR NETWORK" 
    for i in range(len(sentence)-1, 0, -1):
      for tag in tags:
        print 'Backptr(%s=%s) = %s' %(sentence[i], tag, bkptr_list[i-1][tag])

    print

    bkptr_tag_list = get_best_tag_sequence(bkptr, bkptr_list)
    print "BEST TAG SEQUENCE HAS PROBABILITY = %e" %res
    for i in range(len(sentence)):
      print '%s -> %s' %(sentence[i], bkptr_tag_list[i])
    print dp
    print '\n\n'

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