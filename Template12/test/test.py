# import xml.etree.cElementTree as ET
import sys
from lxml import etree
# import lxml.etree
import re
import copy

# a=[1,2,3]

# def test(a):
# 	b=copy.deepcopy(a)
# 	b.append(23)
# 	b[2]=234
# 	print b 
# test(a)

# a.extend([1,2,3])
# a+=[4,5,6]

# print a
# tree = ET.ElementTree(file='test.xml')
# tree.getroot()
# root = tree.getroot()
# print root.tag, root.attrib
# for child_of_root in root:
# 	print child_of_root.tag, child_of_root.attrib

# print root[0].tag, root[0].text
# for elem in tree.iter():
# 	print elem.tag, elem.attrib, elem.text

# for elem in tree.iterfind('branch/sub-branch'):
# 	print elem.tag, elem.attrib

# for elem in tree.iterfind('branch[@name="release01"]'):
# 	print elem.tag, elem.attrib

# del root[2]
# root[0].set('foo','bar')
# for subelem	in root:
# 	print subelem.tag, subelem.attrib

# tree.write(sys.stdout)

# tree = ET.ElementTree()
# tree.SubElement('child1')=123
# tree[0].set('foo','bar')
# root = tree.getroot()
# root[0].set('foo','bar')
# a= ET.Element('elem')
# c = ET.SubElement(a, 'child1')
# c.text = 'some text'
# d = ET.SubElement(a, 'child2')
# b=ET.Element('elem_b')
# root = ET.Element('root')
# root.extend((a,b))
# tree = ET.ElementTree(root)
# tree.write('test.xml',encoding='utf-8',xml_declaration=	True, pretty_print=True)
# NS='http://www.xml-cml.org/schema'
# print NS
# location_attribute = '{%s}noName' % NS
# root_mesmer = etree.Element('mesmer',attrib={location_attribute:'tREES:XSD'})
nsmap = {None: 'http://www.xml-cml.org/schema','me': 'http://www.chem.leeds.ac.uk/mesmer', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance' }
print nsmap
# root_mesmer = etree.Element("DcmStatistics", nsmap = nsmap)
# root_mesmer.set('{http://www.xml-cml.org/schema}noNamespaceSchemaLocation','http://www.xml-cml.org/schema123')
# nameSpace = 'http://www.xml-cml.org/schema'
root_mesmer = etree.Element('mesmer', nsmap = nsmap)
# root_mesmer = etree.Element('{%s}mesmer' % 'sdfg', attrib={'xmlns':'sfsd'})
# root_mesmer.set('{%s}me' % nameSpace, 'http://www.chem.leeds.ac.uk/mesmer')

# reactionList = etree.SubElement(root_mesmer,'reactionList')
inputFile = etree.ElementTree(root_mesmer)
moleculeList = etree.SubElement(root_mesmer,'moleculeList', {'ef234':'234324'})

# inputFile = etree.ElementTree([moleculeList,reactionList])
# inputFile.append(reactionList)
inputFile.write(sys.stdout, encoding='utf-8',xml_declaration=True, pretty_print=True)


# -*- coding: utf-8 -*-

# from xml.etree import ElementTree as ET
# import cStringIO

# xml = """\
# <?xml version="1.0"?>
# <root xmlns    = "http://default-namespace.org/"
#       xmlns:py = "http://www.python.org/ns/">
#   <py:elem1 />
#   <elem2 xmlns="" />
# </root>
# """
# f = cStringIO.StringIO(xml)

# #find all elements and print tag's name.
# tree = ET.parse(f)
# print tree.getroot().tag
# elems = tree.findall('.//*')
# for elem in elems:
#     print elem.tag

# #same as above, but using iterparse.
# f.seek(0)
# for event, elem in ET.iterparse(f, ("start",)):
#     print elem.tag




