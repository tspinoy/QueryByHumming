from pymongo import MongoClient
import gridfs

db, fs = 0, 0

def connect_db():
    connection = MongoClient()
    global db, fs
    db = connection.qbh
    fs = gridfs.GridFS(db)

    print(fs.list())
    print(fs.find())

    print db
    print fs

    # f = fs.new_file()
    # f.write("test")
    # f.close()

    #test_collection = fs.test
    #print fs
    #x = []
    #t = fs.test.find()
    #for i in t:
    #    x.append(i)
    #print x

    #print os.path.getsize(r"/Users/thijsspinoy/OneDrive/John Miles - Music (ingekort).mp3")

    #fileID = fs.put(open(r"/Users/thijsspinoy/OneDrive/John Miles - Music (ingekort).mp3", 'r'))
    #out = fs.get(fileID)
    #print out.length

    print "db connected: " + str(db)
    print "gridfs: " + str(fs)

def add(file):
    print "try to add file"
    fs.put(file)
    print "file added"

def findByFilename(filename):
    file = fs.find_one({"filename": filename})
    return file

def findByID(id):
    file = fs.find_one({"_id": id})
    return file

def findByArtist(artist):
    file = fs.find_one({"artist": artist})
    return file