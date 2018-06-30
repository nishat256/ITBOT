from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from docParser import readSampleInputDoc1 , readSampleInputDoc3 ,readSampleInput,dataForSampleInputDoc2FromDB
import nltk
import math
import sys
from tinydb import TinyDB, Query
db = TinyDB('db.json')

lookUpDict = {'email':['mail'],'turn on':['switch on','power on','power up']}
wordnet_lemmatizer=WordNetLemmatizer()
tokenizer=RegexpTokenizer(r'\w+')
def lemmatizeList(LystOfWords):
	newLyst=[]
	for word,tag in nltk.pos_tag(LystOfWords):
		if tag.startswith('NN'):
			word=wordnet_lemmatizer.lemmatize(word,pos='n')
		elif tag.startswith('VB'):
			word=wordnet_lemmatizer.lemmatize(word,pos='v')
		elif tag.startswith('JJ'):
			word=wordnet_lemmatizer.lemmatize(word,pos='a')
		else:
			word=wordnet_lemmatizer.lemmatize(word)
		newLyst.append(word)
	return newLyst
def textPreprocessing(text,flag=False):
	stopWords=set(stopwords.words('english')) - {'on','not','up'}
	tokenizedLyst=tokenizer.tokenize(text.lower())
	newLyst=[word  for word in tokenizedLyst if word not in stopWords]
	lemmatizedLyst=lemmatizeList(newLyst)
	if not lemmatizedLyst:
		print("hello")
	bigramLyst=list(nltk.bigrams(lemmatizedLyst))
	
	if flag:
		for key,value in lookUpDict.items():
			for word in value:
				if len(word.split())==1:
					if word in lemmatizedLyst:
						lemmatizedLyst[lemmatizedLyst.index(word)]=key
						bigramLyst=list(nltk.bigrams(lemmatizedLyst))

				else:
					if tuple(word.split()) in bigramLyst:
						lemmatizedLyst[lemmatizedLyst.index(word.split()[0])]=key.split()[0]
						lemmatizedLyst[lemmatizedLyst.index(word.split()[1])]=key.split()[1]
						bigramLyst=list(nltk.bigrams(lemmatizedLyst))
	return (lemmatizedLyst,bigramLyst)
	
def return_count_of_documents_contain_specific_word(word,QAwiseFrequency):
	num=0
	for doc,answer in QAwiseFrequency:
		if word in doc:
			num+=1
	return num
def TF_IDF(text):
	lystOfQA3=readSampleInput()
	lystOfQA1=readSampleInputDoc1()
	lystOfQA2=readSampleInputDoc3()
	lystOfQA4=dataForSampleInputDoc2FromDB()
	lystOfQA=lystOfQA1 + lystOfQA2 + lystOfQA3+lystOfQA4
	QAwiseFrequency=[]
	for item in lystOfQA:
		question=item['Question'].lower()
		answer=item['Answer'].lower()
		Ques=textPreprocessing(question)
		Ques=Ques[0]+Ques[1]
		#Ans=textPreprocessing(answer)
		#Ans=Ans[0]+Ans[1]
		QAdict={}
		for word in (Ques):
			if word in QAdict:
				QAdict[word]+=1
			else:
				QAdict[word]=1

		QAwiseFrequency.append((QAdict,answer))
	processedText=textPreprocessing(text,True)
	processedText=processedText[0] + processedText[1]
	bestScore=0
	topFourAnswer=[[0,''] for x in range(4)]

	for QADict ,answer in QAwiseFrequency:
		totalNumOfWordsInDoc=sum(QADict.values())
		weightageOfWord=0
		for word in processedText:
			if word in QADict:
				tf=QADict[word]/float(totalNumOfWordsInDoc)
				num=return_count_of_documents_contain_specific_word(word,QAwiseFrequency)
				idf=math.log(len(QADict)/num)
				tf_idf=tf * idf
				weightageOfWord+=tf_idf
		if bestScore < weightageOfWord:
			bestScore=weightageOfWord
			response=answer
		for item in enumerate(topFourAnswer):
			index=item[0]
			if item[1][0] < weightageOfWord:
				topFourAnswer.insert(index,[weightageOfWord,answer])
				topFourAnswer=topFourAnswer[:4]
				break

	'''
	if bestScore==0:
		#sys.exit()
		return "Sorry, I don't have an answer"
	else:
		return response
	'''
	#print(topFourAnswer)
	rating=['Most Relevant','Relevant','Less Relevant','Least Relevant']
	print(topFourAnswer)
	for item in enumerate(topFourAnswer[:]):
		if item[1][0]==0:
			topFourAnswer.remove(item[1])
			continue
		topFourAnswer[item[0]][0]=rating[item[0]]
	return topFourAnswer
def queryDataBase(text):
	resp=db.all()
	uniPlusBimax=0
	uniMax=0
	bigramMax=0
	biAnswer=None
	uniAnswer=None
	(queryUni,queryBi)=textPreprocessing(text,True)
	for item in resp:
		questionUni,questionBi=textPreprocessing(item['Question'],True)
		wordMatched=0
		for word in queryUni:
			if word in questionUni:
				wordMatched+=1
		bigramMatched=0
		for bigram in queryBi:
			if bigram in questionBi:
				bigramMatched+=1
		per=float(wordMatched)/len(queryUni)
		#print(wordMatched,bigramMatched,per)
		'''
		if bigramMatched==0:
			if uniMax < per:
				uniMax = per
				uniAnswer = item['Answer']
		else:
			'''
		if uniPlusBimax < per and bigramMax <= bigramMatched:
			uniPlusBimax = per
			bigramMax = bigramMatched
			biAnswer = item['Answer']
	if bigramMax >= 1 and uniPlusBimax >= .6: 
		return (biAnswer,uniPlusBimax)
	else:
		return False









if __name__=='__main__':
	while True:
		question=input('Enter Here:')
		response=queryDataBase(question)
		print('Ans:',response)