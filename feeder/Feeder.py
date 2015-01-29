import os
from ElasticDao import ElasticDao
from Analyzer import Analyzer
from Formatter  import Formatter
import sys
import shutil
import urllib
import json
class Feeder:
    index="music_search"
    docType="mp3_v7"
    host="localhost"
    port="9200"

    def __init__(self,host,port,idx,dct):
        print "creating feeder with conf host ="+host+"\n port="+port+"\n index="+idx+"\n docType="+dct
        self.index=idx
        self.docType=dct
        self.host=host
        self.port=port

        self.eDao = ElasticDao(self.host,self.port)
        self.analyzer=Analyzer()
        self.formatter=Formatter()
        self.database_dir="/Applications/XAMPP/htdocs/music_search/data_mp3_files/"+self.docType
        try:
            shutil.rmtree(self.database_dir)
        except:
            pass
        os.makedirs(self.database_dir)
        
    def feed(self,start_dir):
        print "Started feeding from source dir="+start_dir
        count=0
        mp3Count=0
        failCount=0
        for root, dirs, files in os.walk(start_dir):
            for name in files:
                if(name.endswith('.mp3')):
                    try:
                        src_filepath=os.path.join(root, name)
                        dest_filepath=os.path.join(self.database_dir,name)
                        shutil.copyfile(src_filepath,dest_filepath)
                        tmp_block=self.analyzer.analyze(dest_filepath)
                        tmp_block= self.formatter.format(tmp_block)
                        tmp_block['source']=urllib.pathname2url("/music_search/data_mp3_files/"+self.docType+"/"+name)                      
                        self.eDao.put(self.index,self.docType,tmp_block)
                        mp3Count+=1;
                    except Exception ,e :
                        failCount+=1
                        print "ERR : " + os.path.join(root, name)
                        print e
            count+=1;
            if(count%1000==0):
                print "INFO : total files scaned= "+str(count)+ "\t mp3= "  +str(mp3Count)+"\t failed= "+str(failCount)+" \n"
        print "INFO : total files scaned= "+str(count)+ "\t mp3= "  +str(mp3Count)+"\t failed= "+str(failCount)+" \n"

def main(argv):
    conf=None
    with open("./config/config.json") as json_conf:
        conf = json.loads(json_conf.read())
        json_conf.close()
    if "srcDir" in conf:
        srcDir=conf["srcDir"]
    if (len(argv) >= 2):
        srcDir=argv[1]


    feeder=Feeder(conf['hostname'],conf['port'],conf['index'],conf['docType'])
    feeder.feed(srcDir)

if __name__ == "__main__":
    main(sys.argv)
