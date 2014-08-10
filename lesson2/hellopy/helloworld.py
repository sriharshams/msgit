import webapp2
import cgi

form= """
<form method="post" action="/">
	What is your birthday?
	<br>
	<label>
	Month
	<input type="text" name="month" value="%(month)s">
	</label>
	<label>
	Day
	<input type="text" name="day" value="%(day)s">
	</label>
	<label>
	Year
	<input type="text" name="year" value="%(year)s">	
	</label>
	<div style="color: red">%(error)s</div>
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

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

month_abbvs = dict((m[:3].lower(), m) for m in months)
		
def escape_html(s):
	return cgi.escape(s, quote = True)
		
def valid_month(month):
    if month:
        short_month = month[:3].lower()
        if short_month in month_abbvs:
            return month_abbvs.get(short_month)


def valid_day(day):
    if(day and day.isdigit()):
        day=int(day)
        if(day>=1 and day<=31):    
            return int(day)
        else:
            None

def valid_year(year):
	if(year and year.isdigit()):
		year=int(year)
		if(year>=1990 and year<=2020):
			return int(year)
		else:
			None
		  
class MainPage(webapp2.RequestHandler):
	def write_form(self, error="", month="", day="", year=""):
		self.response.out.write(form % {"error": error, 
										"month": escape_html(month), 
										"day": escape_html(day), 
										"year": escape_html(year)})
		
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.write_form()

	def post(self):
		user_month = self.request.get('month')
		user_day = self.request.get('day')
		user_year = self.request.get('year')
		
		month = valid_month(user_month)
		day = valid_day(user_day)
		year = valid_year(user_year)
		
		if not (year and day and month):
			self.response.headers['Content-Type'] = 'text/html'
			self.write_form("Wrong value", user_month, user_day, user_year)
		else:
			self.redirect('/thanks')
			
#		self.response.out.write("Tests")

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write("Thanks, for entering a valid date!")
		
application = webapp2.WSGIApplication([
    ('/', MainPage), ('/thanks', ThanksHandler),
], debug=True)