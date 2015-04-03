# -*- coding: utf-8 -*-

import os,sys
import xmltodict as xml2dict
import collections
import codecs

def loadXML(path):
	f = codecs.open(path, 'r', 'utf-8')
	c = f.read()
	f.close()

	return xml2dict.parse(c)

def writeXML(data, path):
	txt=xml2dict.unparse(data)
	f = codecs.open(path, 'w', 'utf-8')
	f.write(txt)
	f.close()

def handleOutline(root, src):
	t = type(root)
	ret = []
	if t == collections.OrderedDict:
		children = root.get('outline', None)
		node = collections.OrderedDict()
		node['title'] = root['@text']
		ret.append(node)
		if children:
			node['children'] = collections.OrderedDict()
			handleOutline(children, node['children'])
	elif t == list:
		for child in root:
			new = collections.OrderedDict()
			ret.append(new)
			handleOutline(child, new)
	else:
		raise Exception("invalid outline")

	if len(ret) == 0:
		raise Exception("empty node")

	if len(ret) == 1:
		src['topic'] = ret[0]
	else:
		src['topics'] = ret

def parseOPML(path, output):
	src = loadXML(path)
	root = src['opml']['body']['outline']
	handleOutline(root[0], output)

def main(src, tar):
	template = loadXML(os.path.join(os.path.dirname(__file__), "template\\content.xml"))
	root = template['xmap-content']['sheet']
	parseOPML(src, root)
	writeXML(template, tar)

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
