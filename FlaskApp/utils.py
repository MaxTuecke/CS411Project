from __future__ import print_function # Python 2/3 compatibility
import os, json


import mysql.connector
from mysql.connector.constants import ClientFlag
import csv


config = {
    'user': 'root',
    'password': 'root',
    'host': '34.70.223.157',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem',
    'database' : 'app'
}


def insert_help(data):
    if not ("director_id" in data.keys() and "name" in data.keys() and "birth_year" in data.keys()):
        return

    sql = "INSERT INTO directors (director_id, name, birth_year) VALUES ('{0}', '{1}', '{2}')".format(data["director_id"], data["name"], data["birth_year"])

    cnxn = mysql.connector.connect(**config)

    mycursor = cnxn.cursor()
    mycursor.execute(sql)
    cnxn.commit()   # commit the changes

    mycursor.close()
    cnxn.close()

def search_help_id(dir_id):
    sql = "SELECT * FROM directors WHERE director_id = '{0}'".format(dir_id)

    cnxn = mysql.connector.connect(**config)

    mycursor = cnxn.cursor()
    mycursor.execute(sql)

    out = mycursor.fetchall()

    mycursor.close()
    cnxn.close()

    return out

def search_help_name(dir_name):
    sql = "SELECT * FROM directors WHERE name = '{0}'".format(dir_name)

    cnxn = mysql.connector.connect(**config)

    mycursor = cnxn.cursor()
    mycursor.execute(sql)

    out = mycursor.fetchall()

    mycursor.close()
    cnxn.close()

    return out

def search_help_birth(dir_birth):
    sql = "SELECT * FROM directors WHERE birth_year = '{0}'".format(dir_birth)

    cnxn = mysql.connector.connect(**config)

    mycursor = cnxn.cursor()
    mycursor.execute(sql)

    out = mycursor.fetchall()

    mycursor.close()
    cnxn.close()

    return out

def update_help(update_data):
    sql = "UPDATE directors SET name = '{1}', birth_year = '{2}' WHERE director_id = '{0}'".format(update_data["director_id"], update_data["name"], update_data["birth_year"])

    cnxn = mysql.connector.connect(**config)

    mycursor = cnxn.cursor()
    mycursor.execute(sql)
    cnxn.commit()   # commit the changes

    mycursor.close()
    cnxn.close()

def delete_help(dir_id):
    sql = "DELETE FROM directors WHERE director_id = '{0}'".format(dir_id)

    cnxn = mysql.connector.connect(**config)

    mycursor = cnxn.cursor()
    mycursor.execute(sql)
    cnxn.commit()   # commit the changes

    mycursor.close()
    cnxn.close()


def adv_help():
    sql = "SELECT director_id, CEILING(AVG(avg_rating)) AS rating, MIN(num_ratings) AS min_ratings FROM directs_in NATURAL JOIN movies WHERE num_ratings > 500 GROUP BY director_id"

    cnxn = mysql.connector.connect(**config)

    mycursor = cnxn.cursor()
    mycursor.execute(sql)

    out = mycursor.fetchall()

    mycursor.close()
    cnxn.close()

    return out

def rec_help(user_id):
	cnxn = mysql.connector.connect(**config)

	mycursor = cnxn.cursor()

	arg = [user_id]
	out = []
	mycursor.callproc('RecommendMovies', arg)

	for result in mycursor.stored_results():
		for movie in result.fetchall():
			out.append({"movie_id" : movie[0], "movie_name" : movie[1], "movie_rating" : float(movie[3])})

	mycursor.close()
	cnxn.close()

	return out


def fav_help(user_id):
	sql = "SELECT * FROM liked WHERE user_id = '{0}'".format(user_id)

	cnxn = mysql.connector.connect(**config)

	mycursor = cnxn.cursor()
	mycursor.execute(sql)

	out = []
	for ids in mycursor.fetchall():
		sql2 = "SELECT * FROM movies WHERE movie_id = '{0}'".format(ids[1])
		mycursor.execute(sql2)
		out.append((ids[1], mycursor.fetchall()[0][1]))

	mycursor.close()
	cnxn.close()

	return out

def fav_delete_help(mov_id, user_id):
    sql = "DELETE FROM liked WHERE movie_id = '{0}' and user_id = '{1}'".format(mov_id, user_id)

    cnxn = mysql.connector.connect(**config)

    mycursor = cnxn.cursor()
    mycursor.execute(sql)
    cnxn.commit()   # commit the changes

    mycursor.close()
    cnxn.close()

def fav_add_help(mov_id, user_id):
	sql_check = "SELECT * FROM movies WHERE movie_title = '{0}'".format(mov_id)


	cnxn = mysql.connector.connect(**config)

	mycursor = cnxn.cursor()
	mycursor.execute(sql_check)
	out = mycursor.fetchall()
	if len(out) == 1:
		sql = "INSERT INTO liked (user_id, movie_id) VALUES ('{0}', '{1}')".format(user_id, out[0][0])
		mycursor.execute(sql)
		cnxn.commit()   # commit the changes

	mycursor.close()
	cnxn.close()


def rating_help(movie_id, user_rate):

	cnxn = mysql.connector.connect(**config)

	mycursor = cnxn.cursor()

	sql_get = "SELECT * FROM movies WHERE movie_id = '{0}'".format(movie_id)
	mycursor.execute(sql_get)
	out = mycursor.fetchall()
	rating = float(out[0][3])
	num_rating = out[0][4]


	new_rating = ((num_rating*rating)+float(user_rate))/(num_rating+1)
	new_num_ratings = num_rating+1

	sql = "UPDATE movies SET avg_rating = '{1}', num_ratings = '{2}' WHERE movie_id = '{0}'".format(movie_id, new_rating, new_num_ratings)

	mycursor.execute(sql)
	cnxn.commit()   # commit the changes

	mycursor.close()
	cnxn.close()
