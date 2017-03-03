import web
import model
import datetime
from calendar import monthrange
from web import form


urls = (
	'/', 'Index',
	'/setDate', 'SetDate',
	'/viewItem/(\d+)', 'ViewItem',
	'/newPost', 'NewPost'

	)

app = web.application(urls, globals())

render = web.template.render('templates/', base='base')


class Index:

	form = web.form.Form(
	 	web.form.Textbox('id', description="ID"),
		web.form.Dropdown('category', ['','Automobile', 'Clothing', 'Education','Electronics','Fitness','Music','Sports','Other'],
            description="Category"),
		web.form.Textbox('title', description="Title"),
        web.form.Textbox('key', description="Key Words"),
	    web.form.Textbox('Price', web.form.regexp('[><]?[=]?\d*', 'Must be <, >, <=, or >=, followed by digits'), 
	    	value=">=0.0", description="Max Price"),
        web.form.Dropdown('open', ['','1', '0'], description="Open"),
		)


	def GET(self):
		form = self.form()
		display = model.get_items() 
		return render.index(display,form)


	def POST(self):
		form = self.form()
		if not form.validates():
			display = model.get_items()
			raise web.seeother('/')
		else:
			display = model.selectedItems(form.d.id, form.d.category, form.d.title, form.d.key, form.d.Price, form.d.open)
		return render.index(display,form)


class ViewItem:

	bidForm = web.form.Form( 
		web.form.Dropdown('buyer', ['']),
		web.form.Textbox('price', web.form.notnull, web.form.regexp('\d+', 'Insert a digit')),
		validators=[web.form.Validator("Price too low", lambda i: float(i.price) > 0)])

	def __init__(self):
		self.bid = self.bidForm()
		db = web.database(dbn='sqlite', db='./sqlite.db')
		users = db.select('users', what='userId').list()
		self.bid.buyer.args = []
		for user in users:
			self.bid.buyer.args = self.bid.buyer.args + [user.userId]


	def GET(self, id):
		bids = model.getBids(int(id))
		D = model.get_by_id(int(id))
		if D is not None:
			return render.viewItem(D, id, bids, self.bid)
		if bids is None:
			return render.viewItem(D, id, bids, self.bid)


	def POST(self, id):
		bids = model.getBids(int(id))
		D = model.get_by_id(int(id))
		if D.open == 0:
			raise web.seeother('/')
		highestBid = model.highestBid(int(id))
		buy_price = D.price 
		if highestBid is not None:
			self.bid.validators.append(
				form.Validator("Bid is too low insert higher bid (" + str(highestBid.price) + " by " +
								highestBid.buyer + ")", lambda i: float(i.price) > highestBid.price))
		self.bid.validators.append(
			form.Validator("Bid is too high insert lower bid (" + str(buy_price) +
							")", lambda i: float(i.price) <= buy_price))
		if not self.bid.validates():
			return render.viewItem(D, id, bids, self.bid)
		else:
			model.newBid(id, self.bid.d.buyer, self.bid.d.price)
		raise web.seeother('/viewItem/' + str(id))

class SetDate:
	
	form2 = web.form.Form(
        web.form.Textbox('year', web.form.regexp('\d+', 'Must be a digit')),
        web.form.Textbox('month', web.form.regexp('\d+', 'Must be a digit')),
        web.form.Textbox('day', web.form.regexp('\d+', 'Must be a digit')),
        web.form.Textbox('hour', web.form.regexp('\d+', 'Must be a digit')),
        web.form.Textbox('minute', web.form.regexp('\d+', 'Must be a digit')),
        web.form.Textbox('second', web.form.regexp('\d+', 'Must be a digit')),
		validators=[
			web.form.Validator('Error with year!', lambda i: int(i.year) in range(datetime.MINYEAR, datetime.MAXYEAR)),
            web.form.Validator('Error with month!', lambda i: int(i.month) in range(1, 13)),
            web.form.Validator('Error with day!', lambda i: int(i.day) in range(1, 32)),
            web.form.Validator('Error with minute!', lambda i: int(i.minute) in range(60)),
            web.form.Validator('Error with second!', lambda i: int(i.second) in range(60)),
            ]
        )

	def __init__(self):
		#sets the time and date in each textbox
		self.form = self.form2()
		self.form.year.value=model.GetTime().year
		self.form.month.value=model.GetTime().month
		self.form.day.value=model.GetTime().day
		self.form.hour.value=model.GetTime().hour
		self.form.minute.value=model.GetTime().minute
		self.form.second.value=model.GetTime().second


	def GET(self):
		currTime = str(model.GetTime())
		return render.setDate(self.form, currTime)



	def POST(self):
		if not self.form.validates():
			currTime = str(model.GetTime())
			return render.setDate(self.form, currTime)
		else:
			currTime = str(model.GetTime())
			Newtime = datetime.datetime(
                int(self.form.year.value), 
                int(self.form.month.value), 
                int(self.form.day.value),
                int(self.form.hour.value), 
                int(self.form.minute.value), 
                int(self.form.second.value)
            )
			print Newtime
			model.SetTime(Newtime)
		return render.setDate(self.form, currTime)
		
class NewPost:
	form = web.form.Form(
		web.form.Dropdown('category', ['','Automobile', 'Clothing', 'Education','Electronics','Fitness','Music','Sports','Other'],
            description="Category"),
        web.form.Textbox('title', description="Title"),
        web.form.Textbox('price',description="Price"),
        web.form.Textarea('description',rows=15, cols=50, description="Description" ),
 		validators=[web.form.Validator("The price needs to be higher.", lambda i: float(i.price) > 0)]		)

	def GET(self):
		form = self.form()
		return render.newPost(form)

	def POST(self):
		form = self.form()
		if not form.validates():
   			return render.newPost(form)
   		if form.validates():
			model.insertion(form['category'].value, form['title'].value, form['description'].value, form['price'].value, 1); 
		raise web.seeother('/')


if __name__ == '__main__':
    app.run()
