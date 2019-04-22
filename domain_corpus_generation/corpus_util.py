"""
construct dictionary
"""
from nltk import word_tokenize
from collections import Counter
import pickle
from twokenize import tokenize

# TODO: Add logging instead of prints


def readWikiVocab(fn="vocab.txt"):
    with open(fn, 'r') as input_file:
        cnt = Counter()
        for line in input_file:
            word, freq = line.strip().split()
            cnt[word] += int(freq)
    return cnt


def pythonTokenizeText(fn, output_fn):
    with open(fn, 'r') as input_file:
        input_file = open(fn, "r")
        tok_lines = []
        for line in input_file:
            tok_seq = word_tokenize(line.strip().lower().decode('utf8'))
            tok_line = ' '.join(tok_seq)
            tok_lines.append(tok_line)

    with open(output_fn, 'w') as output_file:
        tok_text = '\n'.join(tok_lines)
        print(tok_text.encode("utf8"), file=output_file)
    print('done processing train text...')


def twitterTokenizeText(fn, output_fn):
    with open(fn, 'r') as input_file:
        tok_lines = []
        for line in input_file:
            line = line.strip().lower().decode('utf8')
            line = line.replace('`', ' ')
            tok_seq = tokenize(line)
            tok_line = ' '.join(tok_seq)
            tok_lines.append(tok_line)

    with open(output_fn, 'w') as output_file:
        tok_text = '\n'.join(tok_lines)
        print(tok_text.encode('utf8'), file=output_file)
    print('done twitter tokenizing text....')


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


def loadDict(fn='dict.pickle', freq_threshold=6):
    with open(fn, 'rb') as handle:
        cnt = pickle.load(handle)
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


if __name__ == "__main__":
    # tokenize train and test data
    # pythonTokenizeText('train.txt', 'tok_train.txt')
    # pythonTokenizeText('test.txt', 'tok_test.txt')
    twitterTokenizeText('train.txt', 'norm_train.txt')
    twitterTokenizeText('test.txt', 'norm_test.txt')

    # load dictionary
    # dumpDict('tok_train.txt')
    # sanityCheck()
