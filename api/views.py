from django.shortcuts import render
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.http import JsonResponse
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, throttle_classes,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import LeaderboardSerializer,AnswerSerializer,SocialSerializer,QuestionSerializer
from quiz.models import UserScore,config,Question
from requests.exceptions import HTTPError
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
import time
import datetime
# Create your views here.
import requests as r
import pytz
from pytz import timezone
utc= pytz.utc



@api_view(['GET'])
def leaderboard(request):
    players=UserScore.leaderboard(UserScore)
    serializer=LeaderboardSerializer(players,many=True)
    return Response(serializer.data)
class getquestion(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self,request):
        player=UserScore.objects.filter(user=request.user)[0]
        active=config.quiz_active(config)
        # initializing current active config:
        configs= config.objects.all()
    


        # arr = [[config]*(no of instances of each day)]* no of days
        arr=[]
        arr = [0 for i in range(10)]      #initialized 10 days with 0 instances of each
        cnt = 1
        for con in configs:
            curr_day = con.current_day
            arr[curr_day] += 1
            cnt = max(curr_day, cnt)
        list_of_configs = []
        new = []
        for i in range(1,cnt+1):
            for j in configs:
                curr_day = j.current_day
                if curr_day == i:
                    new.append(j)
            list_of_configs.append(new)
            new = []

        maxi = datetime.datetime.now().replace(tzinfo=utc)
        choice = None
        default_choice = configs[0]
        for i in list_of_configs:
         
            maxi = datetime.datetime.now().replace(tzinfo=utc)
            for j in i:
                default_choice = j
                quiz_endtime = j.quiz_endtime.replace(tzinfo=utc)
   
                if maxi < quiz_endtime:
                    choice = j
  
                    maxi = quiz_endtime
            if choice is not None:
                break
        if choice is None:
            choice = default_choice
        curr_config=choice
        #end
        if active:
            day= curr_config.current_day
            curr_day=player.today
            curr_question=player.current_question
            if curr_day > curr_config.current_day:
                response={
                  "quiz_finished": True
                }
                return Response(response)
            if curr_day<day:
                player.today = day
                player.current_question = 1
                curr_day =player.today
                curr_question=player.current_question
                player.save()
            question=Question.objects.filter(day=day,question_no=curr_question)[0]
            serializer=QuestionSerializer(question)
            return Response(serializer.data)
        else:
            response= {
                "error":"quiz has ended"
            }
            return Response(response)


@api_view(['GET'])
def configstatus(request):
    configs=config.objects.all()
    


    # arr = [[config]*(no of instances of each day)]* no of days
    arr=[]
    arr = [0 for i in range(10)]      #initialized 10 days with 0 instances of each
    cnt = 1
    for con in configs:
        curr_day = con.current_day
        arr[curr_day] += 1
        cnt = max(curr_day, cnt)
    list_of_configs = []
    new = []
    for i in range(1,cnt+1):
        for j in configs:
            curr_day = j.current_day
            if curr_day == i:
                new.append(j)
        list_of_configs.append(new)
        new = []
    
    maxi = datetime.datetime.now().replace(tzinfo=utc)
    choice = None
    default_choice = configs[0]
    for i in list_of_configs:

        maxi = datetime.datetime.now().replace(tzinfo=utc)
        for j in i:
            default_choice = j
            quiz_endtime = j.quiz_endtime.replace(tzinfo=utc)

            if maxi < quiz_endtime:
                choice = j
  
                maxi = quiz_endtime
        if choice is not None:
            break
    if choice is None:
        choice = default_choice
    if choice:
       response={
       "current_day":choice.current_day,
       "start_time":choice.quiz_start.replace(tzinfo=utc),
       "end_time":choice.quiz_endtime.replace(tzinfo=utc)  
       }
       return Response(response)
    response={
        "status":404,
        "message":"no configs found"
    }
    return Response(response)
class Answer(APIView):
    permission_classes=(IsAuthenticated,)
    
    def post(self,request):
        player=UserScore.objects.filter(user=request.user)[0]
        print(player.name)
        answer=request.data.get("answer",None)
        print(player)
        active=config.quiz_active(config)
        # initializing current active config:
        configs= config.objects.all()
    


        # arr = [[config]*(no of instances of each day)]* no of days
        arr=[]
        arr = [0 for i in range(10)]      #initialized 10 days with 0 instances of each
        cnt = 1
        for con in configs:
            curr_day = con.current_day
            arr[curr_day] += 1
            cnt = max(curr_day, cnt)
        list_of_configs = []
        new = []
        for i in range(1,cnt+1):
            for j in configs:
                curr_day = j.current_day
                if curr_day == i:
                    new.append(j)
            list_of_configs.append(new)
            new = []
        
        maxi = datetime.datetime.now().replace(tzinfo=utc)
        choice = None
        default_choice = configs[0]
        for i in list_of_configs:

            maxi = datetime.datetime.now().replace(tzinfo=utc)
            for j in i:
                default_choice = j
                quiz_endtime = j.quiz_endtime.replace(tzinfo=utc)
            
                if maxi < quiz_endtime:
                    choice = j
    
                    maxi = quiz_endtime
            if choice is not None:
                break
        if choice is None:
            choice = default_choice
        curr_config=choice
        #end
        
        if active:
            day=curr_config.current_day
            curr_day =player.today
            curr_question=player.current_question
            if curr_day>day:
                response={
                  "quiz_finished": True
                }
                return Response(response)
            if curr_day<day:
                player.today = day
                player.current_question= 1
                curr_day =player.today
                curr_question=player.current_question
                player.save()
            question=Question.objects.filter(day=day,question_no=curr_question)
            result=Question.check_ans(Question,answer,question)
            quiz_ended=False
            if result:
               player.new_score(player)
               curr_day =player.today 
               if curr_day > curr_config.current_day:
                   quiz_ended=True
            response={
                    'status_code':status.HTTP_200_OK,
                    'result':result,
                    'quiz_finished':quiz_ended
                }
        else:
           response= {
                "error":"quiz has ended"
            }
        return Response(response)
class GoogleLogin(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.username = data['email']
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()
            score = UserScore(user=user,name=data['name'], email = user.email, current_question = 1)
            score.save()

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)


class facebooklogin(APIView):
    
    def post(self,request):
        print(request.data)
        accesstoken=request.data.get('accesstoken')
        expiration_time=request.data.get('expiration_time')
        print(expiration_time)
        userID=request.data.get('userID')
        if(int(expiration_time) < int(time.time())):
            content= {"status": 404}
            return Response(content)
        else:
            url = "https://graph.facebook.com/{}".format(userID)
            parameters = {
                'fields': 'name,email,picture',
                'access_token': accesstoken
            }
            idInfo = r.get(url=url, params=parameters).json()

            email= idInfo['email']
            
            #these are tuple objects with one element. Placing the elements seperately. Else brackets and commas will be included
            name= idInfo['name']
            email = email[0]
            name = name[0]

            image= idInfo['picture']['data']['url'],
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User()
                user.username = email
                user.email = email
                # provider random default password
                user.password = make_password(BaseUserManager().make_random_password())
                user.save()
                score = UserScore(user=user,name=name, email = user.email, current_question = 1)
                score.save()

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)
        
