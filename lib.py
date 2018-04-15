
# -*- coding: utf-8 -*-

import re
import io
import random
import codecs
import json
import sys

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def divide_text(paragraph):
    '''Dividing paragraph into sentences by punctuation.'''
    SentenceEnders = re.compile('[^,!?\\.]+[,!?\\.]')
    # Defining enders of sentence and excluding short terms.
    SentenceList = SentenceEnders.findall(paragraph)
    # Spliting paragraph into sentences.
    output = list()
    for i in range(0,len(SentenceList)):
        if i == len(SentenceList)-1:
            output.append(SentenceList[i])
        else:
            if len(SentenceList[i]) + len(SentenceList[i+1]) < 30:
                output.append(SentenceList[i]+SentenceList[i+1])
            else:
                output.append(SentenceList[i])
    return [x.strip() for x in output]
    # Returning list of sentences


def find_phrase(text, search):
    '''Matching a phrase in sentence. Phrase could be made with multiple words.'''
    result = re.findall('\\b' + search.lower().decode("utf-8") +
                        '\\b', text.lower().decode("utf-8"), flags=re.UNICODE)
    # Finding searched phrase in text after decoding it into UNICODE and making it lower.
    if len(result) > 0:
        return True
    else:
        return False
    # If function finds a word (based on length of result) into sentence returns True.
    # Otherweis returns False.


def instance_tag(sentence):
    '''Finding and cheks if the tag is annotated in json file'''
    if '#' in sentence:
        x1 = sentence.find('#')
        x2 = 0
        for i in range(x1, len(sentence), 1):
            if sentence[i] == ' ' or sentence[i] in ['.', ',', '!', '?']:
                x2 = i
                break
            else:
                pass
        # Finding numbers of position of tag in text.

        x3 = sentence[x1:x2]
        return x3
        # Picking and returning a tag
    else:
        return False
        # If symbol # is not found returns Falser

def find_tag(sentence,tags_file):

    with open(tags_file) as g:
        tags = json.load(g,encoding='utf-8')

    tag_names = tags['tags'].keys()
    found_tag = str()
    priority = len(tags['tags'].keys())
    for i in tag_names:
        words = tags['tags'].get(i).get('words')
        for n in words:
            if find_phrase(sentence,n.encode('utf-8')) == True:
                if tags['tags'].get(i).get('priority') < priority :
                    found_tag = i
                    priority = tags['tags'].get(i).get('priority')
    return found_tag

def embed_tag(config_file,tag,sentence,position):
    with open(config_file,'r+') as f:
        config = json.load(f,encoding='utf-8')
    if position == 0:
        viable_tags = config['tags'].get('standing_tags')
    else:
        viable_tags = config['tags'].get('sitting_tags')

    if tag not in viable_tags.keys():
        print('Not viable tag.')
        return EOFError

    for i in viable_tags:
        if tag == i:
            if type(viable_tags.get(i))==list:
                movement = random.choice(viable_tags.get(i))
            else:
                movement = viable_tags.get(i)
            break
    
    
