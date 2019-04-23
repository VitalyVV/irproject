"""
construct dictionary
"""
from nltk import word_tokenize
from collections import Counter
import pickle


def readWikiVocab(fn="vocab.txt"):
    with open(fn, 'r') as input_file:
        cnt = Counter()
        for line in input_file:
            word, freq = line.strip().split()
            cnt[word] += int(freq)
    return cnt


def pythonTokenizeText(fn, output_fn):
    with open(fn, 'r') as input_file:
        tok_lines = []
        for line in input_file:
            tok_seq = word_tokenize(line.strip().lower().decode('utf8'))
            tok_line = ' '.join(tok_seq)
            tok_lines.append(tok_line)

    with open(output_fn, 'w') as output_file:
        tok_text = '\n'.join(tok_lines)
        print(tok_text.encode("utf8"), file=output_file)
    print('done processing train text...')


def dumpDict(fn='tok_train.txt'):
    """
    dict: words in lower case
    """
    # word from wikipedia
    cnt = readWikiVocab()

    # word from perspective data
    with open(fn, 'r') as input_file:
        text = input_file.read()
        text_seq = text.split()
        for word in text_seq:
            cnt[word] += 1

    # dump dictionary
    with open('dict.pickle', 'wb') as handle:
        pickle.dump(cnt, handle)
    print('done dumping the vocabulary...')


def loadDict(fn='vocab.txt', freq_threshold=6):
    with open(fn, 'r') as handle:
        cnt = dict(list(map(lambda x: (x.split()[0], int(x.split()[1])), handle.readlines())))
        rare_words = [word for word in cnt if cnt[word] < freq_threshold]
    for word in rare_words:
        cnt.pop(word)
    print('done loading dictionary...')
    return cnt


def sanityCheck(cnt_dump='dict.pickle', test_fn='tok_test.txt'):
    cnt = loadDict(cnt_dump)

    with open(test_fn, 'r') as input_file:
        text = input_file.read()
        text_seq = text.split()

    with open('missing_words.txt', 'w') as output_file:
        for word in text_seq:
            if word not in cnt:
                print(word, file=input_file)
    print('done sanity check...')
