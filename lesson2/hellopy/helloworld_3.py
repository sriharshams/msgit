from google.appengine.api import users
import webapp2


form= """
<form method="post">
	What is your birthday?
	<br>
	<label>
	Month
	<input type="text" name="month">
	</label>
	<label>
	Day
	<input type="text" name="day">
	</label>
	<label>
	Year
	<input type="text" name="year">	
	</label>
<!--
<label>
	One
	<input name="q" type="radio" value="one">
</label>	

<label>
	Two
<input name="q" type="radio" value="two">
</label>

<label>
	Three
<input name="q" type="radio" value="three">
</label>
-->
<!--
<select name="q">
	<option value="1">One</option>
	<option value="2">Two</option>
	<option value="3">Three</option>
</select>
-->
<br>
<br>
<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):

    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(form)
	def post(self):
		self.response.out.write("Thanks, that's a totally validate date")
    
#class TestHandler(webapp2.RequestHandler):

#	def get(self):
#		q=self.request.get("q")
#		self.response.out.write(q)
		
		#self.response.headers['Content-Type'] = 'text/plain'
		#self.response.out.write(self.request)
		
#	def post(self):
#		q=self.request.get("q")
#		self.response.out.write(q)
		
		#self.response.headers['Content-Type'] = 'text/plain'
		#self.response.out.write(self.request)	
		
application = webapp2.WSGIApplication([
    ('/', MainPage),
#	('/testform', TestHandler),
], debug=True)