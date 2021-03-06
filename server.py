import web
import db
import tempfile
from mido import MidiFile
import time
import os

# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------- URLs ------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

urls = (
    # HTML files
    '/', 'Index',
    '/home.html', 'Home',
    '/add.html', 'Add',
    '/query.html', 'Query',
    '/content.html', 'Content',
    '/search.html', 'Search',

    # CSS files
    '/css/creative.min.css', 'CreativeMinCSS',
    '/vendor/bootstrap/css/bootstrap.min.css', 'BootstrapMinCSS',
    '/vendor/magnific-popup/magnific-popup.css', 'MagnificPopupCSS',
    '/vendor/font-awesome/css/font-awesome.min.css', 'FontAwesomeMinCSS',

    # JavaScript files
    '/tables.js', 'TablesJS',
    '/js/add.js', 'AddJS',
    '/js/query.js', 'QueryJS',
    '/js/db.js', 'DBJS',
    '/js/content.js', 'ContentJS',
    '/js/creative.min.js', 'CreativeMinJS',
    '/js/search.js', 'SearchJS',

    '/vendor/jquery/jquery.min.js', 'JQueryMinJS',
    '/vendor/scrollreveal/scrollreveal.min.js', 'ScrollRevealMinJS',
    '/vendor/magnific-popup/jquery.magnific-popup.min.js', 'MagnificPopupMinJS',
    '/vendor/bootstrap/js/bootstrap.min.js', 'BootstrapMinJS',

    # JSON requests
    '/content.json', 'ContentJSON',

    # Database classes - return JSON as well
    '/dbSearch.json', 'DBSearch',
    '/dbFindByFilename.json', 'DBFindByFilename',
    '/dbFindByArtist.json', 'DBFindByArtist',
    '/dbFindByID.json', 'DBFindByID',
    '/dbFindByQuery.json', 'DBFindByQuery',
    '/dbAdd.json', 'DBAdd',

    # Font awesome
    '/vendor/font-awesome/fonts/fontawesome-webfont.woff', 'FAwoff',
    '/vendor/font-awesome/fonts/fontawesome-webfont.woff2', 'FAwoff2',
    '/vendor/font-awesome/fonts/fontawesome-webfont.ttf', 'FAttf',

    # Image files
    '/img/header.jpg', 'HeaderJPG',
    '/favicon.png', 'Favicon'
)

render = web.template.render('templates/')


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- HTML classes --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class Add:
    def GET(self):
        return render.add()


class Content:
    def GET(self):
        return render.content()


class Home:
    def GET(self):
        return render.home()


class Index:
    def GET(self):
        return render.home()  # Send client immediately to home.html


class Query:
    def GET(self):
        return render.query()


class Search:
    def GET(self):
        return render.search()


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- CSS classes ---------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class BootstrapMinCSS:
    def GET(self):
        f = open("templates/vendor/bootstrap/css/bootstrap.min.css")
        return f.read()


class CreativeMinCSS:
    def GET(self):
        f = open("templates/css/creative.min.css")
        return f.read()


class FontAwesomeMinCSS:
    def GET(self):
        f = open("templates/vendor/font-awesome/css/font-awesome.min.css")
        return f.read()


class MagnificPopupCSS:
    def GET(self):
        f = open("templates/vendor/magnific-popup/magnific-popup.css")
        return f.read()


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ JavaScript classes ------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
class AddJS:
    def GET(self):
        f = open("templates/js/add.js")
        return f.read()


class BootstrapMinJS:
    def GET(self):
        f = open("templates/vendor/bootstrap/js/bootstrap.min.js")
        return f.read()


class ContentJS:
    def GET(self):
        f = open("templates/js/content.js")
        return f.read()


class CreativeMinJS:
    def GET(self):
        f = open("templates/js/creative.min.js")
        return f.read()


class DBJS:
    def GET(self):
        f = open("templates/js/db.js")
        return f.read()


class JQueryMinJS:
    def GET(self):
        f = open("templates/vendor/jquery/jquery.min.js")
        return f.read()


class MagnificPopupMinJS:
    def GET(self):
        f = open("templates/vendor/magnific-popup/jquery.magnific-popup.min.js")
        return f.read()


class ScrollRevealMinJS:
    def GET(self):
        f = open("templates/vendor/scrollreveal/scrollreveal.min.js")
        return f.read()


class SearchJS:
    def GET(self):
        f = open("templates/js/search.js")
        return f.read()


class QueryJS:
    def GET(self):
        f = open("templates/js/query.js")
        return f.read()


class TablesJS:
    def GET(self):
        f = open("templates/js/tables.js")
        return f.read()


# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------- Font Awesome classes ----------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class FAttf:
    def GET(self):
        f = open('templates/vendor/font-awesome/fonts/fontawesome-webfont.ttf')
        return f.read()


class FAwoff:
    def GET(self):
        f = open('templates/vendor/font-awesome/fonts/fontawesome-webfont.woff')
        return f.read()


class FAwoff2:
    def GET(self):
        f = open('templates/vendor/font-awesome/fonts/fontawesome-webfont.woff2')
        return f.read()


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- JSON classes --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
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
        title = storage.title                     # The title of the new sound.
        artist = storage.artist                   # The artist of the new sound.
        db.add(midi_file=content, filename=filename, title=title, artist=artist)
        return


class DBFindByArtist:
    def GET(self):
        artist = web.input()
        return db.find_by_artist(artist=artist)


class DBFindByFilename:
    def GET(self):
        filename = web.input()
        return db.find_by_filename(filename=filename)


class DBFindByID:
    def GET(self):
        fileid = web.input()
        return db.find_by_id(file_id=fileid)


class DBFindByQuery:
    def POST(self):
        storage = web.input(queryFile={})
        content = storage.queryFile.file.read()  # The content of the file

        # Put the content of the query in a temporary file
        # because "MidiFile()" expects a path to a file.
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(content)
        temp.read()
        midi = MidiFile(temp.name)

        result = db.find_by_query(midi_file=midi)

        temp.close()  # delete temporary file
        os.unlink(temp.name)

        return result


class DBSearch:
    def POST(self):
        storage = web.input()
        title = storage.title
        artist = storage.artist
        return db.find_by_metadata(artist=artist, title=title)


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- Image classes -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class Favicon:
    def GET(self):
        f = open("favicon.png")
        return f.read()


class HeaderJPG:
    def GET(self):
        f = open("templates/img/header.jpg")
        return f.read()


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Start the server ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def not_found():
    return web.notfound(render.pageNotFound())

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.notfound = not_found
    db.connect_db()
    app.run()
