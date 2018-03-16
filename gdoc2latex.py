#!/usr/bin/env python3

import re
import sys

#------------------------------------
#---------- set variables -----------

#layout classes
italics = 'c18'
bold = ''
bolditalics = ''
underlined = ''
quotations = ''
codetext = 'c12'

#chapter
chapternb = '6'

#file
filename = '3-2-xml'

#------------------------------------
#---------- load html file ----------
    
#path to google doc file
gdoc_path = filename+'.html'

#load the text of the file into a variable html
with open(gdoc_path, 'r', encoding='utf-8') as infile:
    html = infile.read()

#delete <head> content
head = re.compile(r'<head.+?</head>')
html = head.sub(r'', html)

    
#------------------------------------
#-------- TITLES & HEADINGS ---------

title = re.compile(r'<p class=".*?title" id=".+?">(.*?)</p>')
html = title.sub(r'\\chapter{\1}', html)

h1 = re.compile(r'<h1.*?>(.*?)</h1>')
html = h1.sub(r'\n\\section{\1}', html)

h2 = re.compile(r'<h2.*?>(.*?)</h2>')
html = h2.sub(r'\n\\subsection{\1}', html)

h3 = re.compile(r'<h3.*?>(.*?)</h3>')
html = h3.sub(r'\n\\subsubsection{\1}', html)

h4 = re.compile(r'<h4.*?>(.*?)</h4>')
html = h4.sub(r'\n\\paragraph{\1}', html)

h5 = re.compile(r'<h5.*?>(.*?)</h5>')
html = h5.sub(r'\n\\subparagraph{\1}', html)

    
#------------------------------------
#----- italics/bold/underlined ------

#ATTENTION: check span and paragraph class number for each document.

if italics:
    i = re.compile(r'<span class="'+italics+'">(.*?)</span>')
    html = i.sub(r'\\emph{\1}', html)

if bold:
    b = re.compile(r'<span class="'+bold+'">(.*?)</span>')
    html = b.sub(r'\\textbf{\1}', html)

if bolditalics:
    b = re.compile(r'<span class="'+bolditalics+'">(.*?)</span>')
    html = b.sub(r'\\emph{\\textbf{\1}}', html)

if underlined:
    u = re.compile(r'<span class="'+underlined+'">(.*?)</span>')
    html = u.sub(r'\\underline{\\textbf{\1}}', html)

if codetext:
    code = re.compile(r'<span class="'+codetext+'">(.*?)</span>')
    html = code.sub(r'\\texttt{\1}', html)

if quotations:
    q = re.compile(r'<p class="'+quotations+'">(.*?)</p>')
    html = q.sub(r'\n\\begin{quotation}\n\1\n\\end{quotation}\n', html)

#------------------------------------
#-----replace special characters-----

#whitespace
html = re.sub(r'&nbsp;',r' ',html)

#quotation marks, apostrophe
html = re.sub(r'&quot;',r"'",html)
html = re.sub(r'&rdquo;',r"'",html)
html = re.sub(r'&rsquo;',r"'",html)
html = re.sub(r'&#39;',r"'",html)

html = re.sub(r'&ldquo;',r"`",html)
html = re.sub(r'&rlquo;',r"`",html)
html = re.sub(r'&lsquo;',r"`",html)

#dashes
html = re.sub(r'&mdash;',r'---',html)
html = re.sub(r'&ndash;',r'-',html)

#accents
html = re.sub(r'&aring;',r'{\\aa}',html)  #a hakanson
html = re.sub(r'&ccedil;',r'\c{c}',html)  #c cedille
html = re.sub(r'&eacute;',r'é',html)
html = re.sub(r'&oacute;',r'ó',html)
html = re.sub(r'&iacute;',r'í',html)
html = re.sub(r'&aacute;',r'á',html)
html = re.sub(r'&ecirc;',r'ê',html)
html = re.sub(r'&acirc;',r'â',html)
html = re.sub(r'&ocirc;',r'ô',html)
html = re.sub(r'&egrave;',r'è',html)
html = re.sub(r'&auml;',r'ä',html)
html = re.sub(r'&Auml;',r'Ä',html)
html = re.sub(r'&ouml;',r'ö',html)
html = re.sub(r'&uuml;',r'ü',html)
html = re.sub(r'&euml;',r'ë',html)
html = re.sub(r'&szlig;',r'{\ss}',html)  #german sharp s
html = re.sub(r'&agrave;',r'à',html)
html = re.sub(r'&igrave;',r'ì',html)
html = re.sub(r'&ograve;',r'ò',html)
html = re.sub(r'&ugrave;',r'ù',html)
html = re.sub(r'&#347;',r'\'s',html)

#other symbols
html = re.sub(r'&esect;',r'§',html)
html = re.sub(r'&sect;',r'§',html)
html = re.sub(r'&hellip;',r'\dots',html)
html = re.sub(r'&amp;',r'\&',html)
html = re.sub(r'&dagger;',r'\dag',html)  #crux
html = re.sub(r'&#281;',r'\c{e}',html)  #e caudata
html = re.sub(r'&#553;',r'\c{e}',html)  #e caudata

#html = re.sub(r'_',r'\_',html)

#------------------------------------
#-------------- IMAGES --------------

#renaming a folder of images:
# dir | rename-item -NewName {$_.name -replace "image","image2-"}
 
img = re.compile(r'<img.+?src="images/image(.+?)".+?>')

#change nb in includegraphics according to chapter nb
html = img.sub(r'\n\\begin{figure}\n\\includegraphics{images/image'+chapternb+r'-\1}\n\\caption{}\n\\label{}\n\\end{figure}\n', html)

#------------------------------------
#------------ FOOTNOTES -------------

#two types of <sup> for footnote, with or without a class attribute
ftnt = re.compile(r'<sup><a href="#ftnt(\d+?)".*?</sup>')
ftnt2 = re.compile(r'<sup class="c\d+"><a href="#ftnt(\d+?)".*?</sup>')

nb = ftnt.subn(r'\\footnote{ftnt_ref\1i}', html)
html = nb[0]

nb2 = ftnt2.subn(r'\\footnote{ftnt_ref\1i}', html)
html = nb2[0]

j = nb[1]+nb2[1]
print('Total nb of footnotes: ', j)

for i in range(1, j+1):
    string = '<p class="(c\d+\s?)+"><a href="#ftnt_ref{0}" id.*?</p>'.format(str(i))
    match = re.search(string, html, re.MULTILINE)
    if match:
        html = re.sub('ftnt_ref'+str(i)+'i', match.group(), html)
    else:
        print('Failed footnote: ', i)

#delete in text [] references for footnotes and comments
html = re.sub(r'<a href="#ftnt\d+.*?</a>', r'', html)
html = re.sub(r'<a href="#cmnt\d+.*?</a>', r'', html)


#delete footnotes and comments at the end
#problem: it also deletes it in the actual footnotes

# ftnt_del = re.compile(r'<p class="(c\d+\s?)+"><a href="#ftnt_ref(\d+?)" id.*?</p>')
# cmnt_del = re.compile(r'<p class="(c\d+\s?)+"><a href="#cmnt_ref(\d+?)" id.*?</p>')
# html = ftnt_del.sub(r'', html)
# html = cmnt_del.sub(r'', html)


#------------------------------------
#-------------- LISTS ---------------
html = re.sub(r'<ul.*?>', r'\n\\begin{itemize}', html)
html = re.sub(r'</ul>', r'\n\\end{itemize}', html)
html = re.sub(r'<ol.*?>', r'\n\\begin{enumerate}', html)
html = re.sub(r'</ol>', r'\n\\end{enumerate}', html)

html = re.sub(r'<li.*?>(.+?)</li>', r'\n\\item \1', html)

#------------------------------------
#-------------- TABLES ---------------

html = re.sub(r'<table class=".*?"><tbody>', r'\n\\begin{table}\n\\begin{tabular}', html)
html = re.sub(r'</tbody></table>', r'\n\\end{tabular}\n\\end{table}', html)

#rows
html = re.sub(r'<tr.*?>(.+?)</td></tr>', r'\n\1 \\\\', html)

#cells
html = re.sub(r'</td>', r' &', html)
html = re.sub(r'<td class=.+?>', r'', html)

# delete <p> elmts in cells?


#------------------------------------
#-------------- LINKS ---------------

html = re.sub(r'<a class=".+?>(.+?)</a>', r'\\url{\1}', html)

#------------------------------------
#-------------- SAVE ----------------

#keep paragraph separations
html = re.sub(r'<p', r'\n<p', html)

#delete rest of html tags
html = re.sub(r'<.+?>', r'', html)

#replace < > that were in the text
html = re.sub(r'&lt;',r'<',html)
html = re.sub(r'&gt;',r'>',html)


new_gdoc_path = 'LATEX-'+filename+'.txt'

#save
with open(new_gdoc_path, 'w', encoding='utf-8') as outfile:
    outfile.write(html)
