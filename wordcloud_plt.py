# -*- coding: utf-8 -*-
# @Date:   2018-08-02 17:47:35
# @Last Modified time: 2018-09-06 15:32:28


from collections import defaultdict
import os
import re
from wordcloud import WordCloud
import pandas as pd
import nltk
import string
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
# from nltk.collocations import BigramCollocationFinder
from nltk.corpus import stopwords
# from nltk.metrics import BigramAssocMeasures
import matplotlib.pyplot as plt


__author__ = 'Jefferson'

def plot_wc(wordDict):
	"""这是绘制词云的函数
	
	Arguments:
		wordDict {dictionary} -- 含有词频统计的Freqdist
	"""
	wc = WordCloud(
		background_color='white',
		width=600,
		height=450,
		relative_scaling=0.45,
	)
	wc.generate_from_frequencies(wordDict)
	# 以下注释代码是为了在本地程序运行时查看效果图，最终是输出为png格式图
	# wc.generate(wordDict)
	# plt.imshow(wc)
	# plt.axis('off')
	wc.to_file('wordCloud.png')

def main():
	stop_words = [
		'problem',
		'occur',
		'resolve',
		'log',
		'often',
		'request',
		'previous',
		'first',
		'steps',
		'taken',
		'device',
		'se',
		'x',
		'hw',
		'ht',
		'hotline',
		'time',
		'specified',
		'always',
		'yes',
		'customer',
		'today',
		'n/a',
		'called',
		'rcr',
		'translation',
		'yse/no',
		'pi',
		'rs',
		'sr',
		'cu',
		'hi'
	]
	filterWords = []
	# 最终有价值的词一般为形容词、专有名词和名词短语
	reserved_tags = [
		'JJ',
		# 'JJR',
		'NN',
		# 'NNS',
		'NNP'
	]
	# 读取excel表格的数据
	try:
		questionReader = pd.read_excel("germany_procedure.xlsx")
		# detailReader = pd.read_excel("bussiness_Month_detail.xlsx")
	except Exception as e:
		raise e
		print("excel file read failed! please debug!")
	finally:
		print("excel file read successfully!")
	punctuations = string.punctuation
	# 德语停用词
	# stopWords_ger = set(stopwords.words('german'))
	# 英语停用词
	stopWords_eng = list(stopwords.words('english'))
	# stopWords_eng.extend(filted_words)
	questions = questionReader['procedure']
	# products = detailReader['产品线']
	for idx in range(len(questionReader) - 1):
		wordsList = word_tokenize(questions[idx])
		
		word_filter = lambda x: x.lower() in stopWords_eng or x[0] in punctuations
		reg_filter = lambda x: re.search('\d{2}.\d{2}.\d{4}', x)
		tag_filter = lambda x: x in reserved_tags
		
		words = [word.lower() for word in wordsList if not word_filter(word)]
		words = [word for word in words if not reg_filter(word)]
		text_tags = nltk.pos_tag(words)
		words = [word[0] for word in text_tags if tag_filter(word[1])]
		filterWords.extend(words)
		# finder = BigramCollocationFinder.from_words(tokenized_words)
		# finder.apply_word_filter(word_filter)
		# scored = finder.score_ngrams(BigramAssocMeasures.raw_freq)
		# print(sorted(bigram for bigram, score in scored))
		# 获取bigram词组
		# print('index={:},words={:}'.format(idx, words))
		# eng_dict[prod_name].extend(word_set)
	 
	wordFredist= nltk.Text(filterWords)
	wordFredist = nltk.FreqDist(wordFredist)
	for stopW in stop_words:
		if stopW in wordFredist:
			wordFredist.pop(stopW)
	# wordFreq = pd.DataFrame(wordFredist)
	# writer = pd.ExcelWriter('output.xlsx')
	# wordFreq.to_excel(writer)
	# writer.save()

	plot_wc(wordFredist)

	
	
if __name__ == '__main__':
	main()
