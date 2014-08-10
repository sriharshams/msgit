import webapp2
import string
import cgi

form= """<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(text)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>

"""
# Escapes special char for html
def escape_html(s):
    return cgi.escape(s, quote = True)

def encrypt(s):
#     rot13 = string.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
#                              "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
#     string.translate(s, rot13)
      s=s.encode('rot13')
      return s  

class MainPage(webapp2.RequestHandler):
    def write_form(self, text=""):
        self.response.out.write(form % {"text" : escape_html(text)})
    
    #GET process    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.write_form()

    #POST process
    def post(self):
        text = self.request.get('text')
        text = encrypt(text)
        self.response.headers['Content-Type'] = 'text/html'
        self.write_form(text)
            
application = webapp2.WSGIApplication([
    ('/unit2/rot13', MainPage),
], debug=True)