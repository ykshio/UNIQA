from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

@login_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': questions})

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    
    # POSTされた場合の処理
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.created_by = request.user
            answer.save()
            return redirect('questions:question_detail', pk=question.pk)
    else:
        form = AnswerForm()

    return render(request, 'questions/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })

@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()
            return redirect('questions:question_list')
    else:
        form = QuestionForm()
    return render(request, 'questions/question_form.html', {'form': form})

@login_required
def question_form(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user
            question.save()
            return redirect('questions:question_list')
    else:
        form = QuestionForm()
    return render(request, 'questions/question_form.html', {'form': form})

@login_required
def toggle_resolved(request, question_id):
    question = get_object_or_404(Question, id=question_id, created_by=request.user)
    question.is_resolved = not question.is_resolved
    question.save()
    return redirect('questions:question_detail', question_id=question.id)

@login_required
def answer_create(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.created_by = request.user
            answer.save()
            return redirect('questions:question_detail', question_id=question.id)
    else:
        form = AnswerForm()
    return render(request, 'questions/answer_form.html', {'form': form, 'question': question})

