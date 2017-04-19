import web

import match
import db
from mido import MidiFile

# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------- URLs ------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

urls = (
    # HTML files
    '/', 'Index',
    '/home.html', 'Home',
    '/query.html', 'Query',
    '/content.html', 'Content',

    # CSS files
    '/css/general.css', 'GeneralCSS',

    # JavaScript files
    '/js/home.js', 'HomeJS',
    '/js/query.js', 'QueryJS',
    '/js/db.js', 'DBJS',
    '/js/content.js', 'ContentJS',

    # JSON requests
    '/match.json', 'MatchJSON',
    '/content.json', 'ContentJSON',

    # Database classes
    '/dbFindByFilename.json', 'DBFindByFilename',
    '/dbFindByArtist.json', 'DBFindByArtist',
    '/dbFindByID.json', 'DBFindByID',
    '/dbFindByQuery.json', 'DBFindByQuery',
    '/dbAdd.json', 'DBAdd'
)

render = web.template.render('templates/')


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- HTML classes --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class Index:
    def GET(self):
        return render.home()  # Send client immediately to home.html


class Home:
    def GET(self):
        return render.home()


class Query:
    def GET(self):
        return render.query()


class Content:
    def GET(self):
        return render.content()


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- CSS classes ---------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class GeneralCSS:
    def GET(self):
        f = open("templates/css/general.css")
        return f.read()


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ JavaScript classes ------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
class HomeJS:
    def GET(self):
        f = open("templates/js/home.js")
        return f.read()


class QueryJS:
    def GET(self):
        f = open("templates/js/query.js")
        return f.read()


class DBJS:
    def GET(self):
        f = open("templates/js/db.js")
        return f.read()


class ContentJS:
    def GET(self):
        f = open("templates/js/content.js")
        return f.read()


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- JSON classes --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class MatchJSON:
    def GET(self):
        return match.match()


class ContentJSON:
    def GET(self):
        return db.load_content_to_json()


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Database classes ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class DBAdd:
    def POST(self):
        storage = web.input(uploadFile={})
        filename = storage.uploadFile.filename    # The filename.
        content = storage.uploadFile.file.read()  # The content of the file.

        # Put the content in a temporary file
        # because "MidiFile()" expects a path to a file.
        # path = "templates/midi/" + filename
        # temp = open(path, "r+")  # read and write
        # temp.write(content)
        # midi = MidiFile(path)
        db.add(midi_file=content, filename=filename)
        # db.find_by_query(midi_file=midifile)
        return render.home()


class DBFindByFilename:
    def GET(self):
        filename = web.input()
        return db.find_by_filename(filename=filename)


class DBFindByArtist:
    def GET(self):
        artist = web.input()
        return db.find_by_artist(artist=artist)


class DBFindByID:
    def GET(self):
        fileid = web.input()
        return db.find_by_id(file_id=fileid)


class DBFindByQuery:
    def POST(self):
        storage = web.input(queryFile={})
        print storage
        filename = storage.queryFile.filename    # The filename
        content = storage.queryFile.file.read()  # The content of the file

        # Put the content of the query in a temporary file
        # because "MidiFile()" expects a path to a file.
        path = "templates/midi/" + filename
        temp = open(path, "r+")
        temp.write(content)
        midi = MidiFile(path)
        db.find_by_query(midi_file=midi)

        return render.query()


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Start the server ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    app = web.application(urls, globals())
    db.connect_db()
    app.run()
