import web

import match
import db

urls = (
    # HTML files
    '/', 'index',
    '/home.html', 'home',
    '/query.html', 'query',
    '/content.html', 'content',

    # CSS files
    '/css/general.css', 'generalcss',

    # JavaScript files
    '/js/home.js', 'homejs',
    '/js/query.js', 'queryjs',
    '/js/db.js', 'dbjs',

    # JSON requests
    '/match.json', 'match',
    '/dbFindByFilename.json', 'dbFindByFilename',
    '/dbFindByArtist.json', 'dbFindByArtist',
    '/dbFindByID.json', 'dbFindByID',
    '/dbAdd.json', 'dbAdd'
)

render = web.template.render('templates/')

# HTML classes
class index:
    def GET(self):
        return home.GET() # Send client immediately to home.html

class home:
    def GET(self):
        return render.home()

class query:
    def GET(self):
        return render.query()

class content:
    def GET(self):
        return render.content()

# CSS classes
class generalcss:
    def GET(self):
        f = open("templates/css/general.css")
        return f.read()

# JavaScript classes
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

# JSON classes
class match:
    def GET(self):
        return match.match()

class dbAdd:
    def GET(self, f): # f = file
        return db.add(f)

class dbFindByFilename:
    def GET(self, filename):
        return db.findByFilename(filename)

class dbFindByArtist:
    def GET(self, artist):
        return db.findByArtist(artist)

class dbFindByID:
    def GET(self, id):
        return db.findByID(id)

# Start the server
if __name__ == "__main__":
    app = web.application(urls, globals())
    db.connect_db()
    app.run()