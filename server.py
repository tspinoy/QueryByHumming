import web

import match
import db

# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------- URLs ------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

urls = (
    # HTML files
    '/', 'index',
    '/home.*', 'home',
    '/query.html', 'query',
    '/content.html', 'content',

    # CSS files
    '/css/general.css', 'generalcss',

    # JavaScript files
    '/js/home.js', 'homejs',
    '/js/query.js', 'queryjs',
    '/js/db.js', 'dbjs',

    # JSON requests
    '/match.json', 'matchjson',
    '/dbFindByFilename.json', 'dbFindByFilename',
    '/dbFindByArtist.json', 'dbFindByArtist',
    '/dbFindByID.json', 'dbFindByID',
    '/dbAdd.json', 'dbAdd'
)

render = web.template.render('templates/')


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- HTML classes --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class index:
    def GET(self):
        return render.home() # Send client immediately to home.html


class home:
    def GET(self):
        return render.home("test")


class query:
    def GET(self):
        return render.query()


class content:
    def GET(self):
        return render.content()


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- CSS classes ---------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class generalcss:
    def GET(self):
        f = open("templates/css/general.css")
        return f.read()


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ JavaScript classes ------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
class homejs:
    def GET(self):
        f = open("templates/js/home.js")
        return f.read()


class queryjs:
    def GET(self):
        f = open("templates/js/query.js")
        return f.read()


class dbjs:
    def GET(self):
        f = open("templates/js/db.js")
        return f.read()


# -------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- JSON classes --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class matchjson:
    def GET(self):
        return match.match()


class dbAdd:
    def POST(self):
        storage = web.input()
        #print storage.get("uploadFile")
        print storage.items()
        print storage.values()
        print storage.viewitems()
        print storage.viewvalues()
        #db.add(storage.get("uploadFile"))
        return render.home()


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Database classes ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
class dbFindByFilename:
    def GET(self):
        filename = web.input()
        return db.findByFilename(filename)


class dbFindByArtist:
    def GET(self):
        artist = web.input()
        return db.findByArtist(artist)


class dFindByID:
    def GET(self):
        fileid = web.input()
        return db.findByID(fileid)


# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Start the server ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    app = web.application(urls, globals())
    db.connect_db()
    app.run()