# encoding=utf8  
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

import re
import xlsxwriter

import sys
import os

import acadRelaSpider

reload(sys)
sys.setdefaultencoding('utf8')

class AcadRelaSpider(scrapy.Spider):
	name = "acadRelaTroubleShoot"
	allowed_domains = acadRelaSpider.AcadRelaSpider.allowed_domains
	start_urls = [

"http://www.sciencedirect.com/science/article/pii/S0306261998000117",


	]
	journalTitle = acadRelaSpider.AcadRelaSpider.journalTitle
	prefix = acadRelaSpider.AcadRelaSpider.prefix

	def __init__(self):

		# wbr_data = xlrd.open_workbook('data_'+self.journalTitle+'.xlsx')
		# shr_data = wbr_data.sheet_by_name('data')
		# self.existingPaperNum = shr_data.cell_value(0, 1)

		self.existingPaperNum = 0

		self.wb_data = xlsxwriter.Workbook('data_2_'+self.journalTitle+'.xlsx')
		self.sh_data = self.wb_data.add_worksheet('data')

		# write journal data sheet title
		self.sh_data.write(0, 0, 'paperAmount')
		self.sh_data.write(0, 1, self.existingPaperNum)
		self.sh_data.write(2, 0, 'paperLabel')
		self.sh_data.write(2, 1, 'pageWebLink')
		self.sh_data.write(2, 2, 'paperTitle')
		self.sh_data.write(2, 3, 'journalTitle')
		self.sh_data.write(2, 4, 'journalVol')
		self.sh_data.write(2, 5, 'journalDate')
		self.sh_data.write(2, 6, 'journalPage')
		self.sh_data.write(2, 7, 'journalDOILink')
		self.sh_data.write(2, 8, 'journalKeywords')
		self.sh_data.write(2, 9, 'validPaper?')
		self.sh_data.write(2, 10, 'authorNumber')
		for i in xrange(10):
			self.sh_data.write(2, i+11, 'author'+str(i)+'\nfirstName\nlastName\naffiliation\nemail\n')

		if os.path.exists('errorLink2.txt'):
			os.remove('errorLink2.txt')

	# this is used to parse paper page and return useful data
	def parse(self, response):
		try:
			stage = 0
			# fw = file('test.txt', 'a')

			# fw.write('\nparse_paper\n')
			data = {
			'paperLabel': 0,
			'pageWebLink': '',
			'paperTitle': '',
			'journalTitle': '',
			'journalVol': 0,
			'journalDate': '',
			'journalPage': '',
			'journalDOILink': '',
			'journalKeywords': '',
			'validPaper?': '',
			'authorNumber': 0,
			'authorship': []
			}

			data['paperLabel'] = self.existingPaperNum
			data['pageWebLink'] = response.url			
			# fw.write(response.url+'\n')

			# get the journal title and issue
			journal = response.xpath('//*[@id="centerInner"]/div[1]/div[2]')
			journal = journal[0]
			# get journal title
			journalTitle = journal.xpath('div[@class="title"]//text()')
			journalTitle = ''.join(journalTitle.extract()).strip()
			# fw.write(journalTitle+'\n')
			data['journalTitle'] = journalTitle
			# get journal issue
			journalIssue = journal.xpath('p[@class="volIssue"]//text()')
			journalIssue = ''.join(journalIssue.extract()).strip()
			# fw.write(journalIssue+'\n')
			tmp_m = re.match('Volumes? *([0-9]+)[^,0-9]*([0-9]*), *(Issue.*,|Supplement.*,|) *([^,]+), *Pages *([sS0-9]*)[^0-9]*([sS0-9]*)', journalIssue)
			if tmp_m.group(2) != '':
				data['journalVol'] = tmp_m.group(1)+'-'+tmp_m.group(2)
			else:
				data['journalVol'] = tmp_m.group(1)
			data['journalDate'] = tmp_m.group(4)
			data['journalPage'] = tmp_m.group(5)+'-'+tmp_m.group(6)
			stage = 1

			# get the paper title, authorship and link
			paper = response.xpath('//*[@id="frag_1"]')
			paper = paper[0]
			# get paper title
			paperTitle = paper.xpath('h1[@class="svTitle"]//text()')
			paperTitle = ''.join(paperTitle.extract()).strip()
			# fw.write(paperTitle+'\n')
			data['paperTitle'] = paperTitle
			# if re.match('An experimental and kinetic modeling study of',paperTitle):
			# 	from scrapy.shell import inspect_response
			# 	inspect_response(response, self)
			stage = 2

			# get paper author affiliation
			paperAffils = paper.xpath('ul[@class="affiliation authAffil"]/li')
			affilDict = {}
			affilList = []
			for tmpAffil in paperAffils:
				tmpAffilLabel = tmpAffil.xpath('sup/text()')
				if len(tmpAffilLabel) == 0:
					tmpAffilLabel = 'onlyOne'
				else:
					tmpAffilLabel = tmpAffilLabel[0].extract().strip()
					tmpAffilLabel = tmpAffilLabel.lower()
				tmpAffilAddress = ''.join(tmpAffil.xpath('span//text()').extract()).strip()
				# fw.write('AffilAddress:\t' + tmpAffilLabel + '\t' + tmpAffilAddress+'\n')
				affilDict[tmpAffilLabel] = tmpAffilAddress
				affilList.append(tmpAffilAddress)
			if len(affilDict) == 0:
				data['validPaper?'] = 'False'
			else:
				data['validPaper?'] = 'True'
			stage = 3

			# get paper author name
			paperAuthors = paper.xpath('ul[@class="authorGroup noCollab svAuthor"]/li')
			data['authorNumber'] = len(paperAuthors)
			tmpAffilLabelList = []
			for tmpAuthor in paperAuthors:
				tmpList = []
				tmpName = tmpAuthor.xpath('a[@class="authorName svAuthor"]')
				if len(tmpName) == 0:
					tmp_fn = ''.join(tmpAuthor.xpath('.//text()').extract()).strip()
					tmpList = [tmp_fn, '', '', '']
					data['authorship'].append(tmpList)
					continue
				tmp_fn = tmpName.xpath('@data-fn').extract()[0]
				tmp_ln = tmpName.xpath('@data-ln').extract()[0]
				# fw.write('Author\t' + tmp_fn + ' ' + tmp_ln+'\n')
				tmpList.append(tmp_fn)
				tmpList.append(tmp_ln)

				tmpAffils = tmpAuthor.xpath('a[@class="intra_ref auth_aff"]')
				tmpStr = ''
				for tmpAffil in tmpAffils:
					tmpAffilLabel = tmpAffil.xpath('@title').re('Affiliation: *(.*)')[0]
					tmpAffilLabel = tmpAffilLabel.lower().strip()
					# fw.write('Affil:\t' + tmpAffilLabel+'\n')
					if len(tmpAffilLabel) > 0:
						if tmpAffilLabel not in tmpAffilLabelList:
							tmpAffilLabelList.append(tmpAffilLabel)
						if tmpAffilLabel in affilDict.keys():
							tmpStr += affilDict[tmpAffilLabel] + '\n'
						else:
							tmpIndex = tmpAffilLabelList.index(tmpAffilLabel)
							if tmpIndex < len(affilList):
								tmpStr += affilList[tmpIndex] + '\n'
							else:
								for i in xrange(len(affilList)):
									if re.search(tmpAffilLabelList[i], tmpAffilLabel):
										tmpStr += affilList[i] + '\n'
								if tmpStr == '':
									# raise Exception('unrecognizable affiliation label!')
									pass

				if tmpStr == '':
					if len(affilDict) > 0:
						tmpStr = affilDict[affilDict.keys()[0]]
					else:
						tmpStr = ''
				tmpList.append(tmpStr)

				tmpEmails = tmpAuthor.xpath('a[@class="auth_mail"]')
				tmpStr = ''
				for tmpEmail in tmpEmails:
					tmpEmailAddress = tmpEmail.xpath('@href').re('mailto:(.*)')[0]
					# fw.write('Email:\t' + tmpEmailAddress+'\n')
					tmpStr += tmpEmailAddress+'\n'
				tmpList.append(tmpStr)
				data['authorship'].append(tmpList)
			stage = 4

			# get paper keywords
			paperKey = response.xpath('//*[@id="frag_2"]/ul[@class="keyword"]')
			tmpStr = ''
			# fw.write('keywords:\n')
			for tmpKey in paperKey.xpath('li[@class="svKeywords"]'):
				tmpKeyword = ''.join(tmpKey.xpath('span//text()').extract()).strip()
				# fw.write('\t'+tmpKeyword+'\n') 
				tmpStr += tmpKeyword + '\n'
			data['journalKeywords'] = tmpStr
			stage = 5

			# get paper link
			paperLink = response.xpath('//script/text()').re('SDM.doi *= *\'(.*)\'')
			paperLink = paperLink[0]
			# fw.write('paper doi link:\t' + paperLink+'\n')
			data['journalDOILink'] = 'http://dx.doi.org/'+paperLink
			stage = 6


		except Exception, e:
			# print e.args
			# print 'parse_paper\tstage:\t'+str(stage)
			# fw.write('parse_paper\tstage:\t'+str(stage)+'\n')
			if stage != 0:
				fw_error = file('errorLink2.txt', 'a')
				fw_error.write(response.url+'\n'+'parse_paper\tstage:\t'+str(stage)+'\n')
				fw_error.close()
			# from scrapy.shell import inspect_response
			# inspect_response(response, self)
			yield Request(response.url, callback=self.parse_paper2, dont_filter=True)
			# raise e
		else:
			self.sh_data.write(self.existingPaperNum*5+3, 0, data['paperLabel'])
			self.sh_data.write(self.existingPaperNum*5+3, 1, data['pageWebLink'])
			self.sh_data.write(self.existingPaperNum*5+3, 2, data['paperTitle'])
			self.sh_data.write(self.existingPaperNum*5+3, 3, data['journalTitle'])
			self.sh_data.write(self.existingPaperNum*5+3, 4, data['journalVol'])
			self.sh_data.write(self.existingPaperNum*5+3, 5, data['journalDate'])
			self.sh_data.write(self.existingPaperNum*5+3, 6, data['journalPage'])
			self.sh_data.write(self.existingPaperNum*5+3, 7, data['journalDOILink'])
			self.sh_data.write(self.existingPaperNum*5+3, 8, data['journalKeywords'])
			self.sh_data.write(self.existingPaperNum*5+3, 9, data['validPaper?'])
			self.sh_data.write(self.existingPaperNum*5+3, 10, data['authorNumber'])
			for (index, tmpAuthor) in enumerate(data['authorship']):
				self.sh_data.write(self.existingPaperNum*5+3, index+11, tmpAuthor[0])
				self.sh_data.write(self.existingPaperNum*5+4, index+11, tmpAuthor[1])
				self.sh_data.write(self.existingPaperNum*5+5, index+11, tmpAuthor[2])
				self.sh_data.write(self.existingPaperNum*5+6, index+11, tmpAuthor[3])
			# fw.close()
			self.existingPaperNum += 1
			self.sh_data.write(0, 1, self.existingPaperNum)

	# this is used to parse paper page and return useful data
	def parse_paper2(self, response):
		try:
			stage = 0
			# fw = file('test.txt', 'a')

			# fw.write('\nparse_paper\n')
			data = {
			'paperLabel': 0,
			'pageWebLink': '',
			'paperTitle': '',
			'journalTitle': '',
			'journalVol': 0,
			'journalDate': '',
			'journalPage': '',
			'journalDOILink': '',
			'journalKeywords': '',
			'validPaper?': '',
			'authorNumber': 0,
			'authorship': []
			}

			data['paperLabel'] = self.existingPaperNum
			data['pageWebLink'] = response.url			
			# fw.write(response.url+'\n')

			# get the journal title and issue
			journal = response.xpath('//*[@id="content"]/div[2]/div[2]/div[1]/div[1]')
			journal = journal[0]
			# get journal title
			journalTitle = journal.xpath('div[@class="journal-title-details"]/p[@class="journal-title"]//text()')
			journalTitle = ''.join(journalTitle.extract()).strip()
			# fw.write(journalTitle+'\n')
			data['journalTitle'] = journalTitle
			# get journal issue
			journalIssue = journal.xpath('div[@class="journal-title-details"]/p[@class="journal-volume"]//text()')
			journalIssue = ''.join(journalIssue.extract()).strip()
			# fw.write(journalIssue+'\n')
			tmp_m = re.match('Volumes? *([0-9]+)[^,0-9]*([0-9]*), *(Issue.*,|Supplement.*,|) *([^,]+), *Pages *([sS0-9]*)[^0-9]*([sS0-9]*)', journalIssue)
			if tmp_m.group(2) != '':
				data['journalVol'] = tmp_m.group(1)+'-'+tmp_m.group(2)
			else:
				data['journalVol'] = tmp_m.group(1)
			data['journalDate'] = tmp_m.group(4)
			data['journalPage'] = tmp_m.group(5)+'-'+tmp_m.group(6)
			stage = 1

			# get the paper title, authorship and link
			paper = response.xpath('//*[@id="content"]/div[2]/div[2]/div[1]')
			paper = paper[0]
			# get paper title
			paperTitle = paper.xpath('h1[@class="article-title"]//text()')
			paperTitle = ''.join(paperTitle.extract()).strip()
			# fw.write(paperTitle+'\n')
			data['paperTitle'] = paperTitle

			# if re.match('An experimental and kinetic modeling study of',paperTitle):
			# 	from scrapy.shell import inspect_response
			# 	inspect_response(response, self)
			stage = 2

			# get paper author affiliation
			paperAffils = response.xpath('//*[@id="article-author-list"]/div/div[2]/span')
			affilList = []
			for tmpAffil in paperAffils:
				tmpAffilAddress = ''.join(tmpAffil.xpath('span//text()').extract()).strip()
				# fw.write('AffilAddress:\t' + tmpAffilAddress+'\n')
				affilList.append(tmpAffilAddress)
			if len(affilList) == 0:
				data['validPaper?'] = 'False'
			else:
				data['validPaper?'] = 'True'
			stage = 3

			# get paper author name
			paperAuthors = response.xpath('//*[@id="article-author-list"]/div/div[1]/span')
			data['authorNumber'] = len(paperAuthors)
			tmpAffilLabelList = []
			for tmpAuthor in paperAuthors:
				tmpList = []
				tmpName = tmpAuthor.xpath('span[@class="author-name"]/a//text()')
				if len(tmpName) == 0:
					tmp_fn = ''.join(tmpAuthor.xpath('.//text()').extract()).strip()
					tmpList = [tmp_fn, '', '', '']
					data['authorship'].append(tmpList)
					continue				
				tmpName = ''.join(tmpName.extract())
				tmpName = tmpName.split()
				tmp_fn = ''.join(tmpName[:-1])
				tmp_ln = tmpName[-1]
				# fw.write('Author\t' + tmp_fn + ' ' + tmp_ln+'\n')
				tmpList.append(tmp_fn)
				tmpList.append(tmp_ln)
				
				tmpAffils = tmpAuthor.xpath('a[@class="author-affiliation"]')
				tmpStr = ''
				for tmpAffil in tmpAffils:
					tmpAffilLabel = tmpAffil.xpath('sup').extract()[0]
					# fw.write('Affil:\t' + tmpAffilLabel+'\n')
					if tmpAffilLabel not in tmpAffilLabelList:
						tmpAffilLabelList.append(tmpAffilLabel)
					tmpStr += affilList[tmpAffilLabelList.index(tmpAffilLabel)] + '\n'
				if tmpStr == '':
					if len(affilList) > 0:
						tmpStr = affilList[0]
					else:
						tmpStr = ''
				tmpList.append(tmpStr)

				tmpEmails = tmpAuthor.xpath('a[@class="auth_mail"]')
				tmpStr = ''
				for tmpEmail in tmpEmails:
					tmpEmailAddress = tmpEmail.xpath('@href').re('mailto:(.*)')[0]
					# fw.write('Email:\t' + tmpEmailAddress+'\n')
					tmpStr += tmpEmailAddress+'\n'
				tmpList.append(tmpStr)
				data['authorship'].append(tmpList)
			stage = 4

			# get paper keywords
			paperKey = response.xpath('//*[@id="frag_2"]/ul[@class="keyword"]')
			tmpStr = ''
			# fw.write('keywords:\n')
			for tmpKey in paperKey.xpath('li[@class="svKeywords"]'):
				tmpKeyword = ''.join(tmpKey.xpath('span//text()').extract())
				# fw.write('\t'+tmpKeyword+'\n') 
				tmpStr += tmpKeyword + '\n'
			data['journalKeywords'] = tmpStr
			stage = 5

			# get paper link
			paperLink = response.xpath('//*[@id="doi-value"]')
			paperLink = paperLink.xpath('@href')
			paperLink = paperLink.extract()[0]
			# fw.write('paper doi link:\t' + paperLink+'\n')
			data['journalDOILink'] = paperLink
			stage = 6


		except Exception, e:
			# print 'parse_paper2\tstage:\t'+str(stage)
			# fw.write('parse_paper2\tstage:\t'+str(stage)+'\n')
			fw_error = file('errorLink2.txt', 'a')
			fw_error.write(response.url+'\n'+'parse_paper2\tstage:\t'+str(stage)+'\n')
			fw_error.close()
			from scrapy.shell import inspect_response
			inspect_response(response, self)
			# yield Request(paperLink[paperNum], callback=self.parse_paper)
			raise e
		else:
			self.sh_data.write(self.existingPaperNum*5+3, 0, data['paperLabel'])
			self.sh_data.write(self.existingPaperNum*5+3, 1, data['pageWebLink'])
			self.sh_data.write(self.existingPaperNum*5+3, 2, data['paperTitle'])
			self.sh_data.write(self.existingPaperNum*5+3, 3, data['journalTitle'])
			self.sh_data.write(self.existingPaperNum*5+3, 4, data['journalVol'])
			self.sh_data.write(self.existingPaperNum*5+3, 5, data['journalDate'])
			self.sh_data.write(self.existingPaperNum*5+3, 6, data['journalPage'])
			self.sh_data.write(self.existingPaperNum*5+3, 7, data['journalDOILink'])
			self.sh_data.write(self.existingPaperNum*5+3, 8, data['journalKeywords'])
			self.sh_data.write(self.existingPaperNum*5+3, 9, data['validPaper?'])
			self.sh_data.write(self.existingPaperNum*5+3, 10, data['authorNumber'])
			for (index, tmpAuthor) in enumerate(data['authorship']):
				self.sh_data.write(self.existingPaperNum*5+3, index+11, tmpAuthor[0])
				self.sh_data.write(self.existingPaperNum*5+4, index+11, tmpAuthor[1])
				self.sh_data.write(self.existingPaperNum*5+5, index+11, tmpAuthor[2])
				self.sh_data.write(self.existingPaperNum*5+6, index+11, tmpAuthor[3])
			# fw.close()
			self.existingPaperNum += 1
			self.sh_data.write(0, 1, self.existingPaperNum)



