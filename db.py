from pymongo import MongoClient
import gridfs
# Add the database
client = MongoClient()
db = client.qbh
fs = gridfs.GridFS(db)

f = fs.new_file()
f.write("test")
f.close()

print(fs.list())
print(fs.find())



#test_collection = fs.test
#print fs
#x = []
#t = fs.test.find()
#for i in t:
#    x.append(i)
#print x