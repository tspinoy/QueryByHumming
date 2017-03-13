import web

import match

urls = (
    # HTML files
    '/', 'index',
    '/home.html', 'home',
    '/query.html', 'query',

    # CSS files
    '/css/general.css', 'generalcss',

    # JavaScript files
    '/js/home.js', 'homejs',
    '/js/query.js', 'queryjs',

    # JSON requests
    '/match.json', 'matchjson'
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

# JSON classes
class matchjson:
    def GET(self):
        return match.match()

# Start the server
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()