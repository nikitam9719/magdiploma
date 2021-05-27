#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import string
import sys

from tika import parser # pip install tika
from pylatexenc import latex2text
import re
import nltk
from nltk.tag import PerceptronTagger
import itertools
import os
import re
import pymorphy2
from nltk.corpus import stopwords


def build_index(path):
    inv_index = dict()
    listfiles = os.listdir(path+"/"+"output_preproc")
    stop_symbols = string.ascii_lowercase + '0123456789'
    for file in listfiles:
        with open(path+"/" +"output_preproc/"+ file, 'r', encoding='utf-8') as f:
            data = f.read()
            f.close()
            sentences = nltk.sent_tokenize(data, language="russian")
            i = 0
            for sent in sentences:
                words = nltk.word_tokenize(sent, language="russian")
                for word in words:

                    if (word in stopwords.words("russian") or word in string.punctuation or any(
                            (c in stop_symbols) for c in word)):
                        continue
                    else:
                        if word not in inv_index:
                            inv_index[word] = [(file, i)]
                        else:
                            data = inv_index[word]
                            if (file, i) in data:
                                continue
                            else:
                                inv_index[word].append((file, i))
                i = i + 1
    with open(path +'/'+"index.txt", 'w', encoding='utf-8') as f:
        f.write(str(inv_index))
    # with open('04-4-2001.tex', 'r',encoding='utf-8') as f:
    #     text=f.read()
    #     test=latex2text.LatexNodes2Text().latex_to_text(text)
    #     print (test)
    # with open('input.txt','w',encoding='utf-8') as f:
    #     f.write(test)
    # for i in range(600):
    #     if(i==0 or i==25 or i==139):
    #         continue
    #     raw = parser.from_file(str(i)+'.pdf')
    #     with open(str(i)+'.txt', 'w',encoding='utf-8') as f:
    #         if raw['content'] is None:
    #             f.close()
    #             continue
    #         f.write(raw['content'].replace('-','').replace('\n',''))
    #         f.close()
    # print(raw['content'])
    # pos_tagger = PerceptronTagger()
    # #sentences = nltk.sent_tokenize(raw['content'])
    # sentences = nltk.sent_tokenize(raw['content'],language="russian")
    # sentences = [nltk.word_tokenize(sent,language="russian") for sent in sentences]
    # sentences = [nltk.pos_tag(sent,lang="rus") for sent in sentences]
    # print(sentences)


if __name__ == "__main__":
    inv_index=dict()
    listfiles=os.listdir(sys.argv[1])
    morph = pymorphy2.MorphAnalyzer()
    for file in listfiles:
        if file=='output_preproc':
            continue
        with open(sys.argv[1]+"/"+file, 'r', encoding='utf-8') as f:
            data=f.read()
            f.close()
        with open(sys.argv[1]+"/"+"output_preproc/"+file+'output', 'w', encoding='utf-8') as f:
            # data=re.sub(r"\$\$.+\$\$",' ',data)
            # data=re.sub(r"\$.+\$",' ',data)
            test = latex2text.LatexNodes2Text(math_mode='remove').latex_to_text(data)
            sentences=nltk.sent_tokenize(test,language="russian")
            text=''
            for sent in sentences:
                words = nltk.word_tokenize(sent, language="russian")
                parsed_sent=''
                for word in words:
                    p=morph.parse(word)[0]
                    parsed_sent=parsed_sent+p.normal_form+' '

                text=text+parsed_sent
            f.write(text)
    build_index(sys.argv[1])
