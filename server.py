import web

import match
import db
import representation
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

    # JSON requests
    '/match.json', 'MatchJSON',

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


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- JSON classes --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class MatchJSON:
    def GET(self):
        return match.match()


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Database classes ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class DBAdd:
    def POST(self):
        storage = web.input(uploadFile={})
        filename = storage['uploadFile'].filename    # This is the filename
        content = storage['uploadFile'].file.read()  # This is the content of the file
        #print MidiFile(storage)
        print MidiFile(content)
        #db.add(midi_file=content, filename=filename)
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
        filename = storage['queryFile'].filename    # This is the filename
        content = storage['queryFile'].file.read()  # This is the content of the file
        #print storage["queryFile"].filename
        value =  storage["queryFile"].value
        #print content
        #print storage["queryFile"]
        #print db.find_by_query(midi_file=storage['queryFile'])
        return render.query()


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Start the server ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    app = web.application(urls, globals())
    db.connect_db()
    app.run()
