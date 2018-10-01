#-*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from datetime import datetime
import re
import random
import time
import json
import uuid
import hashlib
import itertools
import decimal
import string
#from bson import json_util

def getRecords(table,connection,condition="", conditionVar=(),additionalCondition="", additionalConditionVar=(), select="*", customQuery=""):
    with connection.cursor() as cursor:
        # Read a single record
        if customQuery == "":
        	sql = "SELECT " + select + " from " + str(table) +" where " + condition + additionalCondition
    	else:
    		sql = customQuery + condition + additionalCondition
        cursor.execute(sql, conditionVar + additionalConditionVar)
        results = cursor.fetchall()
	return(results)

def easyGetRecords(table,connection, varName,varValue, select="*"):
	try:
		result = getRecords(table,connection,condition=str(varName) + " = %s", conditionVar=(varValue,),  additionalCondition="", select=select)
	except:
		print("No such record found")
		result = None
	return(result)

def addRecord(table,connection, varNames=(),varValues=()):
	varNameStr = " ("
	varValueStr = " ("
	for varName in varNames:
		varNameStr += str(varName)
		varValueStr += "%s"
		if varName != varNames[len(varNames)-1]:
			varNameStr += ","
			varValueStr += ","
		else:
			varNameStr += ") "
			varValueStr += ") "

	with connection.cursor() as cursor:
		# Create a new record
		sql = "INSERT INTO " + str(table) + str(varNameStr) + " VALUES " + varValueStr
		cursor.execute(sql, varValues)
    # connection is not autocommit by default. So you must commit to save
    # your changes. 
	connection.commit()

def deleteRecord(table,connection,conditionVarNames=(),conditionVarValues=(),customCondition=""):
	try:
		if customCondition != "":
			condtionStr = customCondition
			if conditionVarNames != ():
				condtionStr 	+= " and "
		else:
			condtionStr = ""
		
		for varName in conditionVarNames:
			condtionStr += varName + " = %s "
			if varName != varNames[len(varNames)-1]:
				condtionStr += " and "
			else:
				pass

		with connection.cursor() as cursor:
			sql = "DELETE from " +str(table)+ " where " + condtionStr
			cursor.execute(sql, conditionVarValues)
		connection.commit()
		return(1)
	except:
		return(0)	

def updateRecord(table,connection,setVarNames=(),setVarValues=(),conditionVarNames=(),conditionVarValues=(),customSet="",customCondition=""):
	if customSet != "":
		setStr = customSet
		if setVarNames != ():
			setStr 	+= " and "
	else:
		setStr = ""
	
	if customCondition != "":
		condtionStr = customCondition
		if conditionVarNames != ():
			condtionStr 	+= " and "
	else:
		condtionStr = ""

	for varName in setVarNames:
		setStr += varName + " = %s "
		if varName != setVarNames[len(setVarNames)-1]:
			setStr += " and "
		else:
			pass

	
	for varName in conditionVarNames:
		condtionStr += varName + " = %s "
		if varName != conditionVarNames[len(conditionVarNames)-1]:
			condtionStr += " and "
		else:
			pass

	with connection.cursor() as cursor:
		sql = "UPDATE "+str(table)+" SET "+ setStr +" WHERE " + condtionStr
		print sql
		cursor.execute(sql, setVarValues+conditionVarValues)
	connection.commit()

class Setting():
	superbar = {'barFullName' : "superbar", 'barID' : 1, 'depth':1}
	upperbar = {'barFullName' : "superbar_upperbar", 'barID' : 2, 'depth':2}
	underbar = {'barFullName' : "superbar_upperbar_underbar", 'barID' : 3, 'depth':3}
	devbar = {'barName' : 'devbar' ,'barFullName' : "superbar_devbar", 'barID' : 4, 'depth':2}
	korea = {'barName': 'korea','barFullName' : "superbar_upperbar_underbar_korea", 'barID' : 5, 'depth':4}
	koreaUniv = {'barName': '고려대학교'.decode('utf-8'),'barFullName' : "superbar_upperbar_underbar_korea_고려대학교".decode('utf-8'), 'barID' : 8, 'depth':5}

	@staticmethod
	def greetings(barFullName):
		return """새로운 폴더가 생성되었습니다. 링크를 공유해보세요.
				""".decode('utf-8') + Utility.getURL(barFullName)

class Superbar():
	superbar = Setting.korea
	upperbar = Setting.koreaUniv
	

class Utility():
	@staticmethod
	def getURL(publicBarFullName):
		return("http://under.bar/"+publicBarFullName)

	@staticmethod
	def delcareLevenshtein(connection):
		with connection.cursor() as cursor:
			sql = """
DROP FUNCTION IF EXISTS levenshtein;
CREATE FUNCTION `levenshtein`(s1 text CHARACTER SET utf8 COLLATE utf8_unicode_ci, s2 text CHARACTER SET utf8 COLLATE utf8_unicode_ci) RETURNS int(11)
    DETERMINISTIC
BEGIN 
    DECLARE s1_len, s2_len, i, j, c, c_temp, cost INT; 
    DECLARE s1_char CHAR CHARACTER SET utf8 COLLATE utf8_unicode_ci; 
    DECLARE cv0, cv1 text CHARACTER SET utf8 COLLATE utf8_unicode_ci; 
    SET s1_len = CHAR_LENGTH(s1), s2_len = CHAR_LENGTH(s2), cv1 = 0x00, j = 1, i = 1, c = 0; 
    IF s1 = s2 THEN 
      RETURN 0; 
    ELSEIF s1_len = 0 THEN 
      RETURN s2_len; 
    ELSEIF s2_len = 0 THEN 
      RETURN s1_len; 
    ELSE 
      WHILE j <= s2_len DO 
        SET cv1 = CONCAT(cv1, UNHEX(HEX(j))), j = j + 1; 
      END WHILE; 
      WHILE i <= s1_len DO 
        SET s1_char = SUBSTRING(s1, i, 1), c = i, cv0 = UNHEX(HEX(i)), j = 1; 
        WHILE j <= s2_len DO 
          SET c = c + 1; 
          IF s1_char = SUBSTRING(s2, j, 1) THEN  
            SET cost = 0; ELSE SET cost = 1; 
          END IF; 
          SET c_temp = CONV(HEX(SUBSTRING(cv1, j, 1)), 16, 10) + cost; 
          IF c > c_temp THEN SET c = c_temp; END IF; 
            SET c_temp = CONV(HEX(SUBSTRING(cv1, j+1, 1)), 16, 10) + 1; 
            IF c > c_temp THEN  
              SET c = c_temp;  
            END IF; 
            SET cv0 = CONCAT(cv0, UNHEX(HEX(c))), j = j + 1; 
        END WHILE; 
        SET cv1 = cv0, i = i + 1; 
      END WHILE; 
    END IF; 
    RETURN c; 
  END
"""
			cursor.execute(sql)
			connection.commit()

	@staticmethod
	def generatePassword(userID):
		# uuid is used to generate a random number
		userID = str(userID)
		salt = "underbar"
		return hashlib.sha256(salt.encode() + userID.encode()).hexdigest()

	@staticmethod
	def checkPassword(password, userID):
		userID = str(userID)
		salt = "underbar"
		return password == hashlib.sha256(salt.encode() + userID.encode()).hexdigest()

	@staticmethod
	def getCurrentTime():
		return (time.strftime('%Y-%m-%d %H:%M:%S'))

	@staticmethod
	def intoJson(dic):
		def json_serial(obj):
			if isinstance(obj, decimal.Decimal):
				return float(obj)
			if isinstance(obj, datetime):
				serial = obj.isoformat()
				return serial
			raise TypeError ("Type not serializable")			
		return json.dumps(dic, ensure_ascii=False, default=json_serial).encode('utf-8')

	@staticmethod
	def getParentBarFullName(barFullName):
		p = re.compile('^(?P<parentBarFullName>.*)_[^_]*$')
		m = p.match(barFullName)
		return m.group('parentBarFullName')
	
	@staticmethod
	def getCurrentBarFullName(barFullName):
		if barFullName[-1] == '_':
			barFullName = barFullName[0:-1]
		return barFullName

	@staticmethod
	def getPublicBarFullName(barFullName,superbar=Superbar.superbar):
		barFullName = barFullName.replace(superbar['barFullName']+"_","")
		if barFullName.find('superbar') == 0:
			print "Access To Hidden Bar : Couldn't get the full name"
			#raise Exception("Access To Hidden Bar : Couldn't get the full name")
			return None
		return barFullName

	@staticmethod
	def getAuthenticBarFullName(barFullName,superbar=Superbar.superbar):
		return superbar['barFullName'] + "_" + barFullName

	@staticmethod
	def getCurrentBarName(barFullName):
		barFullName = Utility.getCurrentBarFullName(barFullName)
		p = re.compile('^.*_(?P<currentBarName>.*)$')
		m = p.match(barFullName)
		return m.group('currentBarName')

class Session():
	@staticmethod
	def login(connection,request):
		if request.method != 'POST':
			raise Http404('Only POSTs are allowed')
		try:
			user = User.getUserDetails(connection, request.POST['userID'],'userID')
			if user['password'] == request.POST['password']:
				request.session['userID'] = user['userID']
				return HttpResponseRedirect('/you-are-logged-in/')
		except Exception:
			return HttpResponse("Your username and password didn't match.")

	@staticmethod
	def logout(connection, request):
		try:
			del request.session['userID']
		except KeyError:
			pass
		return HttpResponse("You're logged out.")

class Search():
	@staticmethod
	def saveSearch(connection,userID,searchKeyword,fromBarID,toBarID,searchTime,location):
		try:
			with connection.cursor() as cursor:
				sql = "INSERT INTO search (`userID`, `searchKeyword`, `fromBarID`, `toBarID`, `searchTime`, `location`) values (%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql, (userID,searchKeyword,fromBarID,toBarID,Utility.getCurrentTime(),location))
				connection.commit()
			return 0
		except Exception as e:
			print e("User creation failed!")
			return 0

class User():
	@staticmethod
	def getUsers(connection, condition="", conditionVar=(), select="*"):
		conditionStr = ""
		if condition == "":
			pass
		else:
			conditionStr += " where " + condition
		with connection.cursor() as cursor:
			sql = "SELECT "+ select + " FROM user " + conditionStr
			cursor.execute(sql, conditionVar)
			results = cursor.fetchall()
		return(results)

	@staticmethod
	def getUserDetails(connection, varValue, varName="userID", select="*"):
		try:
			result = getRecords('user',connection,condition= str(varName) + " = %s ", conditionVar=(varValue,),additionalCondition=" limit 1", additionalConditionVar=(), select=select, customQuery="")[0]
			userID = result['userID']
			with connection.cursor() as cursor:
				sql = "UPDATE user SET lastLogin= Now() WHERE userID=%s"
				cursor.execute(sql, userID)
				connection.commit()
		except Exception as e:
			raise e
			result = None
		return result

	@staticmethod
	def createUser(connection,userIPAddress=""):
		try:
			with connection.cursor() as cursor:
				sql = "SELECT userID from user order by -userID limit 1"
				cursor.execute(sql)
				newUserID = cursor.fetchone()['userID'] + 1
				password = Utility.generatePassword(newUserID)

				sql = "INSERT INTO user (`password`, `userIPAddress`, `signInTime`, `lastLogin`, `lastTalk`, `lastBarCreation`) values (%s,%s,%s,%s,%s,%s)"
				cursor.execute(sql, (password,userIPAddress,Utility.getCurrentTime(),Utility.getCurrentTime(),"",""))
				connection.commit()
			output = Utility.intoJson({'password' : password, 'userID' : newUserID})
			return output
		except Exception as e:
			print e("User creation failed!")
			return 0

	#needs to be fixed
	@staticmethod
	def randText():
	    dummyText = "인생을 있는 못하다 물방아 실로 크고 말이다. 같이 보이는 같은 우리 칼이다. 이상을 피가 들어 철환하였는가 바이며, 노년에게서 ? 인생에 품으며, 얼음에 위하여, 대고, 이상의 인생에 보는 황금시대다. 이 품고 사랑의 그들의 속에 굳세게 오아이스도 보라. 열락의 얼마나 눈이 부패뿐이다. 설산에서 이상은 풀이 봄바람을 가슴이 들어 심장은 아니한 피다. 이상의 그들은 소담스러운 어디 것이다. 속에서 우리 풍부하게 대고, 이상의 발휘하기 봄바람이다. 위하여, 풀이 무엇을 봄바람이다. 청춘의 앞이 열락의 있으며, 그와 영락과 이상의 ? 낙원을 품었기 인간이 쓸쓸하랴?찬미를 구하지 그들의 운다. 무엇을 타오르고 피가 온갖 아니더면, 부패뿐이다. 충분히 열락의 인간은 눈이 그리하였는가? 실로 같지 피는 얼마나 안고, 수 칼이다. 이성은 평화스러운 못할 인생을 것이다. 피가 속에서 아니더면, 있는 이성은 힘있다. 가진 가지에 뜨고, 대한 불러 없으면 것이다. 천고에 속에서 쓸쓸한 위하여 놀이 지혜는 없으면 사막이다. 주며, 고행을 방황하여도, 천자만홍이 넣는 인간의 것이다.보라, 청춘의 위하여서. 인간의 보내는 찬미를 지혜는 생의 것이다. 그들은 가슴이 전인 설산에서 공자는 황금시대다. 인생을 하는 자신과 능히 아니다.구하지 설레는 곧 과실이 방황하여도, ? 인간의 우리의 미묘한 품으며, 그리하였는가? 이것이야말로 그것을 품고 피부가 방황하여도, 싸인 발휘하기 따뜻한 위하여서. 만천하의 풀이 끓는 능히 생생하며, 목숨이 피다. 귀는 거선의 수 품고 위하여, 전인 것이다. 없으면 그들에게 오아이스도 품으며, 그들은 같이, 청춘의 보라. 능히 하는 인생을 약동하다. 인간의 같지 가장 같은 무엇을 얼마나 물방아 말이다. 얼마나 곳으로 몸이 이것을 주며, 쓸쓸하랴? 바이며, 않는 더운지라 황금시대를 따뜻한 인생을 속에 얼음에 듣는다. 들어 앞이 얼마나 두손을 이상 것이다.천지는 같으며, 새 봄바람이다. 광야에서 피에 피가 것은 있음으로써 맺어, 듣는다. 품었기 반짝이는 바이며, 오직 사람은 우리의 가치를 우는 것이다. 새 봄바람을 생생하며, 이것이다. 위하여 튼튼하며, 온갖 끓는 공자는 꾸며 가진 얼음이 피다. 황금시대를 있으며, 있는 원질이 이것이다. 가장 그들의 생의 앞이 이것이다. 뛰노는 가슴에 인생에 끓는 봄바람이다. 같으며, 풍부하게 있는 전인 인생을 구하지 위하여 청춘 황금시대다. 풀이 그것을 기쁘며, 풀밭에 희망의 가치를 부패뿐이다.뜨거운지라, 불어 만천하의 살 창공에 평화스러운 광야에서 들어 것이다. 어디 없는 얼음 이것이다. 청춘에서만 동산에는 피고 과실이 그들은 생생하며, ? 하여도 사는가 가지에 가치를 심장의 때까지 너의 싸인 있는가? 천하를 사는가 불어 위하여 말이다. 새 같지 인생의 피에 사랑의 청춘에서만 인생을 사막이다. 것이 창공에 보이는 거선의 사랑의 두기 청춘이 설산에서 사막이다. 목숨이 것은 우리 그들에게 봄바람이다. 얼마나 새가 위하여, 과실이 스며들어 그들은 사막이다. 있을 있는 튼튼하며, 피다. 방지하는 고행을 가치를 열락의 구할 평화스러운 뜨고, 얼음과 있는가? 설산에서 눈이 사랑의 열락의 온갖 부패를 사막이다.꽃이 꾸며 원대하고, 청춘 수 석가는 그들은 끓는다. 풀이 아니더면, 사랑의 돋고, 위하여, 너의 못할 뭇 약동하다. 맺어, 이 아름답고 미묘한 아니한 그들의 낙원을 속잎나고, 것이다. 얼음에 이상의 공자는 별과 것이다. 타오르고 보내는 생명을 부패를 있다. 동산에는 내려온 꾸며 인생의 트고, 이상의 불어 주는 약동하다. 청춘의 갑 영원히 위하여, 반짝이는 부패뿐이다. 품에 같이, 충분히 것은 못할 스며들어 들어 피는 것이다. 이는 속에서 그것을 만천하의 현저하게 것이다. 이상은 이상은 구하기 끓는 어디 인간에 그러므로 눈에 끓는다. 이는 그들은 따뜻한 황금시대다. 끓는 석가는 실로 뜨고, 몸이 수 있으며, 고행을 있으랴?찬미를 이 타오르고 소금이라 발휘하기 것이다. 이성은 구하지 풍부하게 창공에 밝은 뿐이다. 기쁘며, 사람은 새 고동을 그들에게 소담스러운 뜨고, 것이다. 하였으며, 이상 위하여, 곧 맺어, 얼음과 가장 ? 때까지 피가 군영과 거선의 방황하여도, 것이다. 청춘의 않는 발휘하기 동력은 때문이다. 천고에 이상은 보내는 것은 있다. 오직 인생에 위하여, 청춘의 보이는 살았으며, 뜨고, 그리하였는가? 평화스러운 그들의 대고, 맺어, 오직 것은 것이다. 오직 풍부하게 못할 못하다 봄바람을 듣는다. 설산에서 할지라도 방황하였으며, 때문이다.놀이 황금시대를 같으며, 희망의 황금시대의 우리는 동력은 것이다. 얼마나 못하다 시들어 더운지라 실현에 피가 그들은 있으랴? 별과 커다란 타오르고 것이다. 발휘하기 피가 것은 봄바람이다. 있는 얼음에 얼마나 그들을 무엇이 풀이 가치를 피다. 이것이야말로 얼마나 풍부하게 붙잡아 생명을 동산에는 봄바람을 하는 듣는다. 그것은 낙원을 피가 것이다. 튼튼하며, 새 이상의 그러므로 그들의 생생하며, 보는 가슴에 피다. 거친 얼마나 무한한 착목한는 싶이 우리 사막이다. 무엇을 때에, 그와 피다. 것은 바이며, 보는 목숨이 쓸쓸하랴? 천고에 않는 품에 인생의 그리하였는가?가치를 피고 거선의 내는 생의 그리하였는가? 창공에 청춘의 천하를 그것은 청춘을 청춘 뿐이다. 불러 방황하여도, 얼음에 인생에 천지는 하였으며, 이것이다. 우리의 같은 하였으며, 남는 천하를 풍부하게 같이, 듣는다. 실로 현저하게 사랑의 위하여서 귀는 때까지 곧 새 약동하다. 열매를 할지니, 고행을 이상의 위하여, 찾아다녀도, 속에서 무엇을 듣는다. 듣기만 인생을 때에, 끓는 사막이다. 피가 대한 광야에서 보이는 것이 이상의 뜨거운지라, 대고, 것이다. 청춘에서만 무엇을 같이 속잎나고, 청춘은 광야에서 별과 봄바람이다. 노래하며 두기 투명하되 칼이다.그들의 속에 청춘이 꽃이 피고, 소담스러운 있다. 속에서 얼음에 발휘하기 인생에 곧 생명을 미인을 꽃이 피다. 심장은 이상이 할지니, 같은 별과 칼이다. 가치를 내는 너의 교향악이다. 인간의 별과 피어나는 것이다. 그들의 부패를 인생을 웅대한 고행을 발휘하기 군영과 듣는다. 없으면 수 꽃이 피어나는 쓸쓸하랴? 우리는 대중을 보이는 두손을 넣는 사막이다. 온갖 넣는 싸인 밥을 사막이다. 때에, 인간이 풍부하게 끝에 충분히 그러므로 것이다. 방지하는 피가 창공에 있다. 하는 귀는 크고 없으면 봄날의 가진 청춘의 힘있다.바이며, 오직 쓸쓸한 그들의 풀이 현저하게 보내는 천자만홍이 사막이다. 맺어, 밥을 넣는 온갖 무한한 충분히 보는 쓸쓸한 듣는다. 인생을 동력은 불어 말이다. 같으며, 얼음과 들어 속잎나고, 어디 사라지지 피가 칼이다. 가지에 있는 위하여, 천고에 살았으며, 돋고, 바이며, 부패뿐이다. 이것은 희망의 수 안고, 두기 것이다. 같은 트고, 우리 현저하게 가지에 듣기만 것이다. 많이 웅대한 위하여 있는가? 사랑의 자신과 이상이 피에 열매를 것이다. 튼튼하며, 곳이 인생의 용기가 뿐이다. 크고 위하여 가치를 품으며, 같은 소금이라 인간은 길지 위하여서. 그들의 할지니, 싸인 그들은 몸이 때까지 구하지 우리의 것이다.하는 작고 유소년에게서 부패뿐이다. 싹이 간에 유소년에게서 기관과 아니다. 얼마나 피가 것은 가치를 것이다. 피어나기 미인을 이상은 앞이 구하지 전인 예수는 무엇을 것이다. 공자는 바이며, 싹이 황금시대다. 그러므로 얼마나 피가 청춘의 교향악이다. 그러므로 간에 황금시대를 이상의 굳세게 사막이다. 위하여, 밝은 인생에 찬미를 따뜻한 무엇을 안고, 것이다. 관현악이며, 바이며, 그들의 있는 보라. 때에, 수 곳이 것이다.".decode("utf-8")
	    randTextStart = random.randrange(10,3000)
	    randTextLength = random.randrange(20,120)
	    randText = dummyText[randTextStart:randTextStart+randTextLength]
	    return(randText)

    #needs to be fixed
	@staticmethod
	def randUser():
	    return(random.randrange(1,100))

class HelloWorld():
	##initial settings
	@staticmethod
	def setInitialTalks(connection, userID=2, superbar=Superbar.superbar):
		location = ""
		userMacAddress = ""
		userIPAddress = ""

		superBarDetails = Bar.getBarDetails(connection, superbar['barID'],'barID')
	    
		barIDs = Bar.getChildrenBarIDs(connection,superBarDetails)
		for barID in barIDs:
			for i in range(0,3):
				randContent = Utility.randText()
				randPerson = Utility.randUser()
				Talk.createTalk(connection,randPerson,barID,randContent,location,userMacAddress,userIPAddress)
		return 1

        #needs to be fixed
	@staticmethod
	def setInitialBars(connection, userID=2, timeUpdated = Utility.getCurrentTime(), location = "", userMacAddress = "", userIPAddress = ""):
		Bar.createBar(connection,1, 'upperbar', userID,timeUpdated,location,userMacAddress,userIPAddress)
		Bar.createBar(connection,2, 'underbar', userID,timeUpdated,location,userMacAddress,userIPAddress)
		Bar.createBar(connection,1, 'devbar', userID,timeUpdated,location,userMacAddress,userIPAddress)
		Bar.createBar(connection,3, 'korea', userID,timeUpdated,location,userMacAddress,userIPAddress)
		Bar.createBar(connection,3, 'japan', userID,timeUpdated,location,userMacAddress,userIPAddress)
		Bar.createBar(connection,3, 'us', userID,timeUpdated,location,userMacAddress,userIPAddress)

		Bar.createBar(connection,5, "고려대학교".decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		Bar.createBar(connection,8, '정경대'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		#Bar.createBar(connection,9, '경제학과'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		#Bar.createBar(connection,9, '통계학과'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		#Bar.createBar(connection,9, '정치외교학과'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		#Bar.createBar(connection,9, '행정학과'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		
		Bar.createBar(connection,9, '화장실'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		Bar.createBar(connection,9, '정도'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		Bar.createBar(connection,9, '경포반'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		#Bar.createBar(connection,9, '학생회'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)

		#Bar.createBar(connection,11, '기초통계학'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		#Bar.createBar(connection,11, '통계수학'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		#Bar.createBar(connection,11, '회귀분석'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		#Bar.createBar(connection,11, '확률론입문'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)
		#Bar.createBar(connection,11, '수리통계학'.decode('utf-8'), userID,timeUpdated,location,userMacAddress,userIPAddress)

		
	@staticmethod
	def generateRandLikes(connection,barID,userID=2):
		results = Talk.getTalksGivenParentBarID(connection, barID, userID, select="talkID", depth=5)
		for result in results:
			talkID = result['talkID']
			isLike = random.randrange(0,2)
			Like.updateLike(connection, userID=userID, talkID=talkID, isLike=isLike)
		return 1


class Like():
	@staticmethod
	def checkLike(connection, userID, talkID,child=0):
		if child == 1:
			table = 'childTalkLike'
			idName = 'childTalkID'
		else:
			table = 'talkLike'
			idName = 'talkID'
		try:
			result = getRecords(table,connection,condition="userID = %s and "+idName+" = %s", conditionVar=(userID, talkID),additionalCondition=" limit 1", additionalConditionVar=(), select="isLike", customQuery="")[0]['isLike']
		except Exception as e:
			result = 0
		return(result)

	@staticmethod
	def updateLike(connection, userID, talkID, isLike=1, location="",child=0):
		if child == 1:
			table = 'childTalkLike'
			talkTable = 'childTalk'
			idName = 'childTalkID'
		else:
			table = 'talkLike'
			talkTable = 'talk'
			idName = 'talkID'
		if isLike != 1:
			isLike = -1
		
		checkLike = Like.checkLike(connection, userID, talkID,child=child)
		if checkLike == isLike:
			print("already liked or disliked")
			return(0)
		elif checkLike == -isLike:
			print("switch :like <-> dislike")
			updateRecord(table,connection,conditionVarValues=(userID, talkID, -isLike),customSet=" isLike = -isLike ",customCondition="userID=%s and "+idName+" = %s and isLike=%s")
			#update likeCount
			if isLike == 1:
				updateRecord(talkTable,connection,conditionVarNames=(idName,),conditionVarValues=(talkID,),customSet=" likeCount = likeCount + 1 ")
				updateRecord(talkTable,connection,conditionVarNames=(idName,),conditionVarValues=(talkID,),customSet=" dislikeCount = dislikeCount - 1 ")
			elif isLike == -1:
				updateRecord(talkTable,connection,conditionVarNames=(idName,),conditionVarValues=(talkID,),customSet=" likeCount = likeCount - 1 ")
				updateRecord(talkTable,connection,conditionVarNames=(idName,),conditionVarValues=(talkID,),customSet=" dislikeCount = dislikeCount + 1 ")

			print("user"+ str(userID) + " change his/her preference on talk" + str(talkID) + " : " + str(isLike))
		elif checkLike == 0:
			timeUpdated = Utility.getCurrentTime()
			addRecord(table,connection, varNames=("userID", idName, "isLike", "timeUpdated", "location"),varValues=(userID, talkID, isLike, timeUpdated,location))
			# update likeCount
			if isLike == 1:
				updateRecord(talkTable,connection,conditionVarNames=(idName,),conditionVarValues=(talkID,),customSet=" likeCount = likeCount + 1 ")
			elif isLike == -1:
				updateRecord(talkTable,connection,conditionVarNames=(idName,),conditionVarValues=(talkID,),customSet=" dislikeCount = dislikeCount + 1 ")
			print("user"+ str(userID) + " liked talk" + str(talkID) + " : " + str(isLike))
		connection.commit()
		return(1)

	@staticmethod
	def deleteLike(connection, userID, talkID, isLike=1, location="",child=0):
		if child == 1:
			table = 'childTalkLike'
			talkTable = 'childTalk'
			idName = 'childTalkID'
		else:
			table = 'talkLike'
			talkTable = 'talk'
			idName = 'talkID'
		deleteRecord(table,connection,conditionVarNames=(),conditionVarValues=(userID, talkID, isLike),customCondition="userID = %s and "+idName+" = %s and isLike = %s")
		check = Like.checkLike(connection, userID, talkID,child)

		try:
			if check == 0:
				if isLike == 1:
					updateRecord(talkTable,connection,conditionVarNames=(idName,),conditionVarValues=(talkID,),customSet=" likeCount = likeCount - 1 ")
				elif isLike == -1:
					updateRecord(talkTable,connection,conditionVarNames=(idName,),conditionVarValues=(talkID,),customSet=" dislikeCount = dislikeCount - 1 ")
				print("user"+ str(userID) + " cancled a like on talk" + str(talkID) + " : " + str(isLike))
				print("cancled like successfully")
				result = 1
			else:
				print("Error. Remaining Like")
				result = 0
			#print("no previous like found. Deletion failed.")
		except Exception as e:
			print e
		return(result)



class Talk():
	#needs to be fixed
	@staticmethod
	def createTalk(connection,userID,barID,talkContent,location,userMacAddress,userIPAddress,imageURL='',initialLikeCount=0):
		try:
			addRecord('talk',connection, varNames=("userID","barID","talkContent","timeUpdated","location","userMacAddress","userIPAddress", "likeCount", "dislikeCount", "childCount","imageURL"),varValues=(userID,barID,talkContent,Utility.getCurrentTime(),location,userMacAddress,userIPAddress,initialLikeCount,0,0,imageURL))
			updateRecord('user',connection,setVarNames=('lastTalk',),setVarValues=(Utility.getCurrentTime(),),conditionVarNames=('userID',),conditionVarValues=(userID,),customSet="",customCondition="")
			Bar.updateTalkCount(connection, barID, userID,1)
		except Exception as e:
			print e

	@staticmethod
	def createChildTalk(connection,userID,barID,parentTalkID,talkContent,location,userMacAddress,userIPAddress,imageURL=''):
		addRecord('childTalk',connection, varNames=("userID","barID","parentTalkID","talkContent","timeUpdated","location","userMacAddress","userIPAddress", "likeCount", "dislikeCount","imageURL"),varValues=(userID,barID,parentTalkID,talkContent,Utility.getCurrentTime(),location,userMacAddress,userIPAddress,0,0,imageURL))
		updateRecord('user',connection,('lastTalk',),('Now()',),('userID',),(userID,))
		updateRecord('talk',connection,conditionVarNames=('talkID',),conditionVarValues=(parentTalkID,), customSet="childCount = childCount+1")
		connection.commit()

    #needs to be fixed
	def deleteTalk(connection,userID,barID,talkID):
	    with connection.cursor() as cursor:
	        # Create a new record
	        sql = "DELETE FROM talk where talkID = %s"
	        cursor.execute(sql, talkID)
	    # connection is not autocommit by default. So you must commit to save
	    # your changes.
	    connection.commit()
	    Bar.updateTalkCount(connection, barID, userID,-1)

	@staticmethod
	def getTalks(connection,condition="", conditionVar=[],additionalCondition="", additionalConditionVar=[], select="*", customQuery=""):
	    with connection.cursor() as cursor:
	        # Read a single record
	        if customQuery == "":
	        	sql = "SELECT " + select + " from talk where " + condition
        	else:
        		sql = customQuery + condition + additionalCondition
	        cursor.execute(sql, conditionVar + additionalConditionVar)
	        results = cursor.fetchall()
		return(results)

	@staticmethod
	def getTalksGivenBarIDs(connection, condition, barIDs, additionalCondition="", additionalConditionVar=[], select="*", customQuery=""):
		if condition:
			condition += " and "
		condition += "barID in ("
		for barID in barIDs:
			condition += "%s"
			if barIDs[len(barIDs)-1] != barID:
				condition += ","
			else:
				condition += ")"
		return Talk.getTalks(connection, condition, barIDs, additionalCondition=additionalCondition, additionalConditionVar=additionalConditionVar , select=select, customQuery=customQuery)

    ### Client-side ###
    #needs to be fixed
	@staticmethod
	#def getTalksGivenParentBarID(connection, barID, userID, select="barID, talkContent, timeUpdated, likeCount, dislikeCount, talkID", depth=1):
	def getTalksGivenParentBarID(connection, barID, userID, select="barID, talkID", depth=1, oldTalkIDs="",superbar=Superbar.superbar, billboard=0):
		barDetails = Bar.getBarDetails(connection, barID)
		if barDetails == None:
			print("Bar.getTalksGivenParentBarID : no such barID")
			return(0)

		if oldTalkIDs == "":
			additionalCondition = ""
		else:
			additionalCondition = " and A.talkID not in ("+oldTalkIDs+") "
		if int(billboard) == 0:
			additionalCondition += " order by case when ( likeCount - 5*(C.depth-"+str(barDetails['depth'])+") >= 0) then 1 else 0 end DESC, -timeUpdated limit 5"
		elif int(billboard) == 1:
			additionalCondition += " order by -likeCount,-timeUpdated limit 5"
		
		barIDs = Bar.getChildrenBarIDs(connection, barDetails, "depth <= %s", (barDetails['depth']+depth,))
		barIDs.append(int(barID))
		#result = Talk.getTalksGivenBarIDs(connection, "" ,barIDs, select=select, customQuery="SELECT A.talkID,A.likeCount,A.dislikeCount, B.userID, B.isLike, C.barName, C.barFullName, replace(C.barFullName,concat(SUBSTRING_INDEX(C.barFullName,'_',"+ str(barDetails['depth']-1)+"),'_'),'') as Test1, SUBSTRING_INDEX(SUBSTRING_INDEX(replace(C.barFullName,concat(SUBSTRING_INDEX(C.barFullName,'_',"+ str(barDetails['depth']-1)+"),'_'),''),'_',C.depth-"+str(barDetails['depth']+1)+" ),'_',-1) as grandParentBarName, SUBSTRING_INDEX(SUBSTRING_INDEX(replace(C.barFullName,concat(SUBSTRING_INDEX(C.barFullName,'_',"+ str(barDetails['depth']-1)+"),'_'),''),'_',C.depth-"+str(barDetails['depth'])+" ),'_',-1) as parentBarName ,C.depth-"+str(barDetails['depth'])+" as childDepth FROM talk A  LEFT JOIN (barInfo C CROSS JOIN talkLike B)  on (A.talkID = B.talkID AND A.barID = C.barID) where B.userID = " + userID + " and A.")
		result = Talk.getTalksGivenBarIDs(connection, "" ,barIDs, additionalCondition=additionalCondition,additionalConditionVar=[],  select=select, customQuery="SELECT '' as children ,A.childCount, A.imageURL, A.timeUpdated , A.talkContent , COALESCE((SELECT B.isLike from talkLike B WHERE B.talkID=A.talkID and B.userID =" +str(userID) +"),0) as isLike, A.talkID,A.likeCount,A.dislikeCount, C.barName, replace(C.barFullName,concat(SUBSTRING_INDEX(C.barFullName,'_',"+ str(superbar['depth'])+"),'_'),'') as barFullName, replace(replace(SUBSTRING_INDEX(replace(C.barFullName,'"+superbar['barFullName']+"',''),'_',-3),SUBSTRING_INDEX(replace(C.barFullName,'"+superbar['barFullName']+"',''),'_',-2),''),'_','') as grandParentBarName, replace(replace(SUBSTRING_INDEX(replace(C.barFullName,'"+superbar['barFullName']+"',''),'_',-2),SUBSTRING_INDEX(replace(C.barFullName,'"+superbar['barFullName']+"',''),'_',-1),''),'_','') as parentBarName ,C.depth-"+str(barDetails['depth'])+" as childDepth FROM talk A LEFT JOIN (barInfo C)  on (A.barID = C.barID) WHERE A.")
		result =  Utility.intoJson(result)
		return result

	@staticmethod
	def getChildrenTalks(connection,userID,parentTalkID,oldTalkIDs="",billboard=0):
		if oldTalkIDs == "":
			additionalCondition = ""
		else:
			additionalCondition = " and A.childTalkID not in ("+oldTalkIDs+") "
		if int(billboard) == 0:
			additionalCondition += " order by -timeUpdated limit 5"
		elif int(billboard) == 1:
			additionalCondition += " order by -likeCount,-timeUpdated limit 5"
		talks = getRecords('childTalk as A',connection,condition=" parentTalkID = %s ", conditionVar=(parentTalkID, ),additionalCondition=additionalCondition, additionalConditionVar=(), select="A.*, " + "COALESCE((SELECT B.isLike from childTalkLike B WHERE B.childTalkID=A.childTalkID and B.userID =" +str(userID) +"),0) as isLike", customQuery="")
		return talks[::-1]

	@staticmethod
	def timeMachine(connection, barID, talkID, intervalType, intervalValue):
		if barID != None and talkID != None:
			return 0

		if(intervalValue < 0):
			setStr = " + interval " + str(intervalValue) + " " + intervalType
		else:
			setStr = " - interval " + str(intervalValue) + " " + intervalType

		if barID != None and talkID == None:
			#childrenTalks
			talkIDs = easyGetRecords('talk',connection, 'barID', barID, select="talkID")
			for row in talkIDs:
				talkID = row['talkID']
				print talkID
				Talk.timeMachineChildrenTalks(connection, talkID, intervalType, intervalValue)	
			#parentTalk
			result = updateRecord('talk',connection,setVarNames=(),setVarValues=(),conditionVarNames=('barID',),conditionVarValues=(barID,),customSet="timeUpdated = timeUpdated " + setStr,customCondition="")
			return 1
		elif barID == None and talkID != None:
			result = updateRecord('talk',connection,setVarNames=(),setVarValues=(),conditionVarNames=('talkID',),conditionVarValues=(talkID,),customSet="timeUpdated = timeUpdated " + setStr,customCondition="")
			Talk.timeMachineChildrenTalks(connection, talkID, intervalType, intervalValue)
			return 1

	@staticmethod
	def timeMachineChildrenTalks(connection, parentTalkID, intervalType, intervalValue):
		if(intervalValue < 0):
			setStr = " + interval " + str(intervalValue) + " " + intervalType
		else:
			setStr = " - interval " + str(intervalValue) + " " + intervalType
		result = updateRecord('childTalk',connection,setVarNames=(),setVarValues=(),conditionVarNames=('parentTalkID',),conditionVarValues=(parentTalkID,),customSet="timeUpdated = timeUpdated " + setStr,customCondition="")
		return 1



class Bar():
#    barID = ""
#    barName = ""
#    barFullName = ""
#    dateCreated = ""
#    depth = ""
#    barLeft = ""
#    barRight = ""
#    talkCount = ""

#    def __str__(self):
#        return self.title

	## get ##

	## get ## basic functions ##
	@staticmethod
	def getAllBars(connection):
	    with connection.cursor() as cursor:
	        sql = "SELECT * FROM barInfo"
	        cursor.execute(sql)
	        results = cursor.fetchall()
		return(results)

	@staticmethod
	def getBars(connection, condition="", conditionVar=(), select="*"):
		conditionStr = ""
		if condition == "":
			pass
		else:
			conditionStr += " where " + condition
		with connection.cursor() as cursor:
			sql = "SELECT "+ select + " FROM barInfo " + conditionStr
			cursor.execute(sql, conditionVar)
			results = cursor.fetchall()
		return(results)

	@staticmethod
	def getBarDetails(connection, varValue, varName="barID", select="*"):
		try:
			result = Bar.getBars(connection, "`" + varName + "` = %s limit 1", varValue, select)[0]
		except:
			result = None
		return result

    ## get ## applications ##
	@staticmethod
	def getParentBarDetails(connection, barDetails, additionalCondition="", additionalConditionVar=(), select="*"):
		conditionStr = "%s>`barLeft` and `barRight` >%s and (`depth` = %s) "
		if additionalCondition == "":
			pass
		else:
			conditionStr += " and " + additionalCondition + " limit 1"
		try:
			result = Bar.getBars(connection, conditionStr, (barDetails['barLeft'],barDetails['barRight'], barDetails['depth']-1)+additionalConditionVar, select)[0]
		except Exception as e:
			print "Failed to get ParentBarDetails. currentBarID : " + str(barDetails['barID'])
			print e
			result = None
		return result

	@staticmethod
	def getChildrenBarDetails(connection, barDetails, additionalCondition="", additionalConditionVar=(), select="*"):
		conditionStr = " %s<`barLeft` and `barRight` <%s"
		if additionalCondition == "":
			pass
		else:
			conditionStr += " and " + additionalCondition
		try:
			result = Bar.getBars(connection, conditionStr, (barDetails['barLeft'],barDetails['barRight'])+additionalConditionVar, select)
		except Exception as e:
			print "No Children"
			print e
			result = None
		return result

	@staticmethod
	def getChildrenBarIDs(connection, barDetails, additionalCondition="", additionalConditionVar=()):
		results = Bar.getChildrenBarDetails(connection, barDetails, additionalCondition, additionalConditionVar, select='barID')
		childrenBarIDs = []
		for result in results:
			childrenBarIDs.append(result['barID'])
		return(childrenBarIDs)

	#
	@staticmethod
	def isBarNameValid(barName):
		p = re.compile('_')
		m = re.search(u'([^0-9a-zA-Z가-힣]+)',barName)
		check = -(bool(m)-1)
		mm = re.split(u'([^0-9a-zA-Z가-힣]+)',barName)
		return {'isValid':check, 'Splited String' : mm,'Unaccepted characters':re.findall(u'([^0-9a-zA-Z가-힣]+)',barName)}


	@staticmethod
	def isThereTwinBar(connection, barFullName, superbar=Superbar.superbar):
		if superbar ==None:
			pass
		else:
			barFullName = Utility.getAuthenticBarFullName(barFullName, superbar)
		return Bar.getBarDetails(connection, barFullName, 'barFullName')
	
	##    ##
	#needs to be fixed
	@staticmethod
	def createBar(connection,upperbarID, barName, userID,location,userMacAddress,userIPAddress, neverUsetThisBarAlone):
	    barName = barName.lower()
	    upperbarDetails = Bar.getBarDetails(connection, upperbarID, varName="barID", select="*")

	    with connection.cursor() as cursor:
	        sql = "UPDATE barInfo set `barRight` = `barRight` + 2  where `barRight` >= %s"
	        cursor.execute(sql, (upperbarDetails['barRight']))
	        sql = "UPDATE barInfo set `barLeft` = `barLeft` + 2  where `barLeft` >= %s"
	        cursor.execute(sql, (upperbarDetails['barRight']))

	    with connection.cursor() as cursor:
	        barFullName = upperbarDetails['barFullName'] + "_" + barName
	        sql = "INSERT INTO barInfo (`barName`,`barFullName`,`dateCreated`,`depth`,`barLeft`,`barRight`,talkCount) VALUES (%s,%s,%s,%s,%s,%s,0)"
	        cursor.execute(sql, (barName,barFullName,Utility.getCurrentTime(),upperbarDetails['depth']+1,upperbarDetails['barRight'],upperbarDetails['barRight']+1))

	    with connection.cursor() as cursor:
	        sql = "UPDATE user SET lastBarCreation= Now() WHERE userID=%s"
	        cursor.execute(sql, userID)
	        
	    
	    # connection is not autocommit by default. So you must commit to save
	    # your changes.
	    connection.commit()

    #needs to be fixed
	@staticmethod
	def deleteBar(connection, barID, userID):
	    barDetails = Bar.getBarDetails(connection, barID, "barID")
	    getRecords()
	    Bar.updateTalkCount(connection, barID, userID, -barDetails['talkCount'])
	    childrenBarIDs = Bar.getChildrenBarIDs(connection,barDetails,userID)
	    childrenBarIDs.append(barID) #add its own ID on childrenBarIDs
	    Bar.clearBars(connection,childrenBarIDs,userID)
	    Bar.deleteBars(connection, childrenBarIDs,userID,"!Never run this function alone!")

	    fix = len(childrenBarIDs) *2
	    with connection.cursor() as cursor:
	        sql = "UPDATE barInfo set `barRight` = `barRight` - %s  where `barRight` >= %s"
	        cursor.execute(sql, (fix, barDetails['barRight']))
	        sql = "UPDATE barInfo set `barLeft` = `barLeft` - %s  where `barLeft` >= %s"
	        cursor.execute(sql, (fix, barDetails['barRight']))
	    connection.commit()

    #needs to be fixed
	@staticmethod
	def deleteBars(connection, barIDs,userID,warning):
	    if warning !="!Never run this function alone!":
	        return "Error : Can't run deleteBars... Dangerous!"
	    condition = ""
	    for barID in barIDs:
	        condition += "%s"
	        if barIDs[len(barIDs)-1] != barID:
	            condition += ","

	    with connection.cursor() as cursor:
	        sql = "DELETE FROM `barInfo` where `barID` in (" + condition + ")"
	        cursor.execute(sql, barIDs)
	    connection.commit()

    #needs to be fixed
	@staticmethod
	def updateTalkCount(connection, barID, userID,count):
		with connection.cursor() as cursor:
			sql = "SELECT * FROM barInfo where `barID` = %s"
			cursor.execute(sql, barID)
			result = cursor.fetchone()

			barDepth = result['depth']
			barLeft = result['barLeft']
			barRight = result['barRight']

		updateRecord('barInfo',connection,setVarNames=(),setVarValues=(),conditionVarNames=(),conditionVarValues=(count,barLeft,barRight),customSet="talkCount = talkCount + %s",customCondition="%s >= `barLeft` and `barRight` >= %s")

    #needs to be fixed
	@staticmethod
	def clearBars(connection, barIDs, userID):
	    condition = ""
	    for barID in barIDs:
	        condition += "%s"
	        if barIDs[len(barIDs)-1] != barID:
	            condition += ","

	    with connection.cursor() as cursor:
	        sql = "DELETE FROM `talk` where `barID` in (" + condition + ")"
	        cursor.execute(sql, barIDs)
	    connection.commit()

	### Client-side ###
	@staticmethod
	def getTwoUpperBars(connection, barID, superbar = Setting.superbar):
		if int(barID) == superbar['barID']:
			return Utility.intoJson({'barFullName' : Utility.getPublicBarFullName(superbar['barFullName'],superbar), 'upperbarIDs' : None, 'upperbarNames' : None})
		superbarDetails = Bar.getBarDetails(connection, superbar['barID'], 'barID')
		superbarCondition = "%s<`barLeft` and `barRight` <%s"
		superbarConditionVar = (superbarDetails['barLeft'],superbarDetails['barRight'])
	    
	    #[upperbar2, upperbar1(higher)]
		barDetails = Bar.getBarDetails(connection, barID, 'barID')
		upperbarIDs = []
		upperbarNames = []
		try:
		    parentBarDetails = Bar.getParentBarDetails(connection, barDetails, superbarCondition,superbarConditionVar,  select="*")
		    upperbarIDs.append(parentBarDetails['barID'])
		    upperbarNames.append(parentBarDetails['barName'])
		except Exception as e:
		    print "No UpperBars"
		    print e
		    upperbarIDs = ["NULL", "NULL"]
		    upperbarNames = ["NULL", "NULL"]
		else:
		    try:
		        grandparentBarDetails = Bar.getParentBarDetails(connection, parentBarDetails,superbarCondition,superbarConditionVar, select="*")
		        upperbarIDs.append(grandparentBarDetails['barID'])
		        upperbarNames.append(grandparentBarDetails['barName'])
		    except Exception as e:
		        print "Only one Upperbar"
		        print e
		        upperbarIDs.append("NULL")
		        upperbarNames.append("NULL")
		finally:
			output = Utility.intoJson({'barFullName' : Utility.getPublicBarFullName(barDetails['barFullName'],superbar), 'upperbarIDs' : upperbarIDs, 'upperbarNames' : upperbarNames})
    		return(output)

	@staticmethod
	def checkAndCreateBar(connection, barFullName, userID, location="",userMacAddress="",userIPAddress="", superbar=Superbar.superbar):
		userDetails = User.getUserDetails(connection, userID, varName="userID", select="*")
		#print(Utility.getCurrentTime-userDetails['lastBarCreation'])
		try:
			#superbar exception
			if barFullName[0] == '_':
				barFullName = string.replace(barFullName,'_','')
			barFullName = barFullName.lower()
			barFullName = Utility.getAuthenticBarFullName(barFullName, superbar)
			barName =  Utility.getCurrentBarName(barFullName)
			isvalidName = Bar.isBarNameValid(barName)
		except:
			raise Exception('error occurred during barName conversion')
			return 0
		if(isvalidName['isValid']==1):
			twinBar = Bar.isThereTwinBar(connection, barFullName,superbar=None)
			if twinBar == None:
				parentBarFullName = Utility.getParentBarFullName(barFullName)
				parentBarDetails = Bar.getBarDetails(connection, parentBarFullName, 'barFullName')
				if parentBarDetails != None:
					Bar.createBar(connection,parentBarDetails['barID'], barName, userID,location,userMacAddress,userIPAddress, "neverUsetThisBarAlone")
					barDetails = Bar.getBarDetails(connection, barFullName, 'barFullName')
					message = Setting.greetings(Utility.getPublicBarFullName(barFullName,superbar))
					Talk.createTalk(connection,userID,barDetails['barID'], message,location,userMacAddress,userIPAddress,initialLikeCount=5)
					#Talk.createChildTalk(connection,userID,barID,parentTalkID,talkContent,location,userMacAddress,userIPAddress,imageURL='')
					return Utility.intoJson({'success':1, 'code':'200', 'description': 'success'})
				else:
					print "Parent doesn't exist. Bar creation failed"
					return Utility.intoJson({'success':0, 'code':'401', 'description': 'Parent doesn not exist. Bar creation failed'})
			else:
				print "There already exists the same bar. Bar creation failed"
				return Utility.intoJson({'success':0, 'code':'402', 'description': 'There already exists the same bar. Bar creation failed'})
		else:
			return Utility.intoJson({'success':0, 'code':'403', 'description': 'Unaccepted characters included :'+str(isvalidName['Unaccepted characters'])})

	@staticmethod
	def getSearchResult(connection, barFullName,superbar=Superbar.superbar, depth=1000, deep=0, debugging =0):
		def caseStringGenerator(searchKeyword, barFullName="", field = 'barFullName', weight=10000, editScoreWeight = 1000, tolerance = 0.3):
			keywordArray = searchKeyword.split()
			primeKeyword = keywordArray[len(keywordArray)-1]
			defaultStr = "-1/(char_length("+str(field)+")*"+str(tolerance)+"+1)*"+str(editScoreWeight)


			caseStr = "case "
			if field == 'barName':
				levenshteinScoreStr = "(levenshtein("+field+",'"+primeKeyword+"'))"
				#for keyword in keywordArray:
				#	levenshteinScoreStr += " + levenshtein("+field+",'"+keyword+"') "
				#levenshteinScoreStr += ")"
				caseStr += " when ( " + field + " REGEXP \'^.*" + primeKeyword + ".*$\') then " +str(weight) +"+1/("+levenshteinScoreStr+"+1)*"+str(editScoreWeight)
				caseStr += " else " + defaultStr +"+1/("+levenshteinScoreStr+"+1)*"+str(editScoreWeight)
				caseStr += " end "
			elif field == 'barFullName':
				levenshteinScoreStr = "(levenshtein("+field+",'"+searchKeyword+"'))"
				for i in reversed(range(1, len(keywordArray)+1)):
					combinations = list(itertools.combinations(keywordArray, i))
					for combination in combinations:
						caseStr += " when ("
						caseStr += field +" REGEXP \'^"
						for element in combination:
							caseStr += '.*'
							caseStr += element
							if element != combination[len(combination)-1]:
								pass
							else:
								caseStr += ".*"
								caseStr += '$\') '
						caseStr += " then "+str(i*weight) +"+1/("+levenshteinScoreStr+"+1)*"+str(editScoreWeight)
				caseStr += " else "+ defaultStr +"+1/("+levenshteinScoreStr+"+1)*"+str(editScoreWeight)
				caseStr += " end "
			else:
				print "caseStringGenerator :field Name is neither barName or barFullName"
				raise Exception("caseStringGenerator :field Name is neither barName or barFullName")
			return caseStr

		barFullName = barFullName.lower()
		if barFullName == "" or barFullName =="_":
			select = "barID, talkCount, replace(barFullName, '" + superbar['barFullName'] + "_', '') as barSearchFullName"
			parentBarDetails = Bar.getBarDetails(connection,  superbar['barFullName'], 'barFullName')
			siblingBarDetails = Bar.getChildrenBarDetails(connection, parentBarDetails, additionalCondition = str(parentBarDetails['depth']) + " < `depth`and `depth` <= %s and barID != %s ", additionalConditionVar = (parentBarDetails['depth']+1, superbar['barID']) ,select=select)
			searchResults = siblingBarDetails
			if barFullName =="":
				output = Utility.intoJson({'doesExist' : 1, 'currentBarInfo' : {"barSearchFullName": "...", "barID": superbar['barID'], "talkCount": parentBarDetails['talkCount']}, 'searchResults':searchResults, 'deepSearchResults' : None})
			elif barFullName =="_":
				output = Utility.intoJson({'doesExist' : 1, 'currentBarInfo' : {"barSearchFullName": "underbar", "barID": superbar['barID'], "talkCount": parentBarDetails['talkCount']}, 'searchResults':searchResults, 'deepSearchResults' : None})
			#output = Utility.intoJson({'doesExist' : 0, 'currentBarInfo' : None,  'searchResults' : None})
		else:
			doesExist = 1
			searchResults = None

			barFullName = superbar['barFullName'] + "_" + barFullName 
			select = "barID, talkCount, replace(barFullName, '" + superbar['barFullName'] + "_', '') as barSearchFullName"
			
			#get current bar Info
			if barFullName[len(barFullName)-1] == "_":
				parentBarFullName = Utility.getCurrentBarFullName(barFullName)
				parentBarDetails = Bar.getBarDetails(connection,  parentBarFullName, 'barFullName')
				barDetails = Bar.getBarDetails(connection,  parentBarFullName, 'barFullName', select="barID, talkCount, replace(barFullName, '" + superbar['barFullName'] + "_', '') as barSearchFullName")
			else:
				currentBarFullName = Utility.getCurrentBarFullName(barFullName)
				barDetails = Bar.getBarDetails(connection,  currentBarFullName, 'barFullName', select="barID, talkCount, replace(barFullName, '" + superbar['barFullName'] + "_', '') as barSearchFullName")

				parentBarFullName = Utility.getParentBarFullName(currentBarFullName)
				parentBarDetails = Bar.getBarDetails(connection,  parentBarFullName, 'barFullName')

			if barDetails == None:
				doesExist = 0
				barID = 0
			else:
				doesExist = 1
				barID = barDetails['barID']

			#check whether the parent bar exists
			if parentBarDetails == None:
				print "Error : no parent bar"
				searchResults = None
			else:
				Utility.delcareLevenshtein(connection)
				searchKeyword = Utility.getCurrentBarName(barFullName)
				keywordArray = searchKeyword.split()

				if len(keywordArray) ==1:
					barNameCaseStr = caseStringGenerator(searchKeyword,field = 'barName', weight = 100000,editScoreWeight = 1000,tolerance=0.6)
					barFullNameCaseStr = caseStringGenerator(searchKeyword,field = 'barFullName', weight =100,editScoreWeight = 100,tolerance=0.6)
				else:
					barNameCaseStr = caseStringGenerator(searchKeyword,field = 'barName', weight = 1000,editScoreWeight = 1000,tolerance=0.5)
					barFullNameCaseStr = caseStringGenerator(searchKeyword,field = 'barFullName', weight =100,editScoreWeight = 100,tolerance=0.6)
				
				if int(deep)==1:
					searchScoreStr = barNameCaseStr+"+"+barFullNameCaseStr + "+("+str(parentBarDetails['depth']+1)+ "- depth)*10"
					searchScoreStrWithAs = searchScoreStr + " as searchScore"
					caseStr = searchScoreStr + " DESC"
					selectStr = select + ", " + barNameCaseStr + " as barNameMatchScore" + " , " + barFullNameCaseStr + " as barFullNameMatchScore" +" , "+ searchScoreStrWithAs +" , depth"

					if str(debugging) ==1:
						additionalCondition = ""
					else:
						additionalCondition = searchScoreStr + " > 0 and "
					additionalCondition += str(parentBarDetails['depth']+1) + """ < `depth`and `depth` <= %s and barID != %s
																			 		order by
																			 			"""+caseStr+""",
																			 			levenshtein(barFullName,%s),
																 						talkCount DESC
																 						limit 3
																			 """
				 	additionalConditionVar = (parentBarDetails['depth']+depth, barID, searchKeyword)
					childerenBarDetails = Bar.getChildrenBarDetails(connection, parentBarDetails, additionalCondition = additionalCondition, additionalConditionVar = additionalConditionVar ,select= selectStr)
					deepSearchResults = childerenBarDetails
				else:
					deepSearchResults = None

				if barFullName[len(barFullName)-1] == "_":
					additionalCondition = str(parentBarDetails['depth']) + " < `depth`and `depth` <= %s and barID != %s order by talkCount DESC limit 20"
					additionalConditionVar = (parentBarDetails['depth']+1, barID)
				else:
					additionalCondition = str(parentBarDetails['depth']) + " < `depth`and `depth` <= %s and barID != %s order by levenshtein(barName,%s) ASC, talkCount DESC limit 20"
					additionalConditionVar = (parentBarDetails['depth']+1, barID, Utility.getCurrentBarName(barFullName))
				siblingBarDetails = Bar.getChildrenBarDetails(connection, parentBarDetails, additionalCondition = additionalCondition, additionalConditionVar = additionalConditionVar ,select=select)
				searchResults = siblingBarDetails
				
			output = Utility.intoJson({'doesExist' : doesExist, 'currentBarInfo' : barDetails, 'searchResults':searchResults, 'deepSearchResults' : deepSearchResults})
		return output

