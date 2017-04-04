from pymongo import MongoClient
import gridfs
import representation
import match

db, fs = 0, 0


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ Create connection ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def connect_db():
    connection = MongoClient()
    global db, fs
    db = connection.qbh
    fs = gridfs.GridFS(db)

    #print(fs.list())
    #print(fs.find())

    #print db
    #print fs

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

    print "db successfully connected: " + str(db)
    #print "gridfs: " + str(fs)


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- Add & get ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def add(midi_file, filename):
    kwargs = {"filename": filename}
    fs.put(midi_file, **kwargs)


def find_by_filename(filename):
    f = fs.find_one({"filename": filename})
    return f


def find_by_id(file_id):
    f = fs.find_one({"_id": file_id})
    return f


def find_by_artist(artist):
    f = fs.find_one({"artist": artist})
    return f


def find_by_query(midi_file):
    print "hello"
    print fs.find()
    relevant_messages = representation.get_onset_and_note_messages(midi_file=midi_file)
    ioi = representation.ioi(messages_array=relevant_messages)
    rel_notes = representation.relative_note(messages_array=relevant_messages)
    print fs.find()
    for d in fs.find():
        iois = match.lcs(ioi, representation.ioi(representation.get_onset_and_note_messages(d)))
        notes = match.lcs(rel_notes, representation.relative_note(representation.get_onset_and_note_messages(d)))
        print "ioi   = " + str(iois)
        print "notes = " + str(notes)
    return 0
