import os
class Analyzer:
    def analyze(self,fullFileame):
        detail={}
        try:

            file=open(fullFileame,'rb')
            name,extension =os.path.splitext(file.name)

            detail['filename']=os.path.basename(name)
            if (extension is not "") and (extension is not None):
                detail['file_type']=extension[1:]

            file.seek(-128,2)
            if  file.read(3)=="TAG":
                detail['title']=file.read(30)
                detail['artist']=file.read(30)
                detail['album']=file.read(30)
                detail['year']=file.read(4)
                detail['comment']=file.read(30)
                detail['genre']=file.read(1)

            file.close()
            return detail;
        except(e):
            print "ErrCode:1 error({0}): {1}".format(e.errno, e.strerror)
            file.close()
            return detail;


#example use
#ana= Analyzer()
#details=ana.analyze("./1.mp3")
#for d in details:
#    print d
#    print details[d]
