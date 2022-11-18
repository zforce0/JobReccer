import PyPDF2
#create file object variable
#opening method will be rb
pdffileobj = open('./resume/yz.pdf','rb')
#create reader variable that will read the pdffileobj
pdfreader = PyPDF2.PdfFileReader(pdffileobj)
#This will store the number of pages of this pdf file
pageobj=pdfreader.getPage(0)
#(x+1) because python indentation starts with 0.
#create text variable which will store all text datafrom pdf file
text=pageobj.extractText()
#save the extracted data from pdf to a txt file
#we will use file handling here
#dont forget to put r before you put the file path
#go to the file location copy the path by right clicking on the file
#click properties and copy the location path and paste it here.
#put "\\your_txtfilename"
file1=open(r"./resume/resume_output/result.txt","a")
file1.writelines(text)