# Converting a GoogleDoc to LaTeX

At the end of my PhD, I had to quickly convert a bunch of Google doc chapters into LaTeX, so I wrote this small script. It converts the HTML version of your gdoc and works best if you kept layout modifications to a minimum.

The script uses regular expressions to locate relevant `<p>` and `<span>` elements in the HTML. I know that some XSLT would be better, but I was in a hurry! So here are the features of the HTML that are converted into LaTeX.

## Title and Headings
The document title becomes a chapter title `\chapter{...}`, and all headings are transformed into their LaTeX equivalent: from `<h1>` becoming a `\section{}`, all the way to `<h5>` for a `\subparagraph{}`.

## Page layout  (italics, bold, etc.)
It is best to keep those to only a few, and try not to combine them! I have limited myself to six layout features: 
1) italics: `\emph{...}`
2) bold: `\textbf{...}`
3) bold italics: `\emph{\textbf{...}}`
4) underline: `\underline{...}`
5) codetext: `\texttt{...}` (for snippets of text in sans serif)
6) quotation: within a `quotation` environment (I changed the indentation of quotation paragraphs).

These features are encoded in the HTML as class attributes to `<p>` and `<span>` elements, as the letter 'c' followed by a number. For instance `<span class="c0">` may indicate a span of text in italics. The main issue with the class numbers is that they are not consistent across documents. Even the same document may have a different class for italics, if you refresh the page! So you have to check numbers before applying the transformation. You can set the class numbers as variables at the start of the script.

## Special characters
Although the main text was in English, I had plenty of accented letters from quotations in French, Italian and German, plus a few special characters like the _e caudata_ &#281; and &amp;. This also includes all kinds of characters like quotation marks or apostrophes, which are all HTML entities that must be transformed into LaTeX. For example: the _e caudata_ `&#281;` becomes `\c{e}`, and `&amp;` becomes `\&`. I've been filling this list as I went along, so it's definitely not exhaustive! You may want to add your own.

## Images
Images in the gdoc file are also included in a separate `images` folder when you download the HTML. Images keep their original extension, but are renamed as 'image1', 'image2' etc. As I had images in each chapter, I needed to add an indication of the chapter number so that there would be no conflict. To rename an entire folder of images, I have used the following command in the terminal, here for chapter 2:

`dir | rename-item -NewName {$_.name -replace "image","image2-"}`

When replacing the HTML tags `<img>`, I have used `\includegraphics{path}` of the `figure` environment. For the path to be correct, after I modified the image names, the chapter number is also needed: that's why it is a variable that must be set at the beginning of the script.

## Footnotes

## Lists

## Tables

## Links
