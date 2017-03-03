import web, datetime, time
from datetime import timedelta


db = web.database(dbn='sqlite', db='./sqlite.db')

time_format = '%Y-%m-%d %H:%M:%S'


def SetTime(new_time):
    db.update('Time', where="1=1", current_time=new_time)


def GetTime():
    time_string = db.select('Time')[0].current_time
    return datetime.datetime.strptime(time_string, time_format)

def get_items():
	return db.select('items',order='id DESC')


def selectedItems(id, category, title, key, price, open):	
	return db.select('items', order='id DESC', where='category like \'%' + category + '%\' and description like \'%' + key + '%\'' + ' and title like \'%' + title + '%\'' + ' and open like \'%' + open + '%\'' + ' and price ' + price + ' and id like \'%' + id + '%\'')
	
def get_by_id(id):
	try:
		return db.select('items', where='id=$id', vars=locals())[0]
	except IndexError:
		return None


def getBids(id):
	if get_by_id(id) is None:
		return None
	else:
		return db.select('bids', where='id=$id', vars=locals(), order='bid_time DESC')

def highestBid(id):
	try:
		return db.select('bids', where='id=$id', vars=locals(), order='price DESC')[0]
	except IndexError:
		return None


def newBid(id, buyer, price):
	db.insert('bids', id=id, buyer=buyer, price=price, bid_time=GetTime().strftime(time_format))

def insertion(category, title, description, price, open):
    db.insert('items', category=category, title=title, description=description, price=price, open=True, end_date=(GetTime()+ timedelta(days=7)).strftime('%Y-%m-%d  %H:%M:%S') ) #, end_date=(get_current_time()+timedelta(days=7)).strftime(time_format))



