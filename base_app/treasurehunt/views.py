from django.shortcuts import render
from . import forms
# Create your views here.
from treasurehunt import models
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages

# def index(request):
#     return render(request, 'treasurehunt/index.html')

# def register(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('treasurehunt:question'))
#     registered = False

#     if request.method == 'POST':
#         user_form = forms.UserForm(data=request.POST)
#         if user_form.is_valid():
#             passmain = user_form.cleaned_data['password']
#             passverify = user_form.cleaned_data['confirm_password']
#             if passmain == passverify:
#                 user = user_form.save()
#                 user.set_password(user.password)
#                 user.save()

#                 score = models.Score()
#                 score.user = user
#                 score.save()

#                 registered = True
#             else:
#                 return HttpResponse("Password Don't Match")
#         else:
#             print(user_form.errors)
#     else:
#         user_form = forms.UserForm()

#     return render(request, 'treasurehunt/signup.html', {
#         'user_form': user_form,
#         'registered': registered
#     })


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('treasurehunt:question'))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('treasurehunt:question'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            messages.warning(request, 'Wrong id or password')
            return render(request, 'treasurehunt/index.html', {'flag': 1})
    else:
        return render(request, 'treasurehunt/index.html', {'flag': 1})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('treasurehunt:index'))


@login_required
def question(request):

    question_fixed = [
        'iunmoid6gb', 'tRX8qaRmJp', 'QjQHE68KYF', 'FbjZg8JEcc', 'f1X3YrD8W9',
        'Q6(the man who would live)', 'xZzrr11AyL', 'ciNt7FbDz4', 'jeZHXr6dYa',
        '4LcGlbjua3', 'wZt5JLT3fp', 'dQ8quLottX', '5fmY44Iwri', 'jkVK9ZngIi',
        'NgwDd9Ebbv', 'HFMlJGqcpX', 'yL8uNNcazx', 'CyZs3wjB0x', 'jpKdnk4whi',
        'zZwAwMSAjU'
    ]

    current_user = request.user
    sc = models.Score.objects.get(user__exact=current_user)
    if sc.score == 20:
        return render(request, 'treasurehunt/end.html')
    else:
        if request.method == 'POST' and sc.score != 20:
            ans_fixed = models.AnswerChecker.objects.get(index__exact=sc.score)
            question_form = forms.Answer(data=request.POST)
            if question_form.is_valid():
                ans = question_form.cleaned_data['answer']
                if ans.lower() == ans_fixed.ans_value():
                    sc.score = sc.score + 1
                    # sc.last_answer = datetime.now()
                    sc.save()
                else:
                    return render(
                        request, 'treasurehunt/question.html', {
                            'flag': 0,
                            'question_form': question_form,
                            'score': sc.score,
                            'question_fixed': question_fixed[sc.score],
                        })
            else:
                return render(
                    request, 'treasurehunt/question.html', {
                        'flag': 0,
                        'question_form': question_form,
                        'score': sc.score,
                        'question_fixed': question_fixed[sc.score],
                    })
        elif sc.score == 20:
            return render(request, 'treasurehunt/end.html')
        else:
            question_form = forms.Answer()
        return render(
            request, 'treasurehunt/question.html', {
                'flag': 0,
                'question_form': question_form,
                'score': sc.score,
                'question_fixed': question_fixed[sc.score],
            })


def leaderboard(request):
    leader = models.Score.objects.all().order_by('-score', 'last_answer')
    if len(leader) >= 30:
        user_name = []
        for x in leader[:30]:
            user_name.append((x.user.email, x.score, x.last_answer))
        return render(request, 'treasurehunt/leaderboard.html', {
            'flag': 0,
            'user_name': user_name,
        })
    else:
        user_name = []
        for x in leader:
            user_name.append((x.user.email, x.score, x.last_answer))
        return render(request, 'treasurehunt/leaderboard.html', {
            'user_name': user_name,
        })


#t = Score.objects.all().order_by('-score')
# t[0].user.username