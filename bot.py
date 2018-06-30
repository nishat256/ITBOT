from docParser import readSampleInputDoc3,readSampleInputDoc2
from main import queryDataBase,TF_IDF
from tinydb import TinyDB
sampleDoc2=TinyDB('sampleDoc2.json')
def botBrain(text,source,session):
	if source=="button":
		if text.lower()=='troubleshooting' or 'troubleshooting' in session.get('context','').lower():
			if session.get('context','').lower()=='troubleshooting':
				resp=readSampleInputDoc3(True)
				response=resp[text]
				symptoms=[x['symptom'] for x in response]
				session['context']=text +" symptom"
				return (symptoms,['choose symptom'])
			elif 'symptom' in session.get('context',''):
				resp=readSampleInputDoc3(True)
				response=resp[session['context'].replace(' symptom','')]
				answer=[x['diagnosis'] for x in response if x['symptom']==text]
				session['context']=""
				session['endFlag']=True
				return (['issue resolved?','still facing issue?'],answer)
			else:
				resp=readSampleInputDoc3(True)
				response=resp.keys()
				context=text.lower()
				session['context']=context
				return (response,['Choose specific troubleshooting from side options'])

		elif text.lower()=='performance issue' or session.get('context','').lower()=='performance issue':
			print(session.get('context','').lower(),'inside')
			if session.get('context','').lower()=='performance issue':
				resp=sampleDoc2.all()
				LystOfSolution=[x['topic'] for x in resp if x['root']==text]
				print(LystOfSolution,'fa')
				answer=[]
				for item in LystOfSolution[0]:
					answer.append("<strong>"+item['problem']+"</strong><br>"+item['solution'])

				session['context']=""
				return (['issue resolved?','still facing issue?'],answer)
				
			else:
				session['context']=text.lower()
				#resp=readSampleInputDoc2()
				resp=sampleDoc2.all()
				#response=[x['Question'] for x in resp]
				response=[x['root'] for x in resp]
				print(response)
				return (response,['which performance issue are you facing?'])

		elif text.lower()=='account related' or session.get('context','').lower()=='account related':
			if session.get('context','').lower()=='account related':
				if text=='Password reset':
					session['context']=""
					return(['issue resolved?','still facing issue?'],['go to url : password.reset.com, enter you login id, enter password received, reset the password'])
				elif text=='New Account Setup':
					session['context']=""
					return(['issue resolved?','still facing issue?'],['go to url : accountsetup.com, enter personal details along with user id, enter otp received, click finish. check email for details'])
				

			else:
				session['context']=text.lower()
				return (['Password reset','New Account Setup'],['Choose one of the option'])
	elif source=="textField":
		session['context']=""
		optionTuple=('troubleshooting','performance issue','account related')
		response=queryDataBase(text)
		if not response:
			result=TF_IDF(text)
			if not result:
				answer=["Sorry,I don't have answer for your query","Do you want to connect with live agent?","select option from right panel"]
				return(['Yes,I want to connect with live agent',"No,I don't want to connect with live agent"],answer)
			else:
				result=result[0][1]
				answer=[result,"Most relevant answer for your query but I'm not 100% sure"]
				return(['issue resolved?','still facing issue?'],answer)
		else:
			bot_answer=[response[0]]

		return (optionTuple,bot_answer)


if __name__ == '__main__':
	context=""
	print("Hello, I'm Vince \n How can I help you ?")
	while True:
		print('Choose one option:')
		text=input()
		response=botBrain(text,True)