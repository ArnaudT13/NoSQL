#!/usr/bin/python3.7

#sudo apt-get install python-pip
#sudo pip3 install redis

import redis
r = redis.Redis(host='localhost', port=6379, db=1)
operator_list_name = "operators"
call_list_name = "calls"


def add_operator(id, lastname, firstname, birthdate, income_date):
	key = operator_list_name + ":" + str(id)
	r.hset(key, "lastname", lastname)
	r.hset(key, "firstname", firstname)
	r.hset(key, "birthdate", birthdate)
	r.hset(key, "incomeDate", income_date)


def add_call(id, call_hour, origin_phone_number, state, call_duration, operator_id, description):
	key = call_list_name + ":" + str(id)
	if r.exists("operators:" + str(operator_id)): 
		r.hset(key, "callHour", call_hour)
		r.hset(key, "originPhoneNumber", origin_phone_number)
		r.hset(key, "state", state)
		r.hset(key, "callDuration", call_duration)
		r.hset(key, "operatorId", operator_id)
		r.hset(key, "description", description)
	else:
		print("Operator doesn't exist. Operation aborted")


add_operator(1, "etienne", "tom", "15/03/1998", "10/12/2019")
add_operator(2, "tom", "andre", "12/03/1998", "20/12/2019")

add_call(1, "12:00:01", "0410121314", "finished", "12m", 1, "Appel SAV")


