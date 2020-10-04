#!/usr/bin/python3.7

#sudo apt-get install python-pip
#sudo pip3 install redis

import redis
r = redis.Redis(host='localhost', port=6379, db=1)
operator_list_name = "operators"


def add_operator(id, lastname, firstname, birthdate, income_date):
	key = operator_list_name + ":" + str(id)
	r.hset(key, "lastname", lastname)
	r.hset(key, "firstname", firstname)
	r.hset(key, "birthdate", birthdate)
	r.hset(key, "incomeDate", income_date)


def add_call(id, call_hour, origin_phone_number, state, call_duration, operator_id, description)
	r.hset("operators:" + str(id), "lastname", lastname)
	r.hset("operators:" + str(id), "firstname", firstname)
	r.hset("operators:" + str(id), "birthdate", birthdate)
	r.hset("operators:" + str(id), "incomeDate", income_date)


add_operator(1, "etienne", "tom", "15/03/1998", "10/12/2019")
add_operator(2, "tom", "andre", "12/03/1998", "20/12/2019")
