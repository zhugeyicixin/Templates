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
	name = "acadRelaPaper"
	allowed_domains = acadRelaSpider.AcadRelaSpider.allowed_domains
	start_urls = [

"http://www.sciencedirect.com/science/article/pii/S0003448713002722",
"http://www.sciencedirect.com/science/article/pii/S0003448713001297",
"http://www.sciencedirect.com/science/article/pii/S0003448714001218",
"http://www.sciencedirect.com/science/article/pii/S0003448703000386",
"http://www.sciencedirect.com/science/article/pii/S0003448702000124",
"http://www.sciencedirect.com/science/article/pii/S0003448703000039",
"http://www.sciencedirect.com/science/article/pii/S0003448702000082",
"http://www.sciencedirect.com/science/article/pii/S0003448703000404",
"http://www.sciencedirect.com/science/article/pii/S0003448713002576",
"http://www.sciencedirect.com/science/article/pii/S0003448713003016",
"http://www.sciencedirect.com/science/article/pii/S0003448703000040",
"http://www.sciencedirect.com/science/article/pii/S0003448703000441",
"http://www.sciencedirect.com/science/article/pii/S0003448703000064",
"http://www.sciencedirect.com/science/article/pii/S0003448703000052",
"http://www.sciencedirect.com/science/article/pii/S000344870300043X",
"http://www.sciencedirect.com/science/article/pii/S0003448702000070",
"http://www.sciencedirect.com/science/article/pii/S0003448703000428",
"http://www.sciencedirect.com/science/article/pii/S0003448702000057",
"http://www.sciencedirect.com/science/article/pii/S0003448702000021",
"http://www.sciencedirect.com/science/article/pii/S0003448702000045",
"http://www.sciencedirect.com/science/article/pii/S0003448703000398",
"http://www.sciencedirect.com/science/article/pii/S0003448714001814",
"http://www.sciencedirect.com/science/article/pii/S0003448714000237",
"http://www.sciencedirect.com/science/article/pii/S0003448714001486",
"http://www.sciencedirect.com/science/article/pii/S000344871400081X",
"http://www.sciencedirect.com/science/article/pii/S0003448713003570",
"http://www.sciencedirect.com/science/article/pii/S0003448713003375",
"http://www.sciencedirect.com/science/article/pii/S0003448713000711",
"http://www.sciencedirect.com/science/article/pii/S0003448713002072",
"http://www.sciencedirect.com/science/article/pii/S0003448713001819",
"http://www.sciencedirect.com/science/article/pii/S0003448713001406",
"http://www.sciencedirect.com/science/article/pii/S0003448712003903",
"http://www.sciencedirect.com/science/article/pii/S0003448703001203",
"http://www.sciencedirect.com/science/article/pii/S0003448703000829",
"http://www.sciencedirect.com/science/article/pii/S0003448703001434",
"http://www.sciencedirect.com/science/article/pii/S0003448703001720",
"http://www.sciencedirect.com/science/article/pii/S0003448703002464",
"http://www.sciencedirect.com/science/article/pii/S000344870300249X",
"http://www.sciencedirect.com/science/article/pii/S000344870400068X",
"http://www.sciencedirect.com/science/article/pii/S000344870300252X",
"http://www.sciencedirect.com/science/article/pii/S0003448704000575",
"http://www.sciencedirect.com/science/article/pii/S0003448704001258",
"http://www.sciencedirect.com/science/article/pii/S0003448704000563",
"http://www.sciencedirect.com/science/article/pii/S000344870400054X",
"http://www.sciencedirect.com/science/article/pii/S0003448704000873",
"http://www.sciencedirect.com/science/article/pii/S0003448704000903",
"http://www.sciencedirect.com/science/article/pii/S0003448703000246",
"http://www.sciencedirect.com/science/article/pii/S0003448703000258",
"http://www.sciencedirect.com/science/article/pii/S0003448703000234",
"http://www.sciencedirect.com/science/article/pii/S0003448703000222",
"http://www.sciencedirect.com/science/article/pii/S0003448703000209",
"http://www.sciencedirect.com/science/article/pii/S0003448703000416",
"http://www.sciencedirect.com/science/article/pii/S0003448703000210",
"http://www.sciencedirect.com/science/article/pii/S0003448704000861",
"http://www.sciencedirect.com/science/article/pii/S0003448704000812",
"http://www.sciencedirect.com/science/article/pii/S0003448704000800",
"http://www.sciencedirect.com/science/article/pii/S0003448704000824",
"http://www.sciencedirect.com/science/article/pii/S0003448704000927",
"http://www.sciencedirect.com/science/article/pii/S0003448704000915",
"http://www.sciencedirect.com/science/article/pii/S0003448704000939",
"http://www.sciencedirect.com/science/article/pii/S0003448704000794",
"http://www.sciencedirect.com/science/article/pii/S0003448704000599",
"http://www.sciencedirect.com/science/article/pii/S0003448704000630",
"http://www.sciencedirect.com/science/article/pii/S0003448704000848",
"http://www.sciencedirect.com/science/article/pii/S0003448704000538",
"http://www.sciencedirect.com/science/article/pii/S0003448704000253",
"http://www.sciencedirect.com/science/article/pii/S0003448704000332",
"http://www.sciencedirect.com/science/article/pii/S0003448704000356",
"http://www.sciencedirect.com/science/article/pii/S0003448704000988",
"http://www.sciencedirect.com/science/article/pii/S0003448704000307",
"http://www.sciencedirect.com/science/article/pii/S0003448704000319",
"http://www.sciencedirect.com/science/article/pii/S0003448704000381",
"http://www.sciencedirect.com/science/article/pii/S000344870400037X",
"http://www.sciencedirect.com/science/article/pii/S0003448704000745",
"http://www.sciencedirect.com/science/article/pii/S0003448704000344",
"http://www.sciencedirect.com/science/article/pii/S0003448703002506",
"http://www.sciencedirect.com/science/article/pii/S0003448703002518",
"http://www.sciencedirect.com/science/article/pii/S0003448703002427",
"http://www.sciencedirect.com/science/article/pii/S0003448703002488",
"http://www.sciencedirect.com/science/article/pii/S0003448703002440",
"http://www.sciencedirect.com/science/article/pii/S0003448703002476",
"http://www.sciencedirect.com/science/article/pii/S0003448703002385",
"http://www.sciencedirect.com/science/article/pii/S000344870300235X",
"http://www.sciencedirect.com/science/article/pii/S0003448703002439",
"http://www.sciencedirect.com/science/article/pii/S0003448704000101",
"http://www.sciencedirect.com/science/article/pii/S000344870400006X",
"http://www.sciencedirect.com/science/article/pii/S0003448704000046",
"http://www.sciencedirect.com/science/article/pii/S0003448703002452",
"http://www.sciencedirect.com/science/article/pii/S0003448703002610",
"http://www.sciencedirect.com/science/article/pii/S0003448703002592",
"http://www.sciencedirect.com/science/article/pii/S0003448703002634",
"http://www.sciencedirect.com/science/article/pii/S0003448704000423",
"http://www.sciencedirect.com/science/article/pii/S0003448703002117",
"http://www.sciencedirect.com/science/article/pii/S0003448703002051",
"http://www.sciencedirect.com/science/article/pii/S0003448703002002",
"http://www.sciencedirect.com/science/article/pii/S0003448703001604",
"http://www.sciencedirect.com/science/article/pii/S0003448703001926",
"http://www.sciencedirect.com/science/article/pii/S0003448703001938",
"http://www.sciencedirect.com/science/article/pii/S0003448703001914",
"http://www.sciencedirect.com/science/article/pii/S000344870300194X",
"http://www.sciencedirect.com/science/article/pii/S0003448703001884",
"http://www.sciencedirect.com/science/article/pii/S0003448703001574",
"http://www.sciencedirect.com/science/article/pii/S0003448703001719",
"http://www.sciencedirect.com/science/article/pii/S0003448703001690",
"http://www.sciencedirect.com/science/article/pii/S0003448703001707",
"http://www.sciencedirect.com/science/article/pii/S0003448703001689",
"http://www.sciencedirect.com/science/article/pii/S0003448703000313",
"http://www.sciencedirect.com/science/article/pii/S000344870300163X",
"http://www.sciencedirect.com/science/article/pii/S0003448703001410",
"http://www.sciencedirect.com/science/article/pii/S0003448703001392",
"http://www.sciencedirect.com/science/article/pii/S0003448703001380",
"http://www.sciencedirect.com/science/article/pii/S0003448703001367",
"http://www.sciencedirect.com/science/article/pii/S0003448703001343",
"http://www.sciencedirect.com/science/article/pii/S0003448703001197",
"http://www.sciencedirect.com/science/article/pii/S0003448703000325",
"http://www.sciencedirect.com/science/article/pii/S0003448703001148",
"http://www.sciencedirect.com/science/article/pii/S0003448703000878",
"http://www.sciencedirect.com/science/article/pii/S0003448703001173",
"http://www.sciencedirect.com/science/article/pii/S0003448703000866",
"http://www.sciencedirect.com/science/article/pii/S0003448703001094",
"http://www.sciencedirect.com/science/article/pii/S0003448703001082",
"http://www.sciencedirect.com/science/article/pii/S0003448703000830",
"http://www.sciencedirect.com/science/article/pii/S0003448703000817",
"http://www.sciencedirect.com/science/article/pii/S0003448703000805",
"http://www.sciencedirect.com/science/article/pii/S0003448703000726",
"http://www.sciencedirect.com/science/article/pii/S0003448703000714",
"http://www.sciencedirect.com/science/article/pii/S0003448703000842",
"http://www.sciencedirect.com/science/article/pii/S0003448703000532",
"http://www.sciencedirect.com/science/article/pii/S0003448703000544",
"http://www.sciencedirect.com/science/article/pii/S0003448703000519",
"http://www.sciencedirect.com/science/article/pii/S0003448703000507",
"http://www.sciencedirect.com/science/article/pii/S0003448703000490",
"http://www.sciencedirect.com/science/article/pii/S0003448703000581",
"http://www.sciencedirect.com/science/article/pii/S0003448703000465",
"http://www.sciencedirect.com/science/article/pii/S000344870300009X",
"http://www.sciencedirect.com/science/article/pii/S0003448703000088",
"http://www.sciencedirect.com/science/article/pii/S0003448704001465",
"http://www.sciencedirect.com/science/article/pii/S0003448704001714",
"http://www.sciencedirect.com/science/article/pii/S0003448704001143",
"http://www.sciencedirect.com/science/article/pii/S0003448704001970",
"http://www.sciencedirect.com/science/article/pii/S0003448705000089",
"http://www.sciencedirect.com/science/article/pii/S0003448704002057",
"http://www.sciencedirect.com/science/article/pii/S0003448705000065",
"http://www.sciencedirect.com/science/article/pii/S0003448704002392",
"http://www.sciencedirect.com/science/article/pii/S0003448705000272",
"http://www.sciencedirect.com/science/article/pii/S0003448705001198",
"http://www.sciencedirect.com/science/article/pii/S0003448705000302",
"http://www.sciencedirect.com/science/article/pii/S0003448705000284",
"http://www.sciencedirect.com/science/article/pii/S0003448705000314",
"http://www.sciencedirect.com/science/article/pii/S0003448705000077",
"http://www.sciencedirect.com/science/article/pii/S0003448705001563",
"http://www.sciencedirect.com/science/article/pii/S0003448705001101",
"http://www.sciencedirect.com/science/article/pii/S0003448705001502",
"http://www.sciencedirect.com/science/article/pii/S0003448705001472",
"http://www.sciencedirect.com/science/article/pii/S0003448705001496",
"http://www.sciencedirect.com/science/article/pii/S0003448705001423",
"http://www.sciencedirect.com/science/article/pii/S0003448705001447",
"http://www.sciencedirect.com/science/article/pii/S0003448705001514",
"http://www.sciencedirect.com/science/article/pii/S0003448705001484",
"http://www.sciencedirect.com/science/article/pii/S0003448705001460",
"http://www.sciencedirect.com/science/article/pii/S0003448705001459",
"http://www.sciencedirect.com/science/article/pii/S0003448705001873",
"http://www.sciencedirect.com/science/article/pii/S0003448705001393",
"http://www.sciencedirect.com/science/article/pii/S000344870500137X",
"http://www.sciencedirect.com/science/article/pii/S0003448705001149",
"http://www.sciencedirect.com/science/article/pii/S0003448705001137",
"http://www.sciencedirect.com/science/article/pii/S000344870500140X",
"http://www.sciencedirect.com/science/article/pii/S0003448705001150",
"http://www.sciencedirect.com/science/article/pii/S0003448705001113",
"http://www.sciencedirect.com/science/article/pii/S0003448705000247",
"http://www.sciencedirect.com/science/article/pii/S0003448705000223",
"http://www.sciencedirect.com/science/article/pii/S0003448705000259",
"http://www.sciencedirect.com/science/article/pii/S0003448705000260",
"http://www.sciencedirect.com/science/article/pii/S0003448705000296",
"http://www.sciencedirect.com/science/article/pii/S0003448704002318",
"http://www.sciencedirect.com/science/article/pii/S000344870400229X",
"http://www.sciencedirect.com/science/article/pii/S0003448705000703",
"http://www.sciencedirect.com/science/article/pii/S0003448705000533",
"http://www.sciencedirect.com/science/article/pii/S0003448704002306",
"http://www.sciencedirect.com/science/article/pii/S0003448705000582",
"http://www.sciencedirect.com/science/article/pii/S0003448704002173",
"http://www.sciencedirect.com/science/article/pii/S0003448705000636",
"http://www.sciencedirect.com/science/article/pii/S0003448704002446",
"http://www.sciencedirect.com/science/article/pii/S0003448705000508",
"http://www.sciencedirect.com/science/article/pii/S0003448705000764",
"http://www.sciencedirect.com/science/article/pii/S0003448705000478",
"http://www.sciencedirect.com/science/article/pii/S0003448705000685",
"http://www.sciencedirect.com/science/article/pii/S0003448705000697",
"http://www.sciencedirect.com/science/article/pii/S0003448705000624",
"http://www.sciencedirect.com/science/article/pii/S0003448705000454",
"http://www.sciencedirect.com/science/article/pii/S0003448705000594",
"http://www.sciencedirect.com/science/article/pii/S0003448705000612",
"http://www.sciencedirect.com/science/article/pii/S0003448705000442",
"http://www.sciencedirect.com/science/article/pii/S0003448705000715",
"http://www.sciencedirect.com/science/article/pii/S0003448705000430",
"http://www.sciencedirect.com/science/article/pii/S000344870500048X",
"http://www.sciencedirect.com/science/article/pii/S0003448705000673",
"http://www.sciencedirect.com/science/article/pii/S0003448705000648",
"http://www.sciencedirect.com/science/article/pii/S000344870500051X",
"http://www.sciencedirect.com/science/article/pii/S000344870500065X",
"http://www.sciencedirect.com/science/article/pii/S0003448705000661",
"http://www.sciencedirect.com/science/article/pii/S0003448705000521",
"http://www.sciencedirect.com/science/article/pii/S0003448705001034",
"http://www.sciencedirect.com/science/article/pii/S0003448705000892",
"http://www.sciencedirect.com/science/article/pii/S0003448705001046",
"http://www.sciencedirect.com/science/article/pii/S0003448705001058",
"http://www.sciencedirect.com/science/article/pii/S0003448705000545",
"http://www.sciencedirect.com/science/article/pii/S0003448705000570",
"http://www.sciencedirect.com/science/article/pii/S0003448705000569",
"http://www.sciencedirect.com/science/article/pii/S0003448705001083",
"http://www.sciencedirect.com/science/article/pii/S0003448705001009",
"http://www.sciencedirect.com/science/article/pii/S0003448705001095",
"http://www.sciencedirect.com/science/article/pii/S0003448705001010",
"http://www.sciencedirect.com/science/article/pii/S0003448705001071",
"http://www.sciencedirect.com/science/article/pii/S0003448704002409",
"http://www.sciencedirect.com/science/article/pii/S0003448705000041",
"http://www.sciencedirect.com/science/article/pii/S0003448704002355",
"http://www.sciencedirect.com/science/article/pii/S0003448705000855",
"http://www.sciencedirect.com/science/article/pii/S0003448704002367",
"http://www.sciencedirect.com/science/article/pii/S0003448705000053",
"http://www.sciencedirect.com/science/article/pii/S0003448704002537",
"http://www.sciencedirect.com/science/article/pii/S0003448704001994",
"http://www.sciencedirect.com/science/article/pii/S0003448704002069",
"http://www.sciencedirect.com/science/article/pii/S0003448704001854",
"http://www.sciencedirect.com/science/article/pii/S0003448704001817",
"http://www.sciencedirect.com/science/article/pii/S0003448704002185",
"http://www.sciencedirect.com/science/article/pii/S0003448704002045",
"http://www.sciencedirect.com/science/article/pii/S0003448705000120",
"http://www.sciencedirect.com/science/article/pii/S0003448704002227",
"http://www.sciencedirect.com/science/article/pii/S000344870400174X",
"http://www.sciencedirect.com/science/article/pii/S0003448704001647",
"http://www.sciencedirect.com/science/article/pii/S0003448704001738",
"http://www.sciencedirect.com/science/article/pii/S0003448704001672",
"http://www.sciencedirect.com/science/article/pii/S0003448704001623",
"http://www.sciencedirect.com/science/article/pii/S0003448704001696",
"http://www.sciencedirect.com/science/article/pii/S0003448704001131",
"http://www.sciencedirect.com/science/article/pii/S0003448704002100",
"http://www.sciencedirect.com/science/article/pii/S0003448704001544",
"http://www.sciencedirect.com/science/article/pii/S0003448704001209",
"http://www.sciencedirect.com/science/article/pii/S000344870400143X",
"http://www.sciencedirect.com/science/article/pii/S0003448704001398",
"http://www.sciencedirect.com/science/article/pii/S0003448704001386",
"http://www.sciencedirect.com/science/article/pii/S0003448704001441",
"http://www.sciencedirect.com/science/article/pii/S0003448704001362",
"http://www.sciencedirect.com/science/article/pii/S0003448704001891",
"http://www.sciencedirect.com/science/article/pii/S0003448705001836",
"http://www.sciencedirect.com/science/article/pii/S0003448705002830",
"http://www.sciencedirect.com/science/article/pii/S0003448705002386",
"http://www.sciencedirect.com/science/article/pii/S0003448706000254",
"http://www.sciencedirect.com/science/article/pii/S0003448706000436",
"http://www.sciencedirect.com/science/article/pii/S0003448706000692",
"http://www.sciencedirect.com/science/article/pii/S000344870600254X",
"http://www.sciencedirect.com/science/article/pii/S0003448706000539",
"http://www.sciencedirect.com/science/article/pii/S0003448706002745",
"http://www.sciencedirect.com/science/article/pii/S0003448706002757",
"http://www.sciencedirect.com/science/article/pii/S0003448706001168",
"http://www.sciencedirect.com/science/article/pii/S0003448706001934",
"http://www.sciencedirect.com/science/article/pii/S0003448706002617",
"http://www.sciencedirect.com/science/article/pii/S0003448706002228",
"http://www.sciencedirect.com/science/article/pii/S0003448707000236",
"http://www.sciencedirect.com/science/article/pii/S0003448707000959",
"http://www.sciencedirect.com/science/article/pii/S0003448707000248",
"http://www.sciencedirect.com/science/article/pii/S0003448707000522",
"http://www.sciencedirect.com/science/article/pii/S000344870600326X",
"http://www.sciencedirect.com/science/article/pii/S0003448707000170",
"http://www.sciencedirect.com/science/article/pii/S0003448706003192",
"http://www.sciencedirect.com/science/article/pii/S0003448706003234",
"http://www.sciencedirect.com/science/article/pii/S0003448706003131",
"http://www.sciencedirect.com/science/article/pii/S0003448706003258",
"http://www.sciencedirect.com/science/article/pii/S0003448706003167",
"http://www.sciencedirect.com/science/article/pii/S0003448705002738",
"http://www.sciencedirect.com/science/article/pii/S0003448706003143",
"http://www.sciencedirect.com/science/article/pii/S0003448707000510",
"http://www.sciencedirect.com/science/article/pii/S000344870600312X",
"http://www.sciencedirect.com/science/article/pii/S0003448707000406",
"http://www.sciencedirect.com/science/article/pii/S0003448707000297",
"http://www.sciencedirect.com/science/article/pii/S0003448706003271",
"http://www.sciencedirect.com/science/article/pii/S0003448707000480",
"http://www.sciencedirect.com/science/article/pii/S0003448707000698",
"http://www.sciencedirect.com/science/article/pii/S000344870700042X",
"http://www.sciencedirect.com/science/article/pii/S0003448707000443",
"http://www.sciencedirect.com/science/article/pii/S0003448707000431",
"http://www.sciencedirect.com/science/article/pii/S0003448707000467",
"http://www.sciencedirect.com/science/article/pii/S0003448707000509",
"http://www.sciencedirect.com/science/article/pii/S0003448707000650",
"http://www.sciencedirect.com/science/article/pii/S0003448707000169",
"http://www.sciencedirect.com/science/article/pii/S0003448706001600",
"http://www.sciencedirect.com/science/article/pii/S0003448707000212",
"http://www.sciencedirect.com/science/article/pii/S0003448707000674",
"http://www.sciencedirect.com/science/article/pii/S0003448707000182",
"http://www.sciencedirect.com/science/article/pii/S000344870700056X",
"http://www.sciencedirect.com/science/article/pii/S0003448706002009",
"http://www.sciencedirect.com/science/article/pii/S0003448706002216",
"http://www.sciencedirect.com/science/article/pii/S000344870600206X",
"http://www.sciencedirect.com/science/article/pii/S0003448706002010",
"http://www.sciencedirect.com/science/article/pii/S0003448706002046",
"http://www.sciencedirect.com/science/article/pii/S0003448706002095",
"http://www.sciencedirect.com/science/article/pii/S0003448706002058",
"http://www.sciencedirect.com/science/article/pii/S0003448706002022",
"http://www.sciencedirect.com/science/article/pii/S0003448706002034",
"http://www.sciencedirect.com/science/article/pii/S000344870600223X",
"http://www.sciencedirect.com/science/article/pii/S0003448706002800",
"http://www.sciencedirect.com/science/article/pii/S0003448706002678",
"http://www.sciencedirect.com/science/article/pii/S0003448706002848",
"http://www.sciencedirect.com/science/article/pii/S0003448706002381",
"http://www.sciencedirect.com/science/article/pii/S0003448706002411",
"http://www.sciencedirect.com/science/article/pii/S0003448706002198",
"http://www.sciencedirect.com/science/article/pii/S0003448706002836",
"http://www.sciencedirect.com/science/article/pii/S0003448706002824",
"http://www.sciencedirect.com/science/article/pii/S0003448706002368",
"http://www.sciencedirect.com/science/article/pii/S000344870600237X",
"http://www.sciencedirect.com/science/article/pii/S000344870600268X",
"http://www.sciencedirect.com/science/article/pii/S000344870600285X",
"http://www.sciencedirect.com/science/article/pii/S0003448706002812",
"http://www.sciencedirect.com/science/article/pii/S0003448706002770",
"http://www.sciencedirect.com/science/article/pii/S0003448706003039",
"http://www.sciencedirect.com/science/article/pii/S0003448706002290",
"http://www.sciencedirect.com/science/article/pii/S0003448706002733",
"http://www.sciencedirect.com/science/article/pii/S0003448706002423",
"http://www.sciencedirect.com/science/article/pii/S0003448706002769",
"http://www.sciencedirect.com/science/article/pii/S000344870600271X",
"http://www.sciencedirect.com/science/article/pii/S0003448706002277",
"http://www.sciencedirect.com/science/article/pii/S0003448706002782",
"http://www.sciencedirect.com/science/article/pii/S0003448706002927",
"http://www.sciencedirect.com/science/article/pii/S0003448706001193",
"http://www.sciencedirect.com/science/article/pii/S0003448706000849",
"http://www.sciencedirect.com/science/article/pii/S0003448706000758",
"http://www.sciencedirect.com/science/article/pii/S0003448706000837",
"http://www.sciencedirect.com/science/article/pii/S0003448705000326",
"http://www.sciencedirect.com/science/article/pii/S0003448706000813",
"http://www.sciencedirect.com/science/article/pii/S0003448705002441",
"http://www.sciencedirect.com/science/article/pii/S0003448706001132",
"http://www.sciencedirect.com/science/article/pii/S0003448706001119",
"http://www.sciencedirect.com/science/article/pii/S0003448706001090",
"http://www.sciencedirect.com/science/article/pii/S0003448706001041",
"http://www.sciencedirect.com/science/article/pii/S0003448706001144",
"http://www.sciencedirect.com/science/article/pii/S0003448706001375",
"http://www.sciencedirect.com/science/article/pii/S000344870600182X",
"http://www.sciencedirect.com/science/article/pii/S0003448706001247",
"http://www.sciencedirect.com/science/article/pii/S0003448706001521",
"http://www.sciencedirect.com/science/article/pii/S0003448706001284",
"http://www.sciencedirect.com/science/article/pii/S0003448706001296",
"http://www.sciencedirect.com/science/article/pii/S0003448706001260",
"http://www.sciencedirect.com/science/article/pii/S0003448706001351",
"http://www.sciencedirect.com/science/article/pii/S0003448706001557",
"http://www.sciencedirect.com/science/article/pii/S0003448706001326",
"http://www.sciencedirect.com/science/article/pii/S0003448706001417",
"http://www.sciencedirect.com/science/article/pii/S0003448706002174",
"http://www.sciencedirect.com/science/article/pii/S0003448706002162",
"http://www.sciencedirect.com/science/article/pii/S0003448706001788",
"http://www.sciencedirect.com/science/article/pii/S0003448706001776",
"http://www.sciencedirect.com/science/article/pii/S0003448706001715",
"http://www.sciencedirect.com/science/article/pii/S0003448706001764",
"http://www.sciencedirect.com/science/article/pii/S0003448706001740",
"http://www.sciencedirect.com/science/article/pii/S0003448706001685",
"http://www.sciencedirect.com/science/article/pii/S0003448706001673",
"http://www.sciencedirect.com/science/article/pii/S0003448706002150",
"http://www.sciencedirect.com/science/article/pii/S0003448705001812",
"http://www.sciencedirect.com/science/article/pii/S0003448706000722",
"http://www.sciencedirect.com/science/article/pii/S000344870600045X",
"http://www.sciencedirect.com/science/article/pii/S0003448706000710",
"http://www.sciencedirect.com/science/article/pii/S0003448706000709",
"http://www.sciencedirect.com/science/article/pii/S0003448706000369",
"http://www.sciencedirect.com/science/article/pii/S0003448706000400",
"http://www.sciencedirect.com/science/article/pii/S0003448706000412",
"http://www.sciencedirect.com/science/article/pii/S0003448706000485",
"http://www.sciencedirect.com/science/article/pii/S0003448706000679",
"http://www.sciencedirect.com/science/article/pii/S0003448706000497",
"http://www.sciencedirect.com/science/article/pii/S0003448706000734",
"http://www.sciencedirect.com/science/article/pii/S0003448706000631",
"http://www.sciencedirect.com/science/article/pii/S0003448706000370",
"http://www.sciencedirect.com/science/article/pii/S0003448706000886",
"http://www.sciencedirect.com/science/article/pii/S0003448706000643",
"http://www.sciencedirect.com/science/article/pii/S0003448706000126",
"http://www.sciencedirect.com/science/article/pii/S0003448706000163",
"http://www.sciencedirect.com/science/article/pii/S0003448706000084",
"http://www.sciencedirect.com/science/article/pii/S0003448706000229",
"http://www.sciencedirect.com/science/article/pii/S0003448706000102",
"http://www.sciencedirect.com/science/article/pii/S0003448706000205",
"http://www.sciencedirect.com/science/article/pii/S0003448706000151",
"http://www.sciencedirect.com/science/article/pii/S0003448706000060",
"http://www.sciencedirect.com/science/article/pii/S0003448706000187",
"http://www.sciencedirect.com/science/article/pii/S0003448706000242",
"http://www.sciencedirect.com/science/article/pii/S0003448705001289",
"http://www.sciencedirect.com/science/article/pii/S0003448705002246",
"http://www.sciencedirect.com/science/article/pii/S0003448705002337",
"http://www.sciencedirect.com/science/article/pii/S0003448705002301",
"http://www.sciencedirect.com/science/article/pii/S0003448705002234",
"http://www.sciencedirect.com/science/article/pii/S0003448705002325",
"http://www.sciencedirect.com/science/article/pii/S0003448705002398",
"http://www.sciencedirect.com/science/article/pii/S0003448705002878",
"http://www.sciencedirect.com/science/article/pii/S0003448705001940",
"http://www.sciencedirect.com/science/article/pii/S0003448705002088",
"http://www.sciencedirect.com/science/article/pii/S0003448705002076",
"http://www.sciencedirect.com/science/article/pii/S0003448705001939",
"http://www.sciencedirect.com/science/article/pii/S0003448705002118",
"http://www.sciencedirect.com/science/article/pii/S0003448705002064",
"http://www.sciencedirect.com/science/article/pii/S0003448705002179",
"http://www.sciencedirect.com/science/article/pii/S0003448705002155",
"http://www.sciencedirect.com/science/article/pii/S0003448705002143",
"http://www.sciencedirect.com/science/article/pii/S0003448705002052",
"http://www.sciencedirect.com/science/article/pii/S000344870500212X",
"http://www.sciencedirect.com/science/article/pii/S0003448705000417",
"http://www.sciencedirect.com/science/article/pii/S0003448705002519",
"http://www.sciencedirect.com/science/article/pii/S0003448705003367",
"http://www.sciencedirect.com/science/article/pii/S0003448705003379",
"http://www.sciencedirect.com/science/article/pii/S0003448705002957",
"http://www.sciencedirect.com/science/article/pii/S0003448705003276",
"http://www.sciencedirect.com/science/article/pii/S0003448705003252",
"http://www.sciencedirect.com/science/article/pii/S000344870500329X",
"http://www.sciencedirect.com/science/article/pii/S0003448705003239",
"http://www.sciencedirect.com/science/article/pii/S0003448705003318",
"http://www.sciencedirect.com/science/article/pii/S0003448705003215",
"http://www.sciencedirect.com/science/article/pii/S0003448705003355",
"http://www.sciencedirect.com/science/article/pii/S0003448706000291",
"http://www.sciencedirect.com/science/article/pii/S0003448705002696",
"http://www.sciencedirect.com/science/article/pii/S0003448705003070",
"http://www.sciencedirect.com/science/article/pii/S0003448705002702",
"http://www.sciencedirect.com/science/article/pii/S0003448705003124",
"http://www.sciencedirect.com/science/article/pii/S0003448705002805",
"http://www.sciencedirect.com/science/article/pii/S0003448705003331",
"http://www.sciencedirect.com/science/article/pii/S0003448705002684",
"http://www.sciencedirect.com/science/article/pii/S0003448705003082",
"http://www.sciencedirect.com/science/article/pii/S0003448705001344",
"http://www.sciencedirect.com/science/article/pii/S0003448705003203",
"http://www.sciencedirect.com/science/article/pii/S0003448705003422",
"http://www.sciencedirect.com/science/article/pii/S0003448705001733",
"http://www.sciencedirect.com/science/article/pii/S0003448705001666",
"http://www.sciencedirect.com/science/article/pii/S0003448705001770",
"http://www.sciencedirect.com/science/article/pii/S0003448705001800",
"http://www.sciencedirect.com/science/article/pii/S000344870500171X",
"http://www.sciencedirect.com/science/article/pii/S0003448705001745",
"http://www.sciencedirect.com/science/article/pii/S0003448705001794",
"http://www.sciencedirect.com/science/article/pii/S0003448705001782",
"http://www.sciencedirect.com/science/article/pii/S0003448705001721",
"http://www.sciencedirect.com/science/article/pii/S000344870500199X",
"http://www.sciencedirect.com/science/article/pii/S0003448707001035",
"http://www.sciencedirect.com/science/article/pii/S0003448707002582",
"http://www.sciencedirect.com/science/article/pii/S0003448707001679",
"http://www.sciencedirect.com/science/article/pii/S0003448707002569",
"http://www.sciencedirect.com/science/article/pii/S0003448707003253",
"http://www.sciencedirect.com/science/article/pii/S0003448708000188",
"http://www.sciencedirect.com/science/article/pii/S0003448708001674",
"http://www.sciencedirect.com/science/article/pii/S0003448708001108",
"http://www.sciencedirect.com/science/article/pii/S0003448708002242",
"http://www.sciencedirect.com/science/article/pii/S0003448708002461",
"http://www.sciencedirect.com/science/article/pii/S0003448708002485",
"http://www.sciencedirect.com/science/article/pii/S0003448707000042",
"http://www.sciencedirect.com/science/article/pii/S000344870800200X",
"http://www.sciencedirect.com/science/article/pii/S0003448708002631",
"http://www.sciencedirect.com/science/article/pii/S0003448708001996",
"http://www.sciencedirect.com/science/article/pii/S0003448708001947",
"http://www.sciencedirect.com/science/article/pii/S0003448708001923",
"http://www.sciencedirect.com/science/article/pii/S0003448706001612",
"http://www.sciencedirect.com/science/article/pii/S0003448708002175",
"http://www.sciencedirect.com/science/article/pii/S0003448708002333",
"http://www.sciencedirect.com/science/article/pii/S0003448708001480",
"http://www.sciencedirect.com/science/article/pii/S0003448708001479",
"http://www.sciencedirect.com/science/article/pii/S0003448708001431",
"http://www.sciencedirect.com/science/article/pii/S0003448708001418",
"http://www.sciencedirect.com/science/article/pii/S0003448708001406",
"http://www.sciencedirect.com/science/article/pii/S0003448708001522",
"http://www.sciencedirect.com/science/article/pii/S0003448708001467",
"http://www.sciencedirect.com/science/article/pii/S0003448708001765",
"http://www.sciencedirect.com/science/article/pii/S0003448708000784",
"http://www.sciencedirect.com/science/article/pii/S0003448708000772",
"http://www.sciencedirect.com/science/article/pii/S0003448708000711",
"http://www.sciencedirect.com/science/article/pii/S0003448708000656",
"http://www.sciencedirect.com/science/article/pii/S0003448708000693",
"http://www.sciencedirect.com/science/article/pii/S0003448708000759",
"http://www.sciencedirect.com/science/article/pii/S0003448708000735",
"http://www.sciencedirect.com/science/article/pii/S0003448708000760",
"http://www.sciencedirect.com/science/article/pii/S0003448708000966",
"http://www.sciencedirect.com/science/article/pii/S0003448708000097",
"http://www.sciencedirect.com/science/article/pii/S0003448708000085",
"http://www.sciencedirect.com/science/article/pii/S000344870800005X",
"http://www.sciencedirect.com/science/article/pii/S0003448708000048",
"http://www.sciencedirect.com/science/article/pii/S0003448708000061",
"http://www.sciencedirect.com/science/article/pii/S0003448708000139",
"http://www.sciencedirect.com/science/article/pii/S0003448708000036",
"http://www.sciencedirect.com/science/article/pii/S0003448708001625",
"http://www.sciencedirect.com/science/article/pii/S0003448708001662",
"http://www.sciencedirect.com/science/article/pii/S0003448708000498",
"http://www.sciencedirect.com/science/article/pii/S0003448708001650",
"http://www.sciencedirect.com/science/article/pii/S0003448708001558",
"http://www.sciencedirect.com/science/article/pii/S0003448708001571",
"http://www.sciencedirect.com/science/article/pii/S0003448708001704",
"http://www.sciencedirect.com/science/article/pii/S0003448708001698",
"http://www.sciencedirect.com/science/article/pii/S0003448707001321",
"http://www.sciencedirect.com/science/article/pii/S000344870700025X",
"http://www.sciencedirect.com/science/article/pii/S0003448707003459",
"http://www.sciencedirect.com/science/article/pii/S0003448707003411",
"http://www.sciencedirect.com/science/article/pii/S0003448707003368",
"http://www.sciencedirect.com/science/article/pii/S0003448707003332",
"http://www.sciencedirect.com/science/article/pii/S0003448707003320",
"http://www.sciencedirect.com/science/article/pii/S0003448707003241",
"http://www.sciencedirect.com/science/article/pii/S000344870700323X",
"http://www.sciencedirect.com/science/article/pii/S0003448707003228",
"http://www.sciencedirect.com/science/article/pii/S0003448707003174",
"http://www.sciencedirect.com/science/article/pii/S0003448707003150",
"http://www.sciencedirect.com/science/article/pii/S0003448707003216",
"http://www.sciencedirect.com/science/article/pii/S0003448707003162",
"http://www.sciencedirect.com/science/article/pii/S0003448707003265",
"http://www.sciencedirect.com/science/article/pii/S0003448707002557",
"http://www.sciencedirect.com/science/article/pii/S0003448707003514",
"http://www.sciencedirect.com/science/article/pii/S0003448707003290",
"http://www.sciencedirect.com/science/article/pii/S000344870700251X",
"http://www.sciencedirect.com/science/article/pii/S0003448707002491",
"http://www.sciencedirect.com/science/article/pii/S0003448707002478",
"http://www.sciencedirect.com/science/article/pii/S0003448707002454",
"http://www.sciencedirect.com/science/article/pii/S0003448707002570",
"http://www.sciencedirect.com/science/article/pii/S0003448707002430",
"http://www.sciencedirect.com/science/article/pii/S0003448707002181",
"http://www.sciencedirect.com/science/article/pii/S0003448707002624",
"http://www.sciencedirect.com/science/article/pii/S000344870700220X",
"http://www.sciencedirect.com/science/article/pii/S0003448707001977",
"http://www.sciencedirect.com/science/article/pii/S0003448707002168",
"http://www.sciencedirect.com/science/article/pii/S0003448707002259",
"http://www.sciencedirect.com/science/article/pii/S0003448707002144",
"http://www.sciencedirect.com/science/article/pii/S0003448707002132",
"http://www.sciencedirect.com/science/article/pii/S0003448707002119",
"http://www.sciencedirect.com/science/article/pii/S0003448707002193",
"http://www.sciencedirect.com/science/article/pii/S0003448707002296",
"http://www.sciencedirect.com/science/article/pii/S0003448707001540",
"http://www.sciencedirect.com/science/article/pii/S0003448707001564",
"http://www.sciencedirect.com/science/article/pii/S0003448707001576",
"http://www.sciencedirect.com/science/article/pii/S0003448707001436",
"http://www.sciencedirect.com/science/article/pii/S0003448707001552",
"http://www.sciencedirect.com/science/article/pii/S0003448707001515",
"http://www.sciencedirect.com/science/article/pii/S0003448707001497",
"http://www.sciencedirect.com/science/article/pii/S0003448707001485",
"http://www.sciencedirect.com/science/article/pii/S0003448707002879",
"http://www.sciencedirect.com/science/article/pii/S0003448707002867",
"http://www.sciencedirect.com/science/article/pii/S0003448707002831",
"http://www.sciencedirect.com/science/article/pii/S0003448707002843",
"http://www.sciencedirect.com/science/article/pii/S000344870700282X",
"http://www.sciencedirect.com/science/article/pii/S0003448707002806",
"http://www.sciencedirect.com/science/article/pii/S000344870700279X",
"http://www.sciencedirect.com/science/article/pii/S0003448707002776",
"http://www.sciencedirect.com/science/article/pii/S0003448707002788",
"http://www.sciencedirect.com/science/article/pii/S0003448707002739",
"http://www.sciencedirect.com/science/article/pii/S0003448707002727",
"http://www.sciencedirect.com/science/article/pii/S0003448707002740",
"http://www.sciencedirect.com/science/article/pii/S0003448707003009",
"http://www.sciencedirect.com/science/article/pii/S000344870700087X",
"http://www.sciencedirect.com/science/article/pii/S0003448707000844",
"http://www.sciencedirect.com/science/article/pii/S0003448707000856",
"http://www.sciencedirect.com/science/article/pii/S0003448707000832",
"http://www.sciencedirect.com/science/article/pii/S0003448707000911",
"http://www.sciencedirect.com/science/article/pii/S0003448707000893",
"http://www.sciencedirect.com/science/article/pii/S0003448707000819",
"http://www.sciencedirect.com/science/article/pii/S0003448707001011",
"http://www.sciencedirect.com/science/article/pii/S0003448707001242",
"http://www.sciencedirect.com/science/article/pii/S0003448707001904",
"http://www.sciencedirect.com/science/article/pii/S0003448707001862",
"http://www.sciencedirect.com/science/article/pii/S0003448707001850",
"http://www.sciencedirect.com/science/article/pii/S0003448707001886",
"http://www.sciencedirect.com/science/article/pii/S0003448707001345",
"http://www.sciencedirect.com/science/article/pii/S0003448707001825",
"http://www.sciencedirect.com/science/article/pii/S0003448707002016",
"http://www.sciencedirect.com/science/article/pii/S0003448708003569",
"http://www.sciencedirect.com/science/article/pii/S0003448709001395",
"http://www.sciencedirect.com/science/article/pii/S0003448709001401",
"http://www.sciencedirect.com/science/article/pii/S0003448709000213",
"http://www.sciencedirect.com/science/article/pii/S0003448709000055",
"http://www.sciencedirect.com/science/article/pii/S0003448709001012",
"http://www.sciencedirect.com/science/article/pii/S0003448709002455",
"http://www.sciencedirect.com/science/article/pii/S0003448709003114",
"http://www.sciencedirect.com/science/article/pii/S0003448709003072",
"http://www.sciencedirect.com/science/article/pii/S0003448709003035",
"http://www.sciencedirect.com/science/article/pii/S0003448710000405",
"http://www.sciencedirect.com/science/article/pii/S0003448710000260",
"http://www.sciencedirect.com/science/article/pii/S0003448710000600",
"http://www.sciencedirect.com/science/article/pii/S0003448710000466",
"http://www.sciencedirect.com/science/article/pii/S0003448710000326",
"http://www.sciencedirect.com/science/article/pii/S0003448710000739",
"http://www.sciencedirect.com/science/article/pii/S0003448710000673",
"http://www.sciencedirect.com/science/article/pii/S0003448710000715",
"http://www.sciencedirect.com/science/article/pii/S0003448710000636",
"http://www.sciencedirect.com/science/article/pii/S0003448710000697",
"http://www.sciencedirect.com/science/article/pii/S0003448710000685",
"http://www.sciencedirect.com/science/article/pii/S0003448709002789",
"http://www.sciencedirect.com/science/article/pii/S0003448710001228",
"http://www.sciencedirect.com/science/article/pii/S0003448710000284",
"http://www.sciencedirect.com/science/article/pii/S0003448710000351",
"http://www.sciencedirect.com/science/article/pii/S0003448710000387",
"http://www.sciencedirect.com/science/article/pii/S0003448710000338",
"http://www.sciencedirect.com/science/article/pii/S0003448710000429",
"http://www.sciencedirect.com/science/article/pii/S000344871000034X",
"http://www.sciencedirect.com/science/article/pii/S0003448710000788",
"http://www.sciencedirect.com/science/article/pii/S0003448709003588",
"http://www.sciencedirect.com/science/article/pii/S000344870900359X",
"http://www.sciencedirect.com/science/article/pii/S0003448709003369",
"http://www.sciencedirect.com/science/article/pii/S0003448709003345",
"http://www.sciencedirect.com/science/article/pii/S0003448709003400",
"http://www.sciencedirect.com/science/article/pii/S0003448709003382",
"http://www.sciencedirect.com/science/article/pii/S0003448709003618",
"http://www.sciencedirect.com/science/article/pii/S000344870900362X",
"http://www.sciencedirect.com/science/article/pii/S0003448710000053",
"http://www.sciencedirect.com/science/article/pii/S0003448709003709",
"http://www.sciencedirect.com/science/article/pii/S0003448709003680",
"http://www.sciencedirect.com/science/article/pii/S0003448709002650",
"http://www.sciencedirect.com/science/article/pii/S0003448709003655",
"http://www.sciencedirect.com/science/article/pii/S0003448709003643",
"http://www.sciencedirect.com/science/article/pii/S0003448709003734",
"http://www.sciencedirect.com/science/article/pii/S0003448709003679",
"http://www.sciencedirect.com/science/article/pii/S0003448709003771",
"http://www.sciencedirect.com/science/article/pii/S0003448709002820",
"http://www.sciencedirect.com/science/article/pii/S000344870900376X",
"http://www.sciencedirect.com/science/article/pii/S0003448709003096",
"http://www.sciencedirect.com/science/article/pii/S0003448709003059",
"http://www.sciencedirect.com/science/article/pii/S0003448709003138",
"http://www.sciencedirect.com/science/article/pii/S0003448709000948",
"http://www.sciencedirect.com/science/article/pii/S000344870900314X",
"http://www.sciencedirect.com/science/article/pii/S000344870800259X",
"http://www.sciencedirect.com/science/article/pii/S0003448709000390",
"http://www.sciencedirect.com/science/article/pii/S0003448709003448",
"http://www.sciencedirect.com/science/article/pii/S0003448709002686",
"http://www.sciencedirect.com/science/article/pii/S0003448709002583",
"http://www.sciencedirect.com/science/article/pii/S0003448709002728",
"http://www.sciencedirect.com/science/article/pii/S0003448709002704",
"http://www.sciencedirect.com/science/article/pii/S000344870900273X",
"http://www.sciencedirect.com/science/article/pii/S0003448709000122",
"http://www.sciencedirect.com/science/article/pii/S0003448709003187",
"http://www.sciencedirect.com/science/article/pii/S000344870900239X",
"http://www.sciencedirect.com/science/article/pii/S0003448709002339",
"http://www.sciencedirect.com/science/article/pii/S0003448709002340",
"http://www.sciencedirect.com/science/article/pii/S0003448709002388",
"http://www.sciencedirect.com/science/article/pii/S0003448709002364",
"http://www.sciencedirect.com/science/article/pii/S0003448709002327",
"http://www.sciencedirect.com/science/article/pii/S0003448709002418",
"http://www.sciencedirect.com/science/article/pii/S0003448709002868",
"http://www.sciencedirect.com/science/article/pii/S0003448709001346",
"http://www.sciencedirect.com/science/article/pii/S0003448709002170",
"http://www.sciencedirect.com/science/article/pii/S000344870900198X",
"http://www.sciencedirect.com/science/article/pii/S0003448709002248",
"http://www.sciencedirect.com/science/article/pii/S0003448709002182",
"http://www.sciencedirect.com/science/article/pii/S0003448709001966",
"http://www.sciencedirect.com/science/article/pii/S0003448709001917",
"http://www.sciencedirect.com/science/article/pii/S0003448709002157",
"http://www.sciencedirect.com/science/article/pii/S0003448709002194",
"http://www.sciencedirect.com/science/article/pii/S0003448709001486",
"http://www.sciencedirect.com/science/article/pii/S0003448709000043",
"http://www.sciencedirect.com/science/article/pii/S0003448709000031",
"http://www.sciencedirect.com/science/article/pii/S000344870900002X",
"http://www.sciencedirect.com/science/article/pii/S0003448709000109",
"http://www.sciencedirect.com/science/article/pii/S0003448709000201",
"http://www.sciencedirect.com/science/article/pii/S0003448709000183",
"http://www.sciencedirect.com/science/article/pii/S0003448709001899",
"http://www.sciencedirect.com/science/article/pii/S0003448709001851",
"http://www.sciencedirect.com/science/article/pii/S0003448709000729",
"http://www.sciencedirect.com/science/article/pii/S000344870900184X",
"http://www.sciencedirect.com/science/article/pii/S0003448709001590",
"http://www.sciencedirect.com/science/article/pii/S0003448709001619",
"http://www.sciencedirect.com/science/article/pii/S000344870900119X",
"http://www.sciencedirect.com/science/article/pii/S0003448709001620",
"http://www.sciencedirect.com/science/article/pii/S000344870900122X",
"http://www.sciencedirect.com/science/article/pii/S0003448709002030",
"http://www.sciencedirect.com/science/article/pii/S0003448709001383",
"http://www.sciencedirect.com/science/article/pii/S000344870900136X",
"http://www.sciencedirect.com/science/article/pii/S0003448709001450",
"http://www.sciencedirect.com/science/article/pii/S0003448709001474",
"http://www.sciencedirect.com/science/article/pii/S0003448709001449",
"http://www.sciencedirect.com/science/article/pii/S0003448709000961",
"http://www.sciencedirect.com/science/article/pii/S0003448709001668",
"http://www.sciencedirect.com/science/article/pii/S0003448709000687",
"http://www.sciencedirect.com/science/article/pii/S0003448709000675",
"http://www.sciencedirect.com/science/article/pii/S000344870900064X",
"http://www.sciencedirect.com/science/article/pii/S0003448709001000",
"http://www.sciencedirect.com/science/article/pii/S0003448709000985",
"http://www.sciencedirect.com/science/article/pii/S0003448709000626",
"http://www.sciencedirect.com/science/article/pii/S0003448709001024",
"http://www.sciencedirect.com/science/article/pii/S0003448708003016",
"http://www.sciencedirect.com/science/article/pii/S0003448709001061",
"http://www.sciencedirect.com/science/article/pii/S0003448708002710",
"http://www.sciencedirect.com/science/article/pii/S0003448708002746",
"http://www.sciencedirect.com/science/article/pii/S0003448708002692",
"http://www.sciencedirect.com/science/article/pii/S0003448708002771",
"http://www.sciencedirect.com/science/article/pii/S0003448708002953",
"http://www.sciencedirect.com/science/article/pii/S0003448708003223",
"http://www.sciencedirect.com/science/article/pii/S0003448708003430",
"http://www.sciencedirect.com/science/article/pii/S0003448708003193",
"http://www.sciencedirect.com/science/article/pii/S0003448708003132",
"http://www.sciencedirect.com/science/article/pii/S0003448708003168",
"http://www.sciencedirect.com/science/article/pii/S0003448708003144",
"http://www.sciencedirect.com/science/article/pii/S0003448708003120",
"http://www.sciencedirect.com/science/article/pii/S0003448708003107",
"http://www.sciencedirect.com/science/article/pii/S0003448708001492",
"http://www.sciencedirect.com/science/article/pii/S0003448708003089",
"http://www.sciencedirect.com/science/article/pii/S0003448708003545",
"http://www.sciencedirect.com/science/article/pii/S000344870800348X",
"http://www.sciencedirect.com/science/article/pii/S0003448708003442",
"http://www.sciencedirect.com/science/article/pii/S0003448708003600",
"http://www.sciencedirect.com/science/article/pii/S0003448709000158",
"http://www.sciencedirect.com/science/article/pii/S0003448708003557",
"http://www.sciencedirect.com/science/article/pii/S0003448709000444",
"http://www.sciencedirect.com/science/article/pii/S0003448708003363",
"http://www.sciencedirect.com/science/article/pii/S0003448710001666",
"http://www.sciencedirect.com/science/article/pii/S0003448710001575",
"http://www.sciencedirect.com/science/article/pii/S0003448711000023",
"http://www.sciencedirect.com/science/article/pii/S0003448711000047",
"http://www.sciencedirect.com/science/article/pii/S0003448711001119",
"http://www.sciencedirect.com/science/article/pii/S0003448711000990",
"http://www.sciencedirect.com/science/article/pii/S0003448711002265",
"http://www.sciencedirect.com/science/article/pii/S0003448711002010",
"http://www.sciencedirect.com/science/article/pii/S0003448711002009",
"http://www.sciencedirect.com/science/article/pii/S0003448711001387",
"http://www.sciencedirect.com/science/article/pii/S000344871100268X",
"http://www.sciencedirect.com/science/article/pii/S0003448711002654",
"http://www.sciencedirect.com/science/article/pii/S0003448711002666",
"http://www.sciencedirect.com/science/article/pii/S0003448711002782",
"http://www.sciencedirect.com/science/article/pii/S0003448711003027",
"http://www.sciencedirect.com/science/article/pii/S0003448711002903",
"http://www.sciencedirect.com/science/article/pii/S0003448711002861",
"http://www.sciencedirect.com/science/article/pii/S0003448711002770",
"http://www.sciencedirect.com/science/article/pii/S0003448711002836",
"http://www.sciencedirect.com/science/article/pii/S0003448711002885",
"http://www.sciencedirect.com/science/article/pii/S0003448711002915",
"http://www.sciencedirect.com/science/article/pii/S0003448711002927",
"http://www.sciencedirect.com/science/article/pii/S0003448711001247",
"http://www.sciencedirect.com/science/article/pii/S0003448711003222",
"http://www.sciencedirect.com/science/article/pii/S0003448711002642",
"http://www.sciencedirect.com/science/article/pii/S0003448711002575",
"http://www.sciencedirect.com/science/article/pii/S0003448711002563",
"http://www.sciencedirect.com/science/article/pii/S0003448711002691",
"http://www.sciencedirect.com/science/article/pii/S0003448711002514",
"http://www.sciencedirect.com/science/article/pii/S0003448711002320",
"http://www.sciencedirect.com/science/article/pii/S0003448711002964",
"http://www.sciencedirect.com/science/article/pii/S0003448711001752",
"http://www.sciencedirect.com/science/article/pii/S0003448711002022",
"http://www.sciencedirect.com/science/article/pii/S0003448711001818",
"http://www.sciencedirect.com/science/article/pii/S0003448711002034",
"http://www.sciencedirect.com/science/article/pii/S000344871100179X",
"http://www.sciencedirect.com/science/article/pii/S000344871100182X",
"http://www.sciencedirect.com/science/article/pii/S0003448711002071",
"http://www.sciencedirect.com/science/article/pii/S0003448711001995",
"http://www.sciencedirect.com/science/article/pii/S0003448711001272",
"http://www.sciencedirect.com/science/article/pii/S0003448711001284",
"http://www.sciencedirect.com/science/article/pii/S0003448711001326",
"http://www.sciencedirect.com/science/article/pii/S0003448711001351",
"http://www.sciencedirect.com/science/article/pii/S0003448711001867",
"http://www.sciencedirect.com/science/article/pii/S0003448711001600",
"http://www.sciencedirect.com/science/article/pii/S0003448711001363",
"http://www.sciencedirect.com/science/article/pii/S0003448711002381",
"http://www.sciencedirect.com/science/article/pii/S0003448711000965",
"http://www.sciencedirect.com/science/article/pii/S0003448711001016",
"http://www.sciencedirect.com/science/article/pii/S0003448711000989",
"http://www.sciencedirect.com/science/article/pii/S0003448711001028",
"http://www.sciencedirect.com/science/article/pii/S000344871100103X",
"http://www.sciencedirect.com/science/article/pii/S0003448711001053",
"http://www.sciencedirect.com/science/article/pii/S000344871100059X",
"http://www.sciencedirect.com/science/article/pii/S0003448711001065",
"http://www.sciencedirect.com/science/article/pii/S0003448711000606",
"http://www.sciencedirect.com/science/article/pii/S0003448711001429",
"http://www.sciencedirect.com/science/article/pii/S0003448711000576",
"http://www.sciencedirect.com/science/article/pii/S0003448711000540",
"http://www.sciencedirect.com/science/article/pii/S0003448711000552",
"http://www.sciencedirect.com/science/article/pii/S000344871100028X",
"http://www.sciencedirect.com/science/article/pii/S0003448711000321",
"http://www.sciencedirect.com/science/article/pii/S0003448711000503",
"http://www.sciencedirect.com/science/article/pii/S0003448711000837",
"http://www.sciencedirect.com/science/article/pii/S0003448711000709",
"http://www.sciencedirect.com/science/article/pii/S0003448711000734",
"http://www.sciencedirect.com/science/article/pii/S0003448711000680",
"http://www.sciencedirect.com/science/article/pii/S0003448711000771",
"http://www.sciencedirect.com/science/article/pii/S0003448710004154",
"http://www.sciencedirect.com/science/article/pii/S0003448710004129",
"http://www.sciencedirect.com/science/article/pii/S0003448710004130",
"http://www.sciencedirect.com/science/article/pii/S0003448711000060",
"http://www.sciencedirect.com/science/article/pii/S0003448711000059",
"http://www.sciencedirect.com/science/article/pii/S0003448711000072",
"http://www.sciencedirect.com/science/article/pii/S0003448710003604",
"http://www.sciencedirect.com/science/article/pii/S0003448710002180",
"http://www.sciencedirect.com/science/article/pii/S0003448711000369",
"http://www.sciencedirect.com/science/article/pii/S000344871000380X",
"http://www.sciencedirect.com/science/article/pii/S0003448710003811",
"http://www.sciencedirect.com/science/article/pii/S0003448710003872",
"http://www.sciencedirect.com/science/article/pii/S0003448710003859",
"http://www.sciencedirect.com/science/article/pii/S0003448710003847",
"http://www.sciencedirect.com/science/article/pii/S0003448710003835",
"http://www.sciencedirect.com/science/article/pii/S0003448710003793",
"http://www.sciencedirect.com/science/article/pii/S0003448710003975",
"http://www.sciencedirect.com/science/article/pii/S0003448710004014",
"http://www.sciencedirect.com/science/article/pii/S0003448710004075",
"http://www.sciencedirect.com/science/article/pii/S0003448710003239",
"http://www.sciencedirect.com/science/article/pii/S0003448710003379",
"http://www.sciencedirect.com/science/article/pii/S0003448710003641",
"http://www.sciencedirect.com/science/article/pii/S000344871000243X",
"http://www.sciencedirect.com/science/article/pii/S0003448710002520",
"http://www.sciencedirect.com/science/article/pii/S0003448710002556",
"http://www.sciencedirect.com/science/article/pii/S0003448710002490",
"http://www.sciencedirect.com/science/article/pii/S0003448710001836",
"http://www.sciencedirect.com/science/article/pii/S0003448710001459",
"http://www.sciencedirect.com/science/article/pii/S0003448710003082",
"http://www.sciencedirect.com/science/article/pii/S0003448710001472",
"http://www.sciencedirect.com/science/article/pii/S0003448710001435",
"http://www.sciencedirect.com/science/article/pii/S0003448710001538",
"http://www.sciencedirect.com/science/article/pii/S0003448710001393",
"http://www.sciencedirect.com/science/article/pii/S0003448710001551",
"http://www.sciencedirect.com/science/article/pii/S0003448710001009",
"http://www.sciencedirect.com/science/article/pii/S0003448710001897",
"http://www.sciencedirect.com/science/article/pii/S0003448710001563",
"http://www.sciencedirect.com/science/article/pii/S0003448710001083",
"http://www.sciencedirect.com/science/article/pii/S0003448710001034",
"http://www.sciencedirect.com/science/article/pii/S0003448710001381",
"http://www.sciencedirect.com/science/article/pii/S0003448710002866",
"http://www.sciencedirect.com/science/article/pii/S0003448710002854",
"http://www.sciencedirect.com/science/article/pii/S0003448710003045",
"http://www.sciencedirect.com/science/article/pii/S0003448710003008",
"http://www.sciencedirect.com/science/article/pii/S0003448710003458",
"http://www.sciencedirect.com/science/article/pii/S0003448710002878",
"http://www.sciencedirect.com/science/article/pii/S0003448710002325",
"http://www.sciencedirect.com/science/article/pii/S0003448710002258",
"http://www.sciencedirect.com/science/article/pii/S000344871000212X",
"http://www.sciencedirect.com/science/article/pii/S0003448710002271",
"http://www.sciencedirect.com/science/article/pii/S0003448710002623",
"http://www.sciencedirect.com/science/article/pii/S0003448712000996",
"http://www.sciencedirect.com/science/article/pii/S0003448701000221",
"http://www.sciencedirect.com/science/article/pii/S0003448701000208",
"http://www.sciencedirect.com/science/article/pii/S0003448700000111",
"http://www.sciencedirect.com/science/article/pii/S000344870100049X",
"http://www.sciencedirect.com/science/article/pii/S0003448701000592",
"http://www.sciencedirect.com/science/article/pii/S0003448701000348",
"http://www.sciencedirect.com/science/article/pii/S0003448701000580",
"http://www.sciencedirect.com/science/article/pii/S0003448701000555",
"http://www.sciencedirect.com/science/article/pii/S0003448701000269",
"http://www.sciencedirect.com/science/article/pii/S0003448701000427",
"http://www.sciencedirect.com/science/article/pii/S0003448701000488",
"http://www.sciencedirect.com/science/article/pii/S0003448700000093",
"http://www.sciencedirect.com/science/article/pii/S0003448700000123",
"http://www.sciencedirect.com/science/article/pii/S0003448700000056",
"http://www.sciencedirect.com/science/article/pii/S0003448700000044",
"http://www.sciencedirect.com/science/article/pii/S0003448700000019",
"http://www.sciencedirect.com/science/article/pii/S0003448701000531",
"http://www.sciencedirect.com/science/article/pii/S0003448700000135",
"http://www.sciencedirect.com/science/article/pii/S0003448712003721",
"http://www.sciencedirect.com/science/article/pii/S000344871200248X",
"http://www.sciencedirect.com/science/article/pii/S0003448712002429",
"http://www.sciencedirect.com/science/article/pii/S0003448712002430",
"http://www.sciencedirect.com/science/article/pii/S0003448712002454",
"http://www.sciencedirect.com/science/article/pii/S0003448712002466",
"http://www.sciencedirect.com/science/article/pii/S0003448712002442",
"http://www.sciencedirect.com/science/article/pii/S0003448712002806",
"http://www.sciencedirect.com/science/article/pii/S0003448712003204",
"http://www.sciencedirect.com/science/article/pii/S0003448712000510",
"http://www.sciencedirect.com/science/article/pii/S0003448712001874",
"http://www.sciencedirect.com/science/article/pii/S0003448712001898",
"http://www.sciencedirect.com/science/article/pii/S0003448712001655",
"http://www.sciencedirect.com/science/article/pii/S000344871200087X",
"http://www.sciencedirect.com/science/article/pii/S0003448712001230",
"http://www.sciencedirect.com/science/article/pii/S0003448711003490",
"http://www.sciencedirect.com/science/article/pii/S0003448711003519",
"http://www.sciencedirect.com/science/article/pii/S0003448712000248",
"http://www.sciencedirect.com/science/article/pii/S0003448711003532",
"http://www.sciencedirect.com/science/article/pii/S0003448701000865",
"http://www.sciencedirect.com/science/article/pii/S0003448701000877",
"http://www.sciencedirect.com/science/article/pii/S0003448702001841",
"http://www.sciencedirect.com/science/article/pii/S0003448702002159",
"http://www.sciencedirect.com/science/article/pii/S0003448702002548",
"http://www.sciencedirect.com/science/article/pii/S0003448702002135",
"http://www.sciencedirect.com/science/article/pii/S0003448702002147",
"http://www.sciencedirect.com/science/article/pii/S0003448702002020",
"http://www.sciencedirect.com/science/article/pii/S000344870200255X",
"http://www.sciencedirect.com/science/article/pii/S0003448702002718",
"http://www.sciencedirect.com/science/article/pii/S0003448702002809",
"http://www.sciencedirect.com/science/article/pii/S0003448702002706",
"http://www.sciencedirect.com/science/article/pii/S0003448702002664",
"http://www.sciencedirect.com/science/article/pii/S0003448702002639",
"http://www.sciencedirect.com/science/article/pii/S0003448702002627",
"http://www.sciencedirect.com/science/article/pii/S0003448702002615",
"http://www.sciencedirect.com/science/article/pii/S0003448702002524",
"http://www.sciencedirect.com/science/article/pii/S0003448702002500",
"http://www.sciencedirect.com/science/article/pii/S0003448702002494",
"http://www.sciencedirect.com/science/article/pii/S0003448702002445",
"http://www.sciencedirect.com/science/article/pii/S0003448702002433",
"http://www.sciencedirect.com/science/article/pii/S0003448702002482",
"http://www.sciencedirect.com/science/article/pii/S0003448702002421",
"http://www.sciencedirect.com/science/article/pii/S0003448702002470",
"http://www.sciencedirect.com/science/article/pii/S0003448702002469",
"http://www.sciencedirect.com/science/article/pii/S000344870200241X",
"http://www.sciencedirect.com/science/article/pii/S000344870200238X",
"http://www.sciencedirect.com/science/article/pii/S0003448702002457",
"http://www.sciencedirect.com/science/article/pii/S0003448702002111",
"http://www.sciencedirect.com/science/article/pii/S000344870200207X",
"http://www.sciencedirect.com/science/article/pii/S0003448702002226",
"http://www.sciencedirect.com/science/article/pii/S0003448702002019",
"http://www.sciencedirect.com/science/article/pii/S0003448702001877",
"http://www.sciencedirect.com/science/article/pii/S0003448702001828",
"http://www.sciencedirect.com/science/article/pii/S0003448702001804",
"http://www.sciencedirect.com/science/article/pii/S000344870200183X",
"http://www.sciencedirect.com/science/article/pii/S0003448702001798",
"http://www.sciencedirect.com/science/article/pii/S0003448702001749",
"http://www.sciencedirect.com/science/article/pii/S0003448702001725",
"http://www.sciencedirect.com/science/article/pii/S0003448702001713",
"http://www.sciencedirect.com/science/article/pii/S0003448702001634",
"http://www.sciencedirect.com/science/article/pii/S0003448702001610",
"http://www.sciencedirect.com/science/article/pii/S0003448701001226",
"http://www.sciencedirect.com/science/article/pii/S0003448701001196",
"http://www.sciencedirect.com/science/article/pii/S0003448701001378",
"http://www.sciencedirect.com/science/article/pii/S0003448701001391",
"http://www.sciencedirect.com/science/article/pii/S0003448701001159",
"http://www.sciencedirect.com/science/article/pii/S0003448701001366",
"http://www.sciencedirect.com/science/article/pii/S000344870100138X",
"http://www.sciencedirect.com/science/article/pii/S0003448701001317",
"http://www.sciencedirect.com/science/article/pii/S0003448701001354",
"http://www.sciencedirect.com/science/article/pii/S0003448701001287",
"http://www.sciencedirect.com/science/article/pii/S0003448701001299",
"http://www.sciencedirect.com/science/article/pii/S0003448701001275",
"http://www.sciencedirect.com/science/article/pii/S0003448701000750",
"http://www.sciencedirect.com/science/article/pii/S0003448701000762",
"http://www.sciencedirect.com/science/article/pii/S0003448701001068",
"http://www.sciencedirect.com/science/article/pii/S0003448701001019",
"http://www.sciencedirect.com/science/article/pii/S0003448701000683",
"http://www.sciencedirect.com/science/article/pii/S0003448701000725",
"http://www.sciencedirect.com/science/article/pii/S0003448701000981",
"http://www.sciencedirect.com/science/article/pii/S0003448701000993",
"http://www.sciencedirect.com/science/article/pii/S0003448701000944",
"http://www.sciencedirect.com/science/article/pii/S0003448701000968",
"http://www.sciencedirect.com/science/article/pii/S0003448714003485",
"http://www.sciencedirect.com/science/article/pii/S0003448714003916",
"http://www.sciencedirect.com/science/article/pii/S0003448715000025",
"http://www.sciencedirect.com/science/article/pii/S0003448714002893",
"http://www.sciencedirect.com/science/article/pii/S0003448714003096",
"http://www.sciencedirect.com/science/article/pii/S0003448714002819",
"http://www.sciencedirect.com/science/article/pii/S0003448714002108",
"http://www.sciencedirect.com/science/article/pii/S0003448701000907",
"http://www.sciencedirect.com/science/article/pii/S0003448702001488",
"http://www.sciencedirect.com/science/article/pii/S0003448702001543",
"http://www.sciencedirect.com/science/article/pii/S0003448702001506",
"http://www.sciencedirect.com/science/article/pii/S0003448702001555",
"http://www.sciencedirect.com/science/article/pii/S0003448702001439",



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



