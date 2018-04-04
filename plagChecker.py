from __future__ import division

import string

from plag import plagiarismCheck
import codecs
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem import PorterStemmer

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def preProcessing(text,flag=True):
    text=text.lower()
    a=stopwords.words('english')
    stopWords=set(a)

    words=word_tokenize(text)
    print words
    result = []

    if flag:
        for item in words:
            if item not in stopWords:
                result.append(item)
        fil=str(result)
    else:
        result

    repstr=" " * 32
    table=string.maketrans(string.punctuation,repstr)
    s=fil.translate(table)

    lemmatizer=WordNetLemmatizer()
    h=lemmatizer.lemmatize(s)

    wordss=word_tokenize(h)
    ps=PorterStemmer()
    list1=[]
    for i in wordss:
        k=(ps.stem(i))
        list1.append(k)

    final= ' '.join(list1)
    finall=str(final)
    finallstr=''
    sanwrd = 'u'
    splitfinall = finall.split()
    for wrd in splitfinall:
        if wrd != sanwrd:
            finallstr += str(wrd)+str(' ')
    finallstr=str(finallstr)

    return finallstr

def plagCheck(file_list,inputFile):

    fileLastIndex=[]
    combinedFile=''
    inputText=''
    for file in file_list:
        with codecs.open(str(file), 'r', encoding='utf-8', errors='ignore') as rd:
            originalFile = rd.read()
            combinedFile= combinedFile+originalFile+'\n'
            fileLastIndex.append((len(combinedFile.split()),file))

    with codecs.open(str(inputFile), 'r', encoding='utf-8', errors='ignore') as rd:
        inputText = rd.read()

    plagiarismCheck(inputText, combinedFile,fileLastIndex)

if __name__ == "__main__":
    from sys import argv
    plagCheck(argv[1:-1], argv[-1])
