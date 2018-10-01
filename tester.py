import datetime

from brokers.user import SimulatedUser

su = SimulatedUser()
some_date = datetime.datetime(year=2010, day=19, month=1, hour=9, minute=30)
su.broker.set_day(some_date)

su.place_buy_order('ibm', 60)

some_date = datetime.datetime(year=2010, day=20, month=1, hour=9, minute=30) 
su.broker.set_day(some_date)  

su.place_sell_order('ibm', 60)

print(su.buying_power)
