from pymongo import MongoClient
import gridfs
import representation
import json
import match
import tempfile
from mido import MidiFile
import time
import os

db, fs = 0, 0


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ Create connection ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def connect_db():
    connection = MongoClient()
    global db, fs
    db = connection.qbh
    fs = gridfs.GridFS(db)

    print "db successfully connected: " + str(db)


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- Add & get ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def add(midi_file, filename, title, artist):
    # Put the content of the query in a temporary file
    # because "MidiFile()" expects a path to a file.
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(midi_file)
    midi = MidiFile(temp.name)

    for i, track in enumerate(midi.tracks):
        for msg in track:
            print(msg)

    relevant_messages = representation.get_onset_and_note_messages(midi_file=midi)
    ioi = representation.ioi(messages_array=relevant_messages)
    ioi = " ".join(map(str, ioi))
    print ioi
    relative_notes = representation.relative_note(messages_array=relevant_messages)
    relative_notes = " ".join(map(str, relative_notes))
    print relative_notes

    kwargs = {"filename": filename, "metadata": {"title": title,
                                                 "artist": artist,
                                                 "ioi": ioi,
                                                 "relative_notes": relative_notes}}
    temp.close()
    os.unlink(temp.name)
    fs.put(midi_file, **kwargs)


def compute_match_score(ioi, rel_notes):
    print "compute match score"
    print "ioi.matchlength = " + str(float(ioi["matchLength"]))
    print "ioi.totallength = " + str(float(ioi["totalQueryLength"]))
    print "ioi.editdistanc = " + str(ioi["editDistance"])
    print "rel.matchlength = " + str(float(rel_notes["matchLength"]))
    print "rel.totallength = " + str(float(rel_notes["totalQueryLength"]))
    print "rel.editdistanc = " + str(rel_notes["editDistance"])

    score = 0
    tolerance = 0.05

    ioi_edit_distance = ioi["editDistance"]
    ioi_match_length = float(ioi["matchLength"])
    ioi_total_length = float(ioi["totalQueryLength"])
    print "ioi_total_length = " + str(ioi_total_length)
    print str(ioi_edit_distance / ioi_match_length)

    if (ioi_edit_distance / ioi_match_length) <= tolerance:
        score += 1
    else:
        score += (ioi_match_length / ioi_total_length)

    rel_notes_edit_distance = rel_notes["editDistance"]
    rel_notes_match_length = float(rel_notes["matchLength"])
    rel_notes_total_length = float(rel_notes["totalQueryLength"])
    print "rel_notes_total_length = " + str(rel_notes_total_length)
    print str(rel_notes_edit_distance / rel_notes_match_length)

    if (rel_notes_edit_distance / rel_notes_match_length) <= tolerance:
        score += 1
    else:
        score += (rel_notes_match_length / rel_notes_total_length)

    # score += (float(ioi["matchLength"] / float(ioi["totalQueryLength"])))
    # score += (float(rel_notes["matchLength"] / float(rel_notes["totalQueryLength"])))
    score /= 2    # divide by the amount of calculations you did
    score *= 100  # for percents
    return score


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


# TO DO Complete this so that it works nice
def find_by_id(file_id):
    f = fs.find({"_id": file_id})
    return f


def find_by_query(midi_file):
    result = json.loads("{\"matches\": []}")

    query_relevant_messages = representation.get_onset_and_note_messages(midi_file=midi_file)
    query_ioi = representation.ioi(messages_array=query_relevant_messages)
    query_ioi = " ".join(map(str, query_ioi))
    query_relative_notes = representation.relative_note(messages_array=query_relevant_messages)
    query_relative_notes = " ".join(map(str, query_relative_notes))

    for db_element in fs.find(no_cursor_timeout=True):

        db_element_ioi = db_element.metadata["ioi"]

        db_element_relative_notes = db_element.metadata["relative_notes"]

        ioi_match = match.lcs(query_ioi, db_element_ioi)
        relative_notes_match = match.lcs(query_relative_notes, db_element_relative_notes)
        score = compute_match_score(ioi_match, relative_notes_match)
        result["matches"].append({"filename": db_element.filename,
                                  "title": db_element.metadata["title"],
                                  "artist": db_element.metadata["artist"],
                                  "listen": "listen",
                                  "score": score})
        # os.remove(db_element_path)

    result = json.dumps(result)
    return result


def load_content_to_json():
    start = time.time()
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
    end = time.time()
    print "time elapsed: " + str(end - start)
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
