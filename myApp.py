from flask import Flask,render_template,request,jsonify,session
from tinydb import TinyDB, Query
from main import TF_IDF,queryDataBase
from bot import botBrain
db = TinyDB('db.json')
app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def hello_world():
	if request.method=='POST':
		query=request.form['query'].strip()
		if not query:
			return 'Empty Field'
		response=queryDataBase(query)
		if not response:

			response=TF_IDF(query)
		
			return render_template('index.html',data=(query,response,'multiple'))
		return render_template('index.html',data=(query,response,'single'))
	return render_template('index.html',data=None)
@app.route('/reDisplay',methods=['POST'])
def reDisplay():
	if request.method=='POST':
		query=request.form['query'].strip()
		response=TF_IDF(query)
		return render_template('index.html',data=(query,response,'multiple'))
		
@app.route('/bot',methods=['GET','POST'])
def bot_page():
	session['context']=""
	return render_template('bot.html')


@app.route('/storeAnswer',methods=['POST'])
def storeAnswer():
	if request.method=='POST' and 'form1' in request.form :
		answer=request.form['correctAnswer']
		query=request.form['query']
		if answer=='none':
			return render_template('submitResolution.html',data=query)

	elif request.method=='POST' and 'formRes' in request.form:
		answer=request.form['resolution']
		query=request.form['query']
	elif request.method=='POST' and 'issueResolved' in request.form:
		answer=request.form['answer']
		query=request.form['query']
		per=request.form['per']
		if float(per) > .8 :
			return "Thank you for your feedback <br/> <a href='/'>click here to go to home page</a>"

	dbObject = Query()
	resp=db.search(dbObject.Answer==answer)
	if not resp:
		db.insert({'Question':query,'Answer':answer})
	else:
		db.update({'Question':resp[0]['Question']+' '+query},dbObject.Answer==answer)
	return "Thank you for your feedback<br/> <a href='/'>click here to go to home page</a>"
@app.route('/bot/response',methods=['GET','POST'])
def return_response():
	query=request.form['text']
	source=request.form['source']
	optionTuple=('troubleshooting','performance issue','account related')
	html_string_box=""
	html_string_sideMenu=""
	if source=='button':
		if 'issue resolved?' in query or "No,I don't want to" in query:
			html_string_box="<li id='bot_box' class='left clearfix'>Thank you for contacting IT Support Help Desk</li>"
			for item in optionTuple:
				html_string_sideMenu+="<li class='sideoption'>"+item+"</li>"
			return jsonify({'response_box':html_string_box,'response_sideMenu':html_string_sideMenu})
		elif 'facing' in query or 'Yes,I want to connect' in query:
			html_string_box="<li id='bot_box' class='left clearfix'>Ok please wait, connecting you with live agent...</li>"
			for item in optionTuple:
				html_string_sideMenu+="<li class='sideoption'>"+item+"</li>"
			return jsonify({'response_box':html_string_box,'response_sideMenu':html_string_sideMenu})
   
	print(session.get('context'),'efwr')
	response=botBrain(query,source,session)
	
	for item in response[0]:
		html_string_sideMenu+="<li class='sideoption'>"+item+"</li>"
	for item in response[1]:
		html_string_box+="<li id='bot_box' class='left clearfix'>"+ item +"</li>"
	

	return jsonify({'response_box':html_string_box,'response_sideMenu':html_string_sideMenu})

if __name__ == '__main__':
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.secret_key='super secret key '
	app.run(debug=True,port=9090)