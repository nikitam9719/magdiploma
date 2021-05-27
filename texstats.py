import ast
import re
import string
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from typing import List
from nltk.stem.snowball import SnowballStemmer
#import spacy
import os.path
import os
import pickle
import collections


class PyHearst:
    '''PyHearst class.'''

    def __init__(self):
        '''
            if hypernym identifier == 0, the first NP is the hypernym
            if hypernym identifier == 1, the last NP is the hypernym
        '''

        self.patterns = [(

    '(NP_\\w+ (, )?такой как (NP_\\w+ ?(, )?(и |или )?)+)',
    0
),
    (
        '(такой NP_\\w+ (, )?как (NP_\\w+ ?(, )?(и |или )?)+)',
        0
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?другой NP_\\w+)',
        1
    ),
    (
        '(NP_\\w+ (, )?включающий (NP_\\w+ ?(, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?особенно (NP_\\w+ ?(, )?(и |или )?)+)',
        0
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?любой другой NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?некоторый другой NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?является NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?фактически является NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?являться NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?фактически являться NP_\\w+)',
        1
    ),
    (
        '(NP_\\w+ (, )?такие как (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?такая как (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?такое как (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?такой как (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        'такой (NP_\\w+ (, )?как (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?как другой NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?один из NP_\\w+)',
        1
    ),
    (
        'примеры (NP_\\w+ (, )?являются (NP_\\w+ ? '
        '(, )?(и |или )?)+)',
        0
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?являются примерами of NP_\\w+)',
        1
    ),
    (
        'пример (NP_\\w+ (, )?являться (NP_\\w+ ? '
        '(, )?(и |или )?)+)',
        0
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?являться пример of NP_\\w+)',
        1
    ),
    (
        '(NP_\\w+ (, )?например (, )?'
        '(NP_\\w+ ?(, )?(и |или )?)+)',
        0
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?которые называются NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?которые называются NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?который называться NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )?который называться NP_\\w+)',
        1
    ),
    (
        '(NP_\\w+ (, )?в основном (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?в основной (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?чаще всего (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?в частности (NP_\\w+ ? '
        '(, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?в частность (NP_\\w+ ? '
        '(, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?за исключением (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?за исключение (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?другой (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?например (, )?(NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '((NP_\\w+ ?(, )?)+(and |or )?которые похожи на NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(and |or )?похожие на NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(and |or )?который похожй на NP_\\w+)',
        1
    ),
    (
        '((NP_\\w+ ?(, )?)+(and |or )?похожий на NP_\\w+)',
        1
    ),
    (
        '(NP_\\w+ (, )отличный от (NP_\\w+ ? '
        '(, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?примером которых являются (NP_\\w+ ? '
        '(, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?по типу (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?пример который являться (NP_\\w+ ? '
        '(, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?по тип(NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '((NP_\\w+ ?(, )?)+(и |или )? NP_\\w+ тип)',
        1
    ),
    # (
    #     '(NP_\\w+ (, )?whether (NP_\\w+ ? (, )?(и |или )?)+)',
    #     0
    # ),
    (
        '(в сравнении (NP_\\w+ ?(, )?)+(и |или )?с NP_\\w+)',
        1
    ),
    (
        '(в сравнение (NP_\\w+ ?(, )?)+(и |или )?с NP_\\w+)',
        1
    ),
    (
        '(NP_\\w+ (, )?сравнивая с (NP_\\w+ ? (, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?среди -PRON- (NP_\\w+ ? '
        '(, )?(и |или )?)+)',
        0
    ),
    # (
    #     '((NP_\\w+ ?(, )?)+(и |или )?как NP_\\w+)',
    #     1
    # ),
    # (
    #     '(NP_\\w+ (, )? (NP_\\w+ ? (, )?(и |или )?)+ '
    #     'for instance)',
    #     0
    # ),
    (
        '((NP_\\w+ ?(, )?)+(и|или)? похожий на NP_\\w+)',
        1
    ),
    (
        '(NP_\\w+ (, )?которые могут включать в себя (NP_\\w+ '
        '?(, )?(и |или )?)+)',
        0
    ),
    (
        '(NP_\\w+ (, )?который может включать в себя (NP_\\w+ '
        '?(, )?(и |или )?)+)',
        0
    ),
        ]

        # self.tests = ['works by such individuals as Marti A. Hearst, P. J. Proudhon, and Esther Duflo and also foods such as pancakes, waffles, and eggs',
        #                  'bruises, wounds, bones, or other injuries',
        #                  'sports such as basketball and baseball',
        #                  'beans, such as pinto and kidney',
        #                  'temples, treasuries, and other buildings',
        #                  'countries, including Canada and England',
        #                  'countries, especially France, England, and Spain'
        #                 ]

    def annotate_sentence(self, sent: str) -> str:
        sentence=nltk.word_tokenize(sent,language="russian")
        # stemmer = SnowballStemmer("russian")
        # sentence_stem=list()
        # for word in sentence:
        #     sentence_stem.append(stemmer.stem(word))
        #
        # tagged_sent = nltk.pos_tag(sentence_stem,lang="rus")
        tagged_sent = nltk.pos_tag(sentence, lang="rus")
        NPs = set([tup[0] for tup in tagged_sent if tup[1].startswith('S')])
        for NP in NPs:
            sent = sent.replace(NP, 'NP_'+NP) #adds NP tag
        return self.merge_consecutive_NPs(sent)
    def annotate_sentence_no_merge(self, sent: str) -> str:
        sentence=nltk.word_tokenize(sent,language="russian")
        # stemmer = SnowballStemmer("russian")
        # sentence_stem=list()
        # for word in sentence:
        #     sentence_stem.append(stemmer.stem(word))
        #
        # tagged_sent = nltk.pos_tag(sentence_stem,lang="rus")
        tagged_sent = nltk.pos_tag(sentence, lang="rus")
        NPs = set([tup[0] for tup in tagged_sent if tup[1].startswith('S')])
        for NP in NPs:
            sent = sent.replace(NP, 'NP_'+NP) #adds NP tag
        return sent
    def merge_consecutive_NPs(self, annotated_sentence: str) -> str:


        toks = nltk.word_tokenize(annotated_sentence,language="russian")

        #merge initialed NPs to handle instances like J. K. Rowling
        for i in range(len(toks)-1, 0, -1):
            if toks[i] == '.' and i!= len(toks)-1:
                toks[i-1:i+1] = [toks[i-1] + toks[i]]

        NP_indices = [i for i in range(len(toks)) if toks[i].startswith('NP_')] #inidices of all NP_-tagged tokens

        #if two consecutive tokens are tagged NP_, then merge them into one token
        for i in range(len(NP_indices)-1, 0, -1):
            if NP_indices[i]-1 == NP_indices[i-1]:
                toks[NP_indices[i-1]:NP_indices[i]+1] = [toks[NP_indices[i-1]] +'_' + toks[NP_indices[i]][3:]]

        #untokenize and return:
        return ''.join([' '+tok if not tok.startswith('\'') and
                        tok not in string.punctuation else
                        tok for tok in toks]).strip()



    def extract_patterns(self, sent: str) -> List:

        annotated_sentence = self.annotate_sentence(sent)

        hyponym_relations = [] #format is tuples of form (hypernym, hyponym)
        for pattern in self.patterns:
            matches = re.findall(pattern[0], annotated_sentence) #get each instance of the regex pattern

            for match in matches:
                instance = match[0]

                NPs = [tok.replace('NP_', '').replace('_', ' ')
                       for tok in nltk.word_tokenize(instance)
                       if tok.startswith('NP_')]

                if NPs:
                    if pattern[1] == 0:
                        #the first NP is the hypernym
                        hypernym = NPs[0]
                    if pattern[1] == 1:
                        #the last NP is the hypernym
                        hypernym = NPs[len(NPs)-1]

                    hyponyms = [NP for NP in NPs if NP != hypernym]

                    # for hyponym in hyponyms:
                    #     if in_eng.singular_noun(hyponym)==False:
                    #         hyponym_relations.append(
                    #             (in_eng.singular_noun(hypernym), hyponym))
                    #     else:
                    #         hyponym_relations.append(
                    #             (in_eng.singular_noun(hypernym),
                    #             in_eng.singular_noun(hyponym)))
                    for hyponym in hyponyms:
                        hyponym_relations.append((hypernym,hyponym))

        return hyponym_relations

if __name__ == "__main__":
    a=PyHearst()
    result=list()
    path=os.argv[1]
    listfiles = os.listdir(path+"/"+'output_preproc')
    i=0
    iter=2
    with open(path +'/'+"index.txt", 'r', encoding='utf-8') as f:
        inv_index_data=f.read()
        f.close()
    # inv_index=pickle.load(open('index.txt','rb'))
    inv_index=ast.literal_eval(inv_index_data)
    for it in range(iter):
        for file in listfiles:
            # i = i + 1
            # if (i > 10):
            #     break
            with open(path+"/"+"output_preproc/"+file, 'r', encoding='utf-8') as f:
                ff=list()
                text=f.read()
                sentences=nltk.sent_tokenize(text,language="russian")
                for sent in sentences:
                #text=stemmer.stem(text)
                    data=a.extract_patterns(sent)
                    if len(data)==0:
                        continue
                    else:
                        ff=ff+data
            if len(ff)==0:
                continue
            else:
                for tup in ff:
                    result.append(list(tup))
        for hypair in result:
            word_hypo=hypair[0]
            word_hyper=hypair[1]
            word_hypo_list=word_hypo.split(' ')
            word_hyper_list=word_hyper.split(' ')
            if isinstance(word_hypo_list , str):
                word_hypo_list=list(word_hypo_list )
            if isinstance(word_hyper_list , str):
                word_hyper_list=list(word_hyper_list )
            if(nltk.pos_tag([word_hypo],lang='rus')[0][1]in ["SPRO","APRO"] or nltk.pos_tag([word_hyper],lang='rus')[0][1]in ["SPRO","APRO"]):
                continue
            common_docs=[]
            docs_hyper=[]
            docs_hypo=[]
            finalsethyper=set()
            finalsethypo=set()
            step=0
            for word1 in word_hyper_list:
                docs_hyper = []

                if(word1 not in inv_index):
                    finalsethyper=set()
                    break
                for tp in inv_index[word1]:
                    docs_hyper.append(tp)
                # docs_hyper.append(inv_index[word1])
                if len(finalsethyper)==0 and step==0:
                    finalsethyper=set(docs_hyper)
                    step=1
                else:
                    finalsethyper=finalsethyper.intersection(set(docs_hyper))
            step=0

            for word2 in word_hypo_list:
                docs_hypo = []
                if(word2 not in inv_index):
                    finalsethypo=set()
                    break
                for tp in inv_index[word2]:
                    docs_hypo.append(tp)
                # docs_hypo.append(inv_index[word2])
                if len(finalsethypo)==0 and step==0:
                    finalsethypo=set(docs_hypo)
                    step=1
                else:
                    finalsethypo=finalsethypo.intersection(set(docs_hypo))
            #docs_hyper=[item for item, count in collections.Counter(docs_hyper).items() if count > 1]
            finalset=finalsethyper.intersection(finalsethypo)
            if(len(finalset)==0):
                continue
            else:
                for doc in finalset:
                    with open(path+"/"+"output_preproc/" + doc[0], 'r', encoding='utf-8') as f:
                        text = f.read()
                        f.close()
                    sentences = nltk.sent_tokenize(text, language="russian")
                    cur_sent=sentences[doc[1]]
                    cur_sent=a.annotate_sentence(cur_sent)
                    word_list=nltk.word_tokenize(cur_sent,language="russian")
                    pos_word_list=nltk.pos_tag(word_list,lang="rus")
                    l = 0
                    word_hypo='NP_'+'_'.join(word_hypo_list)
                    word_hyper = 'NP_' + '_'.join(word_hyper_list)
                    mark1 = 0
                    mark2=0
                    for k in pos_word_list:
                        if mark1==1 and mark2==1:
                            break
                        if(word_hyper in k[0] and mark1==0):
                            hyper=l
                            mark1=mark1+1
                        if(word_hypo in k[0] and mark2==0):
                            hypo=l
                            mark2=mark2+1
                        l=l+1
                    if mark1!=1 or mark2!=1:
                        continue
                    maxindex=0
                    minindex=0
                    hyperlast=0
                    if(hyper<hypo):
                        minindex=hyper
                        maxindex=hypo
                        hyperlast=0
                    else:
                        maxindex=hyper
                        minindex=hypo
                        hyperlast=1
                    if(maxindex-minindex>4):
                        continue
                    if(maxindex-minindex==2 and (('CONJ' in pos_word_list[minindex+1][1] or 'PART' in pos_word_list[minindex+1][1]))):
                        continue
                    newpattern='('
                    if(hyperlast==0):
                        newpattern=newpattern+'NP_\\w+'
                    else:
                        newpattern=newpattern+'(NP_\\w+ ?(,)?(и | или)?)+'
                    counter=0
                    for i in range(minindex+1,maxindex):
                        if 'A' in pos_word_list[i][1] or 'NP' in pos_word_list[i][0] or 'NUM' in pos_word_list[i][1]or 'PUNCT' in pos_word_list[i][1]or 'PUNCT' in pos_word_list[i][1]:
                            continue
                        else:
                            newpattern=newpattern+' '+pos_word_list[i][0]
                            counter=counter+1
                    if(hyperlast==0):
                        newpattern=newpattern+' (NP_\\w+ ?(,)?(и | или)?)+'
                    else:
                        newpattern=newpattern+' NP_\\w+'
                    newpattern=newpattern+')'
                    newpatterntuple=(newpattern,hyperlast)
                    if counter<2:
                        continue
                    if(newpatterntuple not in a.patterns):
                        a.patterns.append(newpatterntuple)




    with open(path+"/"+"output.txt", 'w', encoding='utf-8') as f:
        for i in result:
           f.write(str(i)+'\n')

#ff=a.extract_patterns("вирусы такие как грипп, кокк")
    #print(ff)