import flask
from flask import Flask
from flask import (abort, flash, redirect, render_template, request, session, url_for)
import requests as REST
import uuid, json

import utils as db_utils


#pip install --upgrade google-auth-oauthlib==0.3.0
#will get auth error if not v 0.3.0


SESSION_COOKIE_SECURE = True
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def base():
	return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
def home():
	try:
		id = session["user_id"]
	except Exception as e:
		session["user_id"] = "1"

	if request.method == 'GET':
		return render_template("home.jinja2")
	elif request.method == 'POST':
		for key, value in request.form.to_dict().items():
			if value == "button_insert":
				return redirect(url_for('insert'))
			elif value == "button_search":
				return redirect(url_for('search'))
			elif value == "button_update":
				return redirect(url_for('update'))
			elif value == "button_delete":
				return redirect(url_for('delete'))
			elif value == "button_adv":
				return redirect(url_for('advq'))
			elif value == "rec_m":
				return redirect(url_for('recm'))
			elif value == "button_setid":
				return redirect(url_for('setid'))
			elif value == "fav":
				return redirect(url_for('favorites'))
			elif value == "ratings":
				return redirect(url_for('ratings'))
			else:
				return redirect(url_for('home'))

@app.route('/setid', methods=['GET', 'POST'])
def setid():
	if request.method == 'GET':
		return render_template("setid.jinja2", user_id = session["user_id"])
	elif request.method == 'POST':
		try:
			if request.form['button_setid'] == "button_setid":
				print(request.form['user_id'])
				session["user_id"] = request.form['user_id']
				return render_template("setid.jinja2", user_id = session["user_id"])
		except Exception as ex:
			print(ex)
		return redirect(url_for('home'))

@app.route('/insert', methods=['GET', 'POST'])
def insert():
	if request.method == 'GET':
		return render_template("insert.jinja2")
	elif request.method == 'POST':
		try:
			if request.form['insert_dir'] == "insert_dir":
				db_utils.insert_help({"director_id" : request.form['insert_id'], "name" : request.form['insert_name'], "birth_year" : request.form['insert_birth']})
				return render_template("insert.jinja2")
		except Exception as ex:
			print(ex)

		return redirect(url_for('home'))

@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		search_data = {"status" : False, "out" : []}
		session["search_data"] = search_data
		return render_template("search.jinja2", search_data = search_data)
	elif request.method == 'POST':
		try:
			if request.form['search_dir_id'] == "search_dir_id":
				search_data = session["search_data"]
				search_data["out"] = db_utils.search_help_id(request.form['search_id'])
				search_data["status"] = True
				session["search_data"] = search_data
				return render_template("search.jinja2", search_data = search_data)
		except Exception as ex:
			print(ex)
		try:
			if request.form['search_dir_name'] == "search_dir_name":
				search_data = session["search_data"]
				search_data["out"] = db_utils.search_help_name(request.form['search_name'])
				search_data["status"] = True
				session["search_data"] = search_data
				return render_template("search.jinja2", search_data = search_data)
		except Exception as ex:
			print(ex)
		try:
			if request.form['search_dir_birth'] == "search_dir_birth":
				search_data = session["search_data"]
				search_data["out"] = db_utils.search_help_birth(request.form['search_birth'])
				search_data["status"] = True
				session["search_data"] = search_data
				return render_template("search.jinja2", search_data = search_data)
		except Exception as ex:
			print(ex)
		

		return redirect(url_for('home'))

@app.route('/update', methods=['GET', 'POST'])
def update():
	if request.method == 'GET':
		return render_template("update.jinja2")
	elif request.method == 'POST':
		try:
			if request.form['update_dir'] == "update_dir":
				db_utils.update_help({"director_id" : request.form['insert_id'], "name" : request.form['insert_name'], "birth_year" : request.form['insert_birth']})
				return render_template("update.jinja2")
		except Exception as ex:
			print(ex)

		return redirect(url_for('home'))


@app.route('/delete', methods=['GET', 'POST'])
def delete():
	if request.method == 'GET':
		return render_template("delete.jinja2")
	elif request.method == 'POST':
		try:
			if request.form['delete_dir'] == "delete_dir":
				db_utils.delete_help(request.form['search_id'])
				return render_template("delete.jinja2")
		except Exception as ex:
			print(ex)

@app.route('/advq', methods=['GET', 'POST'])
def advq():
	if request.method == 'GET':
		q_data = {"status" : False, "out" : []}
		session["q_data"] = q_data
		return render_template("adv.jinja2", q_data = q_data)
	elif request.method == 'POST':
		try:
			if request.form['adv_q_r'] == "adv_q_r":
				q_data = session["q_data"]
				q_data["status"] = True
				q_data["out"] = db_utils.adv_help()
				session["q_data"] = q_data
				return render_template("adv.jinja2", q_data = q_data)
		except Exception as ex:
			print(ex)
		

		return redirect(url_for('home'))


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
	fav = db_utils.fav_help(session["user_id"])
	if request.method == 'GET':
		return render_template("favorites.jinja2", fav = fav)
	elif request.method == 'POST':
		for key, value in request.form.to_dict().items():
			if key == "rem_fav":
				db_utils.fav_delete_help(value, session["user_id"])
				fav = db_utils.fav_help(session["user_id"])
				return render_template("favorites.jinja2", fav=fav)
			elif key == "add_fav":
				db_utils.fav_add_help(request.form['fav_add'], session["user_id"])
				fav = db_utils.fav_help(session["user_id"])
				return render_template("favorites.jinja2", fav=fav)
		return redirect(url_for('home'))



@app.route('/recm', methods=['GET', 'POST'])
def recm():
	if request.method == 'GET':
		q_data = {"status" : False, "out" : []}
		session["q_data_rec"] = q_data
		return render_template("recommend.jinja2", q_data = q_data, user_id = session["user_id"])
	elif request.method == 'POST':
		try:
			if request.form['recm_r'] == "recm_r":
				q_data = session["q_data_rec"]
				q_data["status"] = True
				q_data["out"] = db_utils.rec_help(session["user_id"])
				session["q_data_rec"] = q_data
				return render_template("recommend.jinja2", q_data = q_data, user_id = session["user_id"])
		except Exception as ex:
			print(ex)

		return redirect(url_for('home'))


@app.route('/ratings', methods=['GET', 'POST'])
def ratings():
	if request.method == 'GET':
		return render_template("ratings.jinja2")
	elif request.method == 'POST':
		try:
			if request.form['add_rating'] == "add_rating":
				db_utils.rating_help(request.form['m_id'], request.form['n_rating'])
				return render_template("ratings.jinja2")
		except Exception as ex:
			print(ex)

		return redirect(url_for('home'))

'''
@app.route("/home_unauth")
def home_unauth():
	if session.get("is_authenticated"):
		return redirect(url_for('home'))
	else:
		if request.method == 'GET':
			return render_template("home.jinja2")
		else:
			for key, value in request.form.to_dict().items():
				if value == "button_insert":
					return redirect("https://www.google.com")
				elif value == "button_search":
					return redirect("https://www.google.com")
				elif value == "button_update":
					return redirect("https://www.google.com")
				elif value == "button_delete":
					return redirect("https://www.google.com")
				elif value == "button_adv":
					return redirect("https://www.google.com")
				else:
					return redirect("yahoo.com")

@app.route('/login', methods=['GET'])
def login():
    """Send the user to Globus Auth."""
    return redirect(url_for('authcallback'))

@app.route('/authcallback', methods=['GET'])
def authcallback():
    if 'error' in request.args:
        flash("You could not be logged into the application: " +
              request.args.get('error_description', request.args['error']))
        return flask.redirect(url_for(''))
    if 'code' not in request.args:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', "https://www.googleapis.com/auth/userinfo.profile"])
        flow.redirect_uri = flask.url_for('authcallback', _external=True)
        authorization_url, state = flow.authorization_url(
            access_type='offline', include_granted_scopes='true')
        flask.session['state'] = state
        return flask.redirect(authorization_url)
    else:
        code = request.args.get('code')
        state = flask.session['state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', "https://www.googleapis.com/auth/userinfo.profile"],
            state=state)
        flow.redirect_uri = flask.url_for('authcallback', _external=True)
        authorization_response = flask.request.url
        flow.fetch_token(authorization_response=authorization_response)
        auth_sess = flow.authorized_session()
        id_token = verify_oauth2_token(auth_sess.credentials.id_token, requests.Request())

        """
        EXAMPLE VERIFICATION
        data = json.load(open("world_data.json"))
        if id_token["email"] in data["server_data"]["users"]:
            session.update(id_token = id_token, is_authenticated=True, email=id_token["email"], user_name=id_token["name"])
            return flask.redirect(flask.url_for('home'))
        else:
            session.update(id_token = id_token, is_authenticated=False, email=id_token["email"], user_name=id_token["name"])
            return flask.redirect(flask.url_for('logout'))
        """

        session.update(id_token = id_token, is_authenticated=True, email=id_token["email"], user_name=id_token["name"])
        return flask.redirect(flask.url_for('home'))



@app.route('/logout', methods=['GET'])
@authenticated
def logout():
    revoke = REST.post('https://accounts.google.com/o/oauth2/revoke',
        params={'id_token': session.get("id_token")},
        headers = {'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return "Something Failed, please go <a href="+redirect(url_for('home_unauth'))+">back</a> :(" 

    session.clear()
    return redirect(url_for('home_unauth'))

@app.route('/home', methods=['GET', 'POST'])
@authenticated
def home():
    if request.method == 'GET':
        return render_template("home.jinja2")
    else:
        for key, value in request.form.to_dict().items():
            if value == "button_id":
                return redirect("https://www.google.com")
            else:
                return redirect(url_for('home'))
'''

if __name__ == "__main__":
    app.secret_key = str(uuid.uuid4())
    app.run(port="8080", debug=True, ssl_context='adhoc')
