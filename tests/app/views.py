from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import ListView, DetailView, CreateView
from django.views import View



class Index(View):
    def get(self, request):

        # ПЕРЕДЕЛАТЬ В МИКСИН!
        username = None
        if User.objects.filter(username=request.user.username):
            user = User.objects.get(username=request.user.username)
            username = user.username

        return render(request, 'app/index.html', {'username': username})
class Signup(View):
    def get(self, request):
        return render(request=request, template_name='app/signup.html')

    def post(self, request):
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Логин занят :(')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=pass1)
                user.save()
                user_login = auth.authenticate(username=username, password=pass1)
                auth.login(request, user_login)

                return redirect('success_signin')
        else:
            messages.info(request, 'Пароли не совпадают :(')
            return redirect('signup')

class Success_signin(LoginRequiredMixin, View):
    login_url = 'signin'
    def get(self, request):
        username = User.objects.get(username=request.user.username)
        return render(request, 'app/success_signin.html', {'username' : username,})

class Signin(View):
    def get(self, request):
        return render(request=request, template_name='app/signin.html')

    def post(self, request):
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = auth.authenticate(username=username, password=pass1)

        if user is not None:
            auth.login(request, user)
            return redirect('success_signin')
        else:
            messages.info(request, 'Логин/пароль не корректны :(')
            return redirect('signin')

class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('signin')

class Setsview(LoginRequiredMixin, View):
    login_url = 'signin'
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        username = user.username

        sets = Sets.objects.all()
        return render(request, 'app/sets.html', {'sets': sets, 'username':username})

class Setview(LoginRequiredMixin, View):
    login_url = 'signin'
    def get(self, request, id):
        user = User.objects.get(username=request.user.username)
        username = user.username

        current_set = Sets.objects.get(id=id)
        questions = Questions.objects.filter(sets=current_set)

        #Создаем список вопросов по НАБОРУ, которые USER - проходил
        user_result = Result.objects.filter(user=user, question__sets=current_set, checked=True)
        answered_questions = [question.question.id for question in user_result]

        new_question_for_user=[]
        #Составляем список вопросов, которые USER - не проходил!
        for question in questions:
            if question.id not in answered_questions:
                new_question_for_user.append(question)

        if len(new_question_for_user)!=0:
            question_for_user=new_question_for_user[0]
        else:
            question_for_user=None
        print(question_for_user)
        return render(request, 'app/set.html', {'set':set, 'questions':questions, 'username':username, 'question_for_user':question_for_user })