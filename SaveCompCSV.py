
#
#@Name	Export Comprehensive Comic List...
#@Hook	Books, Library
#@Description Simple script to export all selected eComics into a CSV file

#Edited by Stonepaw to fix unicode errors
def SaveComprehensiveCSVList(books):
	name = GetFileName("Comic List")
	if name=="":
		return
	f=StreamWriter(name, False)
	#f=open(name, "w")
	try:
                for book in books:
                        #print book.ShadowSeries
                        f.Write(book.Publisher + ";")
                        f.Write(book.ShadowSeries + ";")
                        f.Write(book.ShadowTitle + ";")
                        f.Write(str(book.ShadowNumber) + ";")
                        f.Write(str(book.ShadowVolume) + ";")
                        f.Write(str(book.ShadowYear) + ";")
                        f.Write(str(book.FilePath) + ";")
                        f.Write(str(book.FileNameWithExtension) + ";")
                        f.Write(str(book.PageCount) + ";")
                        f.Write(str(book.FileSize) + ";")
        except Exception, ex:
                MessageBox.Show("There was an error writing the csv file. The error was:\n\n"+ str(ex) + str(type(ex)))
                print book.ShadowSeries
        finally:
                f.Close()

