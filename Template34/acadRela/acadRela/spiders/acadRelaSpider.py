# encoding=utf8  
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

import re
import xlsxwriter

import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')

class AcadRelaSpider(scrapy.Spider):
	name = "acadRela"
	allowed_domains = ["sciencedirect.com"]
	start_urls = [
		# "http://www.sciencedirect.com/science/article/pii/S0010218015003077",
		# "http://www.sciencedirect.com/science/article/pii/S0010218015001911",
		# "http://www.sciencedirect.com/science/article/pii/S0926860X14007996",
		"http://www.sciencedirect.com/science/journal/03787753",
		# "http://www.sciencedirect.com/science/journal/00102180/151/1-2",
	]
	journalTitle = 'PowerSource'
	prefix = 'http://www.sciencedirect.com'

	def __init__(self):
		self.wb_journal = xlsxwriter.Workbook(self.journalTitle+'.xlsx')
		self.sh_journal = self.wb_journal.add_worksheet('journal')
		self.sh_volume = self.wb_journal.add_worksheet('volume')
		self.sh_issue = self.wb_journal.add_worksheet('issue')
		self.sh_paper = self.wb_journal.add_worksheet('paper')

		self.wb_data = xlsxwriter.Workbook('data_'+self.journalTitle+'.xlsx')
		self.sh_data = self.wb_data.add_worksheet('data')
		self.existingPaperNum = 0
		
		if os.path.exists('errorLink.txt'):
			os.remove('errorLink.txt')
 
	# this is used to parse journal page and return volume links
	def parse(self, response):
		filename = self.journalTitle + response.url.split("/")[-1]
		fw = file(filename,'w')
		fw.write(response.body)
		fw.close()

		print '\nparse\n'

		# yield Request('http://www.sciencedirect.com/science/article/pii/S0010218097003271',callback=self.parse_paper)
		# return

		# write journal info
		self.sh_journal.write(0, 0, self.journalTitle)
		self.sh_journal.write(0, 1, self.start_urls[0])

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

		# get the journal volume links
		journalVol = response.xpath('//*[@id="volumeIssueData"]/ol/li/a[contains(@class, "volLink")]')
		journalVol = journalVol.xpath('@href').extract()
		for volNum in xrange(len(journalVol)):
			journalVol[volNum] = self.prefix + journalVol[volNum]

		# write volume info
		self.sh_volume.write(0, 0, 'newest volume')
		self.sh_volume.write(0, 1, journalVol[0])
		self.sh_volume.write(0, 2, 'note that the newest volume may be updated on the websites, so it need to be revisited when updating the database')

		# request to parse volume page, and write volume parents & issue sheet title
		self.sh_volume.write(2, 0, 'visited volumes')
		self.sh_issue.write(0, 0, 'newest issue')
		self.sh_issue.write(2, 0,'label [volNum]')
		self.sh_issue.write(3, 0, 'volume')
		self.sh_issue.write(4, 0, 'issue')
		for volNum in xrange(len(journalVol)):		
			self.sh_volume.write(volNum+2, 1, journalVol[volNum])
			self.sh_issue.write(2, volNum+1, volNum)
			self.sh_issue.write(3, volNum+1, journalVol[volNum])
			yield Request(journalVol[volNum], meta={'item': volNum}, callback=self.parse_volume)

	# this is used to parse volume page and return issue links
	def parse_volume(self, response):

		print '\nparse_volume\n'

		# get the journal issue links
		journalIssue = response.xpath('//*[@id="volumeIssueData"]/ol/li/ol/li/div[@class="txt currentVolumes"]/a')
		journalIssue = journalIssue.xpath('@href').extract()
		for issueNum in xrange(len(journalIssue)):
			journalIssue[issueNum] = self.prefix + journalIssue[issueNum]
		journalIssue = [response.url] + journalIssue

		# request to parse issue page, and write issue parents & paper sheet title
		volNum = response.meta['item']
		if volNum == 0:
			self.sh_issue.write(0, 1, journalIssue[0])
		self.sh_paper.write(0, 0, 'label [volNum issueNum]')
		self.sh_paper.write(1, 0, 'issue')
		self.sh_paper.write(2, 0, 'paper')
		for issueNum in xrange(len(journalIssue)):							
			self.sh_issue.write(issueNum+4, volNum+1, journalIssue[issueNum])
			self.sh_paper.write(0, volNum*100+issueNum+1, str([volNum, issueNum]))
			self.sh_paper.write(1, volNum*100+issueNum+1, journalIssue[issueNum])
			yield Request(journalIssue[issueNum], meta={'item': [volNum, issueNum]}, callback=self.parse_issue, dont_filter=True)

	# this is used to parse issue links and return paper links
	def parse_issue(self, response):

		print '\nparse_issue\n'

		# get the paper links
		if len(response.selector.extract()) < len(response.body)/2:
			tmp_m = re.match('.*(<div[^>]+bodyMainResults.*?<ol.*?</ol>.*?</div>)',response.body,re.S|re.M)
			issueSelector = Selector(text=tmp_m.group(1))
		else:
			issueSelector = response
		paperLink = issueSelector.xpath('//*[@id="bodyMainResults"]/ol/li/ul/li/h4/a')
		paperLink = paperLink.xpath('@href').extract()

		# request to parse paper page, and write paper info
		volNum, issueNum = response.meta['item']
		for paperNum in xrange(len(paperLink)):
			self.sh_paper.write(paperNum+2, volNum*100+issueNum+1, paperLink[paperNum])
			yield Request(paperLink[paperNum], callback=self.parse_paper)

	# this is used to parse paper page and return useful data
	def parse_paper(self, response):
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
					tmpAffilLabel = tmpAffilLabel[0].extract()
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
									raise Exception('unrecognizable affiliation label!')

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
			# print 'parse_paper\tstage:\t'+str(stage)
			# fw.write('parse_paper\tstage:\t'+str(stage)+'\n')
			if stage != 0:
				fw_error = file('errorLink.txt', 'a')
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
					if len(tmpAffilLabel) > 0:
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
			fw_error = file('errorLink.txt', 'a')
			fw_error.write(response.url+'\n'+'parse_paper2\tstage:\t'+str(stage)+'\n')
			fw_error.close()
			# from scrapy.shell import inspect_response
			# inspect_response(response, self)
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



