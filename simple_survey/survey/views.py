from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Survey,SurveyAnswer,QuestionAnswer,Question,Choice
import sys

from django.contrib.auth import authenticate, login
# Create your views here.

def index(request):
    ctx = {}
    return render(request, 'main.html', ctx)

def survey_view(request, survey_id = None):
    try:
        survey = Survey.objects.get(id=survey_id)
        questions = survey.question_set.all()
        ctx = {'survey': survey, 'questions': questions}
    except:
        return render(request, 'surveynotfound-error.html', {'sv_id': survey_id})
    return render(request, 'survey-take.html', ctx )

def load_survey(request):
    sv_load = request.POST.get('survey_view',False)
    return redirect('survey-detail', survey_id=sv_load)

def admin_login(request):
    admin_usname = request.POST['username']
    admin_password = request.POST['password']
    user = authenticate(username=admin_usname, password=admin_password)
    if user is not None:
        login(request, user)
        return redirect('admin-panel')
    return render(request, 'main.html', {'login':False})

def admin_panel(request):
    surveys = Survey.objects.all()
    ctx = {'surveys': surveys}
    return render(request, 'admin-panel.html', ctx)

def admin_answers(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    answers = survey.surveyanswer_set.all()
    ctx = {'answers': answers, 'survey': survey}
    return render(request, 'admin-survey-detail.html', ctx)

def survey_fill(request):
    ans = SurveyAnswer()
    orig_survey = Survey.objects.get(id=request.POST.get('survey_id',False))
    ans.orig_survey = orig_survey
    ans.save()
    questions = orig_survey.question_set.all()
    for question in questions:
        qc  = request.POST['question'+str(question.id)]
        qa = QuestionAnswer()
        qa.answer = Choice.objects.get(id=int(qc))
        qa.survey_answer = ans
        qa.save()
    ans.save()
    return render(request, 'survey-complete.html', {})

def survey_create_view(request):
    return render(request, 'survey-create.html', {})

def survey_create(request):
    newSurvey = Survey()
    newSurvey.title = request.POST['survey_title']
    newSurvey.save()
    request.session['current_survey'] = newSurvey.id
    return redirect('admin-question-add-view')
    

    
   

def question_add_view(request):
    return render(request, 'question-add.html', {})

def question_add(request):
   
    survey_add = Survey.objects.get(id= int(request.session['current_survey']))
    new_question = Question()
    request.session['current_question'] = new_question.id
    new_question.question_text = request.POST['question_text']
    new_question.survey = survey_add
    new_question.save()
    survey_add.question_set.add(new_question)
    survey_add.save()
    request.session['current_question'] = new_question.id
    return redirect('admin-choice-add-view')

def choice_add_view(request):
    question = Question.objects.get(id= int(request.session['current_question']))
    return render(request, 'choice-add.html', {'question': question})

def choice_add(request):
   
    question = Question.objects.get(id= int(request.session['current_question']))
    newChoice = Choice()
    newChoice.choice_text = request.POST["choice_text"]
    newChoice.question = question
    newChoice.save()
    question.choice_set.add(newChoice)
    
    question.save()
    return redirect('admin-choice-add-view')

def survey_delete(request):
    survey = request.POST['sv_delete']
    sv_del = Survey.objects.get(id=int(survey))
    sv_del.delete()
    return redirect('admin-panel')



