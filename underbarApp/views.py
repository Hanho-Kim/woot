#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import json



def index(request):
	return render(request, 'underbarApp/index.html')

def update(request):
	# 업데이트 체크. 클라이언트의 앱의 버전을 받아서 최신버전과 비교후 업데이트 해야할 필요가 있는지 판단함
	# request.GET.get("currentVersion") --> 클라이언트의 앱 버전
	if(request.GET.get("currentVersion") < "1.0.0"): # 최신버전과 비교
		return render(request, 'underbarApp/update.html')
	else:
		return HttpResponse("")

def debug(request):
	return render(request, 'underbarApp/debug.html')

def login(request):
	if(request.path == "/login"):
		return render(request, 'underbarApp/login/login.html')
	else:
		return render(request, 'underbarApp/login/' + request.path.split("/")[2] + '.html')

def message(request):
	if(request.path == "/message"):
		return render(request, 'underbarApp/message/discover.html')
	else:
		return render(request, 'underbarApp/message/' + request.path.split("/")[2] + '.html')

def write(request):
	return render(request, 'underbarApp/write/' + request.path.split("/")[2] + '.html')

def notification(request):
	return render(request, 'underbarApp/notification/' + request.path.split("/")[2] + '.html')

def gathering(request):
	return render(request, 'underbarApp/gathering/' + request.path.split("/")[2] + '.html')

def people(request):
	return render(request, 'underbarApp/people/' + request.path.split("/")[2] + '.html')

def pullup(request):
	return render(request, 'underbarApp/pullup/' + request.path.split("/")[2] + '.html')

def footerInput(request):
	return render(request, 'underbarApp/footer-input/' + request.path.split("/")[2] + '.html')

def board(request):
	return render(request, 'underbarApp/board/' + request.path.split("/")[2] + '.html')

def apiv1(request):
	pathSplit = request.path.split("/")
	if(pathSplit[3] == "get"):
		if(pathSplit[4] == "signupEmailCheck"): 
			# 가입 가능한 이메일인지 체크하는거
			if(request.GET.get('email') == "kim.hh91@gmail.com"):
				return HttpResponse(0)
			else:
				return HttpResponse(1)
		elif(pathSplit[4] == "signupBlockCheck"): 
			# 블록 유무 확인
			# request.GET.get('address')로 주소 전송함. 판단해서 블록 유무 및 정보 알려줌
			if(1 == 0):
				return HttpResponse(0)
			else:
				return HttpResponse('{"bid":1,"bname":"법조타운B"}')
		elif(pathSplit[4] == "highlight"):
			# 푸터나 헤더 메뉴중 하이라이트 표시할 것 (새소식 등)
			# Footer의 경우 ["home","gathering","write","board","people"] 형태로 return
			# Header의 경우 알림 개수 리턴. 없으면 0
			return HttpResponse('{"footer":["board","people"],"header":1}')
		elif(pathSplit[4] == "highlightHeaderDelete"):
			# Header Highlight 지우기
			# 유저가 알림창을 봤음
			return HttpResponse(1)
		elif(pathSplit[4] == "avatarChange"):
			# 프로필 수정 페이지에서 아바타 체인지시 쓰이는거
			# 랜덤하게 아바타 정보 보내주기
			return HttpResponse('{"image":"http://hellowoot.co.kr/static/asset/images/profile_images/12-1.png","avatarID":"12"}')
		
		elif(pathSplit[4] == "chatInfo"):
			# 채팅 정보를 전달해줌
			# 해당 채팅방에 대한 정보 + 현재 세션 유저 정보 + 현재 세션 유저가 들어갈수 없는 채팅이라면 그 여부 + 채팅방 닫혔는지 여부

			gatheringExampleChatInfo = {
					"room" 		: {
							"type"			: "gathering",
							"id"			: "5",
							"title"			: "가볍게 맥주한잔",
							"sticker"		: "http://ec2-18-224-96-147.us-east-2.compute.amazonaws.com:8000/site_media/static/sticker1.jpg",
							"date"			: "10월 16일 오후 06:00",
							"place"			: "파크하비오앞",
							"description"	: "출출해 질 오후, 석촌 오모가리 김치찌개를 먹고 한강으로 이동, 해 질녁부터 한강에서 맥주 마시면서 보드게임해요! 늦잠 푹~ 주무시구 오후에 느즈막이 만화방가서 서로 수다떨고 만화책읽어요! <br><br>(그냥 읽고 싶은 책 가지고 오셔두 됩니다) 3시쯤 시작해서 떠들고 머리쓰다 보면 금방 배가 고파질테니 저녁 식사 같이하러 가요~ 메뉴는 오시는 분들과 함께 정해봐요 :) <br><br>처음 오시는 분들 걱정하지 마시구 어서오세요~ 30분만 같이 있으면 그 걱정 한번에 날려드릴게요ㅎㅎ",
							"participants"	: {
									"username" 	: [],
									"uid"		: [],
									"avatar"	: []
							},
							"disable"		: "true"
						},
					"user" 		: {
							"uid"			: 3,
							"username"		: "칙칙",
							"avatarUrl"		: "http://hellowoot.co.kr/static/asset/images/profile_images/3-1.png",
							"avatarColor"	: "#26de81"
						},
					"firebase"	: {
							"instancePath"	: "/messages/gathering/5/",
							"authEmail"		: "kimhh91@gmail.com",
							"authKey"		: "debf48f5898c176db7ca9bdf1ec13303"
						}
				}

			directExampleChatInfo = {
					"room" 		: {
							"type"			: "direct",
							"id"			: "8",
							"title"			: "쩡이",
							"participants"	: {
									"username" 	: ["멍구","쩡이"],
									"uid"		: ["1","13"],
									"avatar"	: ["http://hellowoot.co.kr/static/asset/images/profile_images/7-1.png","http://hellowoot.co.kr/static/asset/images/profile_images/3-1.png"]
							},
							"disable"		: "false"
						},
					"user" 		: {
							"uid"			: 1,
							"username"		: "멍구",
							"avatarUrl"		: "http://hellowoot.co.kr/static/asset/images/profile_images/3-1.png",
							"avatarColor"	: "#26de81"
						},
					"firebase"	: {
							"instancePath"	: "/messages/direct/1/",
							"authEmail"		: "kimhh91@gmail.com",
							"authKey"		: "debf48f5898c176db7ca9bdf1ec13303"
						}
				}

			if(request.GET.get('cid') == '1'):
				return HttpResponse(json.dumps(gatheringExampleChatInfo))
			else:
				return HttpResponse(json.dumps(directExampleChatInfo))

	if(pathSplit[3] == "post"):
		if(pathSplit[4] == "like"):
			# 라이크 누르기 (postid를 pid로 받음)
			# request.POST.get("pid")
			return HttpResponse(1)

		elif(pathSplit[4] == "comment"):
			# 댓글 달기 (수정 & 신규)
			# "cid" : 댓글 id --> 값을 클라이언트가 보내주면 수정 / 안보내주면 신규
			# "text" : 텍스트
			return HttpResponse(1)

		elif(pathSplit[4] == "recomment"):
			# 대댓글 달기
			# "parentCid" : 부모댓글 id
			# "text" : 텍스트
			return HttpResponse(1)

		elif(pathSplit[4] == "gathering"):
			# 게더링만들기 (아래 내용 data로 받음)
        	# sticker     
        	# title       
        	# description 
        	# location    
        	# time        
        	# maxpeople   
        	# agelimit    
        	# instant     
        	# mintime     
        	# minpeople
			return HttpResponse(1)

		elif(pathSplit[4] == "posting"):
			# 포스팅만들기 (아래 내용 data로 받음)
            # board
            # description
            # file-1
            # file-2
            # file-3
            # location
            # 반드시 리턴으로 만들어진 posting의 pid 보내줘야함
			return HttpResponse(1)

		elif(pathSplit[4] == "profile"):
			# 프로필 정보 수정
			# avatar
            # description
            # interest
            # push
			return HttpResponse('{"redirect":"/index"}')

		elif(pathSplit[4] == "password"):
			# 비밀번호 변경 (아래 내용 form으로 전달받음)
            # currentPW
            # newPW
            # newConfirmPW
            # Validate 한후 Redirect 
			return HttpResponse('{"redirect":"/index"}')

		elif(pathSplit[4] == "user"):

			if(pathSplit[5] == "woot"):
				# 특정 유저한테 우트 주기 
				# request.POST.get("uid")
				return HttpResponse(1)

			elif(pathSplit[5] == "block"):
				# 특정 유저 차단하기 
				# request.POST.get("uid")
				return HttpResponse(1)

			elif(pathSplit[5] == "unblock"):
				# 특정 유저 차단 해제하기
				# request.POST.get("uid")
				return HttpResponse(1)

			elif(pathSplit[5] == "report"):
				# 특정 유저 차단하고 신고하기
				# request.POST.get("uid")
				return HttpResponse(1)

		elif(pathSplit[4] == "signup"):

			if(pathSplit[5] == "user"):
				# 유저 정보를 받아 회원가입
				# request.POST.get("address")
				# request.POST.get("email")
				# request.POST.get("password")
				# request.POST.get("nickname")
				# request.POST.get("intro")
				# request.POST.get("interests") --> Array로 전달
				# request.POST.get("phone")
				return HttpResponse(1)

			elif(pathSplit[5] == "address"):
				# 유저 주소지 인증. 이미지 파일 전송
				# request.POST.get("addressConfirmImage")
				return HttpResponse(1)

		elif(pathSplit[4] == "gatheringParticipate"):
			# 게더링 참가
			return HttpResponse(1)

	if(pathSplit[3] == "delete"):
		if(pathSplit[4] == "like"):
			# 포스팅 라이크 취소 (posting id를 pid로 받음)
			# request.DELETE.get("pid")
			return HttpResponse(1)

		elif(pathSplit[4] == "comment"):
			# 코멘트 삭제 (comment id를 cid로 받음)
			# request.DELETE.get("cid")
			return HttpResponse(1)

		elif(pathSplit[4] == "posting"):
			# 포스팅 삭제 (posting id를 pid로 받음)
			# request.DELETE.get("pid")
			return HttpResponse(1)

		elif(pathSplit[4] == "user"):

			if(pathSplit[5] == "woot"):
				# 특정 유저한테 우트 취소하기
				# request.POST.get("uid")
				return HttpResponse(1)


