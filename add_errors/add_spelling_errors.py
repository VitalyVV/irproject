import random
import string
from corpus_util import loadDict, loadDict_std
import pickle


alphabet_list = list(string.ascii_lowercase)
alphabet_list.append(' ')


def readTag(fn):
    TARGET_TAG_SET = ["V", "N", "A"]
    f = open(fn, "r")
    lines = f.readlines()
    selected_inds = []
    selected_words = []
    tok_sent = []
    for line in lines:
        try:
            sent, tag, score, orig_sent = line.strip().split("\t")
        except Exception:
            continue
        tag_seq = tag.split()
        sent_seq = sent.split()
        inds = [
            ind for ind in range(len(tag_seq))
            if tag_seq[ind] in TARGET_TAG_SET]
        selected_inds.append(inds[:])
        words = [sent_seq[ind] for ind in inds]
        selected_words.append(words[:])
        tok_sent.append(sent)
        # if (len(selected_words) >= 2):
        #    break
    return selected_inds, selected_words, tok_sent


def load_toxic_word(fn):
    """Load a list of (toxic_score, sentence, most_toxic_word)"""
    with open(fn, "rb") as handle:
        Sentence_And_Toxic_Word = pickle.load(handle)
    return Sentence_And_Toxic_Word


def add_character(word, char=None):
    """Change a word by adding a random character to it

    :param word: A word to change
    :param char: A character to add or None to let the function choose randomly

    :return: A changed word
    """
    pos = random.randint(0, len(word))
    word1 = word[0:pos]
    word2 = word[pos:len(word)]
    add = char or random.choice(alphabet_list)
    return word1 + add + word2


def delete_character(word):
    """Change a word by deleting a single character in it

    :param word: A word to change

    :return: A changed word
    """
    pos = random.randint(0, len(word) - 1)
    word1 = word[0:pos]
    word2 = word[pos + 1:len(word)]
    return word1 + word2


def change_character(word, char=None):
    """Change a word by replacing a character in it with another one

    :param word: A word to change
    :param char: A replacement character or None to let the function choose
        randomly

    :return: A changed word
    """
    pos = random.randint(0, len(word) - 1)
    word1 = word[0:pos]
    word2 = word[pos + 1:len(word)]
    change = word[pos]
    possible_changes = [char for char in alphabet_list if char != change]
    change = char or random.choice(possible_changes)
    return word1 + change + word2


def permute_characters(word):
    """Change a word by permuting two adjacent characters in it

    :param word: A word to change

    :return: A changed word
    """
    if len(word) <= 1:
        return word
    else:
        pos = random.randint(0, len(word) - 2)
        word1 = word[0:pos]
        word2 = word[pos + 2:len(word)]
        return word1 + word[pos + 1] + word[pos] + word2


def separate_characters(word):
    """Change a word by separating all of its characters with whitespaces

    :param word: A word to change

    :return: A changed word
    """
    return ' '.join(word)


def change_a_word_dis1(word):
    """A method to change a word that maintains edit distance 1

    input:
        word - the input word
    output:
        modified_word - a word that has edit distance 1 from the input word
    """
    method = random.randint(0, 2)
    if method == 0:
        return add_character(word)
    elif method == 1:
        return delete_character(word)
    else:  # method == 2
        return change_character(word)


def change_a_word_5_ways(word):
    """A method to change a word that randomly picks one of
        {
            add 1 char,
            delete 1 char,
            replace 1 char,
            permute 2 adjacent chars,
            separate all chars with ' '
        }.

    input:
        word - the input word
    output:
        modified_word - a word that has edit distance 1 from the input word
        method - the method used to modify. (0 - add, 1 - delete, 2 - replace,
            3 - permute, 4 - separate)
    """
    method = random.randint(0, 4)
    if method == 0:
        return add_character(word), 0
    elif method == 1:
        return delete_character(word), 1
    elif method == 2:
        return change_character(word), 2
    elif method == 3:
        return permute_characters(word), 3
    else:  # method == 4
        return separate_characters(word), 4


def change_a_word_5_ways_invalid(word):
    cnt = loadDict()

    method = random.randint(0, 4)
    ret_word_and_method = ('', -1)
    count = 0
    ret_flag = False

    while not ret_flag and count < 10:
        count = count + 1

        if method == 0:
            ret_word_and_method = (add_character(word), 0)
        elif method == 1:
            ret_word_and_method = (delete_character(word), 1)
        elif method == 2:
            ret_word_and_method = (change_character(word), 2)
        elif method == 3:
            ret_word_and_method = (permute_characters(word), 3)
        else:  # method == 4
            ret_word_and_method = (separate_characters(word), 4)

        if (cnt[ret_word_and_method[0]] == 0):
            ret_flag = True
        else:
            # Do not use method = 4 more than once
            method = random.randint(0, 3)

    return ret_word_and_method


def change_a_word_5_ways_invalid_v2(word):
    cnt = loadDict()

    method = random.randint(0, 3)
    ret_word_and_method = ('', -1)
    count = 0
    ret_flag = False

    while not ret_flag and count < 10:
        count = count + 1

        # TODO: Add logging if ret_word_and_method[0] == ''
        if method == 0:
            ret_word_and_method = (add_character(word), 0)
        elif method == 1:
            if len(word) < 8:
                # Do not delete characters unless a word has length 8 or more
                method = random.choice([0, 2, 3, 4])
                continue
            ret_word_and_method = (delete_character(word), 1)
        elif method == 2:
            ret_word_and_method = (change_character(word), 2)
        else:  # method == 3
            ret_word_and_method = (permute_characters(word), 3)

        if (cnt[ret_word_and_method[0]] == 0):
            ret_flag = True
        else:
            method = random.randint(0, 3)

    if not ret_flag and count >= 10:
        if ret_word_and_method[1] == 0:
            ret_word_and_method = (add_character(word, char='*'), 0)
        elif ret_word_and_method[1] == 2:
            ret_word_and_method = (change_character(word, char='*'), 2)

    if ret_word_and_method[1] == -1:
        if len(word) >= 8:
            ret_word_and_method = (delete_character(word), 1)
        else:
            ret_word_and_method = (add_character(word, char='*'), 0)

    # TODO: Log here also
    return ret_word_and_method


def change_a_word_5_ways_invalid_v2_force_method(word, method):
    cnt = loadDict()

    ret_word_and_method = ('', -1)
    count = 0
    ret_flag = False
    while not ret_flag and count < 10:
        count = count + 1

        # TODO: Add logging if ret_word_and_method[0] == ''
        if method == 0:
            ret_word_and_method = (add_character(word), 0)
        elif method == 1:
            if len(word) < 8:
                raise ValueError(
                    f'The word {word} is too short ({len(word)})'
                    ' to use delete method')
            ret_word_and_method = (delete_character(word), 1)
        elif method == 2:
            ret_word_and_method = (change_character(word), 2)
        else:  # method == 3
            ret_word_and_method = (permute_characters(word), 3)

        if (cnt[ret_word_and_method[0]] == 0):
            ret_flag = True

    if not ret_flag and count >= 10:
        if ret_word_and_method[1] == 0:
            ret_word_and_method = (add_character(word, char='*'), 0)
        elif ret_word_and_method[1] == 2:
            ret_word_and_method = (change_character(word, char='*'), 2)

    if ret_word_and_method[1] == -1:
        if len(word) >= 8:
            ret_word_and_method = (delete_character(word), 1)
        else:
            ret_word_and_method = (add_character(word, char='*'), 0)

    # TODO: Log here also
    return ret_word_and_method


def modify_one_word_dis1(sentence, words_list):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p, '')
    words_in_sentence = s_wo_punctuation.split()
    # print(words_in_sentence)
    modified_sentences = list()
    # print(words_list)
    for word in words_list:
        # Note that Python by default passes by reference
        new_words_in_sentence = words_in_sentence[:]
        # print(new_words_in_sentence)
        indices = [i for i, x in enumerate(words_in_sentence) if x == word]
        # print(indices)
        for i in indices:
            # print(new_words_in_sentence[i])
            new_words_in_sentence[i] = change_a_word_dis1(
                new_words_in_sentence[i])
            # print(new_words_in_sentence[i])
        new_sentence = ''
        for w in new_words_in_sentence:
            new_sentence = new_sentence + w + ' '
        modified_sentences.append(new_sentence)
    return modified_sentences


def modify_one_word_5_ways(sentence, Words_List):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p, '')
    Words_In_Sentence = s_wo_punctuation.split()
    # print(Words_In_Sentence)
    Modified_Sentences = []
    # print(Words_List)
    for word in Words_List:
        # Note that Python by default passes by reference
        New_Words_In_Sentence = Words_In_Sentence[:]
        # print(New_Words_In_Sentence)
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        # print(Indices)
        method = -1
        for i in Indices:
            # print(New_Words_In_Sentence[i])
            # print(type(New_Words_In_Sentence))
            # s = New_Words_In_Sentence
            # print('s=',s)
            New_Words_In_Sentence[i], method = change_a_word_5_ways(
                New_Words_In_Sentence[i])
            # print(New_Words_In_Sentence[i])
        new_sentence = ''
        for w in New_Words_In_Sentence:
            new_sentence = new_sentence + w + ' '
        Modified_Sentences.append([new_sentence, method])
    return Modified_Sentences


def modify_one_word_5_ways_invalid(sentence, Words_List):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p, '')
    Words_In_Sentence = s_wo_punctuation.split()

    Modified_Sentences = []

    for word in Words_List:
        for p in list(string.punctuation):
            word = word.replace(p, '')
        # Note that Python by default passes by reference
        New_Words_In_Sentence = Words_In_Sentence[:]
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        if (len(Indices) > 0):
            method = -1
            for i in Indices:
                New_Words_In_Sentence[i], method = change_a_word_5_ways_invalid(
                    New_Words_In_Sentence[i])
            new_sentence = ''
            for w in New_Words_In_Sentence:
                new_sentence = new_sentence + w + ' '
            Modified_Sentences.append([
                new_sentence, method, word, New_Words_In_Sentence[Indices[0]]])
    return Modified_Sentences


def modify_one_word_5_ways_invalid_v2(sentence, Words_List):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p, '')
    Words_In_Sentence = s_wo_punctuation.split()

    Modified_Sentences = []

    for word in Words_List:
        for p in list(string.punctuation):
            word = word.replace(p, '')
        # Note that Python by default passes by reference
        New_Words_In_Sentence = Words_In_Sentence[:]
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        if (len(Indices) > 0):
            method = -1
            for i in Indices:
                New_Words_In_Sentence[i], method = (
                    change_a_word_5_ways_invalid_v2(New_Words_In_Sentence[i]))
            new_sentence = ''
            for w in New_Words_In_Sentence:
                new_sentence = new_sentence + w + ' '
            Modified_Sentences.append([
                new_sentence, method, word,
                [New_Words_In_Sentence[i] for i in Indices]])
    return Modified_Sentences


def modify_one_word_5_ways_invalid_v2_force_method(sentence, Words_List,
                                                   method):
    s_wo_punctuation = sentence
    for p in list(string.punctuation):
        s_wo_punctuation = s_wo_punctuation.replace(p, '')
    Words_In_Sentence = s_wo_punctuation.split()

    Modified_Sentences = []

    for word in Words_List:
        for p in list(string.punctuation):
            word = word.replace(p, '')
        # Note that Python by default passes by reference
        New_Words_In_Sentence = Words_In_Sentence[:]
        Indices = [i for i, x in enumerate(Words_In_Sentence) if x == word]
        if (len(Indices) > 0):
            for i in Indices:
                New_Words_In_Sentence[i], method = (
                    change_a_word_5_ways_invalid_v2_force_method(
                        New_Words_In_Sentence[i], method))
            new_sentence = ''
            for w in New_Words_In_Sentence:
                new_sentence = new_sentence + w + ' '
            Modified_Sentences.append([
                new_sentence, method, word,
                [New_Words_In_Sentence[i] for i in Indices]])
    return Modified_Sentences


def modify_key_words_5_ways_readTag(indices, sentence):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list))  # unique
    Modified_Sentences = modify_one_word_5_ways(sentence, selected_word_list)
    # print(Modified_Sentences)
    Modified_Sentences_And_Words = [
        [
            Modified_Sentences[i][0],
            Modified_Sentences[i][1],
            selected_word_list[i]
        ]
        for i in range(len(selected_word_list))
    ]
    # print(Modified_Sentences_And_Words)
    return Modified_Sentences_And_Words


def modify_key_words_5_ways_readTag_invalid(indices, sentence):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list))  # unique
    Modified_Sentences = modify_one_word_5_ways_invalid(
        sentence, selected_word_list)
    # print(Modified_Sentences)
    Modified_Sentences_And_Words = []
    for i in range(len(selected_word_list)):
        try:
            Modified_Sentences_And_Words.append([[
                Modified_Sentences[i][0],
                Modified_Sentences[i][1],
                selected_word_list[i],
                Modified_Sentences[i][3]]])
        except Exception:
            print(('len(Modified_Sentences) < 4:', i))
    # print(Modified_Sentences_And_Words)
    return Modified_Sentences_And_Words


def modify_key_words_5_ways_readTag_invalid_v2(indices, sentence):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list))  # unique
    Modified_Sentences = modify_one_word_5_ways_invalid_v2(
        sentence, selected_word_list)
    # print(Modified_Sentences)
    Modified_Sentences_And_Words = []
    for i in range(len(selected_word_list)):
        try:
            Modified_Sentences_And_Words.append([
                Modified_Sentences[i][0],
                Modified_Sentences[i][1],
                selected_word_list[i],
                Modified_Sentences[i][3]])
        except Exception:
            print(('len(Modified_Sentences) < 4:', i))
    # print(Modified_Sentences_And_Words)
    return Modified_Sentences_And_Words


def modify_key_words_5_ways_readTag_invalid_v2_force_method(indices,
                                                            sentence,
                                                            method):
    Words_In_Sentence = sentence.split()
    selected_word_list = [Words_In_Sentence[i] for i in indices]
    selected_word_list = list(set(selected_word_list))  # unique
    Modified_Sentences = modify_one_word_5_ways_invalid_v2_force_method(
        sentence, selected_word_list, method)
    # print(Modified_Sentences)
    Modified_Sentences_And_Words = []
    for i in range(len(selected_word_list)):
        try:
            Modified_Sentences_And_Words.append([
                Modified_Sentences[i][0],
                Modified_Sentences[i][1],
                selected_word_list[i],
                Modified_Sentences[i][3]])
        except Exception:
            print(('len(Modified_Sentences) < 4:', i))
    # print(Modified_Sentences_And_Words)
    return Modified_Sentences_And_Words
