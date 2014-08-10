import webapp2
import cgi
import re

rot13_html= """<!DOCTYPE html>

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

form= """
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(username_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(password_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(verify_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(email_error)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>

"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWD_RE =  re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

# Escapes special char for html
def escape_html(s):
    return cgi.escape(s, quote = True)

def encrypt(s):
    s=s.encode('rot13')
    return s

#validate username
def valid_username(username):
    return USER_RE.match(username)

#validate passwd
def valid_passwd(passwd):
    return PASSWD_RE.match(passwd)

#validate email
def valid_email(email):
    return EMAIL_RE.match(email)

class MainPage(webapp2.RequestHandler):
    def write_form(self, text=""):
        self.response.out.write(rot13_html % {"text" : escape_html(text)})
    
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

class SignUp(webapp2.RequestHandler):
    def write_form(self, username="", username_error="", password_error="", verify_error="", email="", email_error=""):
        self.response.out.write(form % {"username" : escape_html(username),
                                        "username_error" : username_error,
                                        "password_error" : password_error,
                                        "verify_error" : verify_error,
                                        "email" : email,
                                        "email_error" : email_error})
    
    #GET process    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.write_form()

    #POST process
    def post(self):
        username = self.request.get('username')
        passwd = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        username_error = ""
        passwd_error = ""
        email_error = ""
        verify_error = ""
        
        valid_un = valid_username(username)
        if(not valid_un):
            username_error = "That's not a valid username."
        
        valid_pd = valid_passwd(passwd)
        if(not valid_pd):
            passwd_error = "That wasn't a valid password."
            
        valid_e = True
        if(email):
            valid_e = valid_email(email)
        
        if(not valid_e):
            email_error = "That's not a valid email"
        
        valid_v = False
        if(valid_pd):
            valid_v = (passwd==verify)
        
        if(valid_pd and not valid_v):
            verify_error = "Your passwords didn't match."
        
        if(valid_un and valid_pd and valid_v and valid_e):
            self.redirect("/unit2/welcome?username=%s" % username)
        else:    
            self.response.headers['Content-Type'] = 'text/html'
            self.write_form(username, username_error, passwd_error, verify_error, email, email_error)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("Welcome, %s" % username)
            
application = webapp2.WSGIApplication([
    ('/unit2/rot13', MainPage),
    ('/unit2/signup', SignUp),
    ('/unit2/welcome', Welcome),
], debug=True)