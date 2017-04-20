from pymongo import MongoClient
import gridfs
import representation
import json
import match
from mido import MidiFile

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


def compute_match_score(ioi, rel_notes):
    score = 0
    print ioi["totalQueryLength"]
    print ioi["matchLength"]
    score += (ioi["totalQueryLength"] / ioi["matchLength"])
    score += (rel_notes["totalQueryLength"] / rel_notes["matchLength"])
    score /= 200  # divide by 100 times the amount of calculations you did
    score *= 100  # for percents
    return score


def find_by_query(midi_file):
    result = json.loads("{\"matches\": []}")

    query_relevant_messages = representation.get_onset_and_note_messages(midi_file=midi_file)
    query_ioi = representation.ioi(messages_array=query_relevant_messages)
    query_relative_notes = representation.relative_note(messages_array=query_relevant_messages)

    for db_element in fs.find(no_cursor_timeout=True):
        db_element_path = "templates/midi/" + db_element.filename
        temp = open(db_element_path, "r+")
        temp.write(db_element.read())
        ioi_match = match.lcs(query_ioi, representation.ioi(representation.get_onset_and_note_messages(MidiFile(db_element_path))))
        relative_notes_match = match.lcs(query_relative_notes, representation.relative_note(representation.get_onset_and_note_messages(MidiFile(db_element_path))))
        score = compute_match_score(ioi_match, relative_notes_match)
        result["matches"].append({"title": db_element.filename, "listen": "listen", "score": score})

    result = json.dumps(result)
    return result


def load_content_to_json():
    result = json.loads("{\"content\": []}")
    i = 1

    for grid_out in fs.find(no_cursor_timeout=True):
        result["content"].append({"index": i, "title": grid_out.filename, "listen": "listen"})
        i += 1

    result = json.dumps(result)
    return result
