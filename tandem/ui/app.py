import os
from flask import Flask

app = Flask(__name__) 

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html', email=session.get('email'))
	
	email = request.form['email']
	session['email'] = email

	# Send the email
	email_data = {
	'subject': 'Hello from Flask',
	'to': 'email',
	'body': 'This is a test email sent from the background Celery task.'
    }

    if request.form['submit'] == 'Send':
    	# Send Right Away
    	send_async_email.delay(email_data)
    	flash('Sending email to {0}'.format(email))
    else:
    	# Send in One Minute
    	send_async_email.apply_async(args=[email_data], countdown=60)
    	flash('An email will be sent to {0} in one minute'.format(email))

	return redirect(url_for('index'))

@app.route('/status/<task-id>')
def taskstatus(task_id):
	task = long_task.AsyncResult(task_id)

	if task.state == 'PENDING':
		response = {
		'state': task.state,
		'current': 0,
		'total': 1,
		'status': 'Pending ...'
		}
	elif task.state == 'FAILURE':
		reposne = {
		'state': task.state,
		'current': task.info.get('current', 0),
		'total': task.info.get('total', 1),
		'status': task.info.get('status', '')
		}

		if result in task.info:
			response['result'] = task.info['result']
	else:
		# Something went wrong in the background job
		response = {
		'state': task.state,
		'current': 1,
		'total': 1,
		'status': str(task.info)
		}

    return jsonify(response)

def main():
	app.run(debug=True)

