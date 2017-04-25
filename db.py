from pymongo import MongoClient
import os
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
def add(midi_file, filename, title, artist):
    kwargs = {"filename": filename, "metadata": {"title": title, "artist": artist}}
    fs.put(midi_file, **kwargs)


def compute_match_score(ioi, rel_notes):
    score = 0
    score += (float(ioi["totalQueryLength"]) / float(ioi["matchLength"]))
    score += (float(rel_notes["totalQueryLength"]) / float(rel_notes["matchLength"]))
    score /= 200  # divide by 100 times the amount of calculations you did
    score *= 100  # for percents
    return score


def find_by_artist(artist):
    f = fs.find({"metadata[\"artist\"]": artist})
    return f


def find_by_filename(filename):
    f = fs.find({"filename": filename})
    result = json.loads("{\"results\": []}")

    for grid_out in f:
        print grid_out
        result["results"].append({"filename": grid_out.filename,
                                  "title": grid_out.metadata["title"],
                                  "artist": grid_out.metadata["artist"],
                                  "listen": "listen"})

    result = json.dumps(result)
    print result
    return result


def find_by_id(file_id):
    f = fs.find({"_id": file_id})
    return f


def find_by_query(midi_file):
    result = json.loads("{\"matches\": []}")

    query_relevant_messages = representation.get_onset_and_note_messages(midi_file=midi_file)
    query_ioi = representation.ioi(messages_array=query_relevant_messages)
    query_relative_notes = representation.relative_note(messages_array=query_relevant_messages)

    for db_element in fs.find(no_cursor_timeout=True):
        db_element_path = "templates/midi/" + db_element.filename
        temp = open(db_element_path, "r+")
        temp.write(db_element.read())
        ioi_match = match.lcs(query_ioi,
                              representation.ioi(representation.get_onset_and_note_messages(MidiFile(db_element_path))))
        relative_notes_match = match.lcs(query_relative_notes,
                                         representation.relative_note(representation.get_onset_and_note_messages(MidiFile(db_element_path))))
        score = compute_match_score(ioi_match, relative_notes_match)
        result["matches"].append({"filename": db_element.filename,
                                  "title": db_element.metadata["title"],
                                  "artist": db_element.metadata["artist"],
                                  "listen": "listen",
                                  "score": score})
        # os.remove(db_element_path)

    result = json.dumps(result)
    return result


def find_by_title(title):
    f = fs.find({"metadata[\"title\"]": title})
    return f


def load_content_to_json():
    result = json.loads("{\"content\": []}")
    i = 1

    for grid_out in fs.find(no_cursor_timeout=True):
        result["content"].append({"index": i,
                                  "filename": grid_out.filename,
                                  "title": grid_out.metadata["title"],
                                  "artist": grid_out.metadata["artist"],
                                  "listen": "listen"})
        i += 1

    result = json.dumps(result)
    return result


def search_by_metadata(artist, title):
    result = json.loads("{\"results\": []}")
    if artist == "":
        grid_outs = fs.find({"metadata.title": title})
    elif title == "":
        grid_outs = fs.find({"metadata.artist": artist})
    else:
        grid_outs = fs.find({"metadata.artist": artist, "metadata.title": title})

    print grid_outs

    for grid_out in grid_outs:
        print grid_out
        result["results"].append({"filename": grid_out.filename,
                                  "title": grid_out.metadata["title"],
                                  "artist": grid_out.metadata["artist"],
                                  "listen": "listen"})

    result = json.dumps(result)
    return result
