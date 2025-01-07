from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, Category
from .forms import QuestionForm, AnswerForm
from django.db.models import Count
from django.db.models import Q

@login_required
def question_list(request):
    # 並び順パラメータ取得
    order = request.GET.get('order', 'new')  # デフォルトは新しい順
    category_id = request.GET.get('category', None)  # カテゴリID取得
    status = request.GET.get('status', None)  # 解決ステータス取得
    query = request.GET.get('query', '')

    # 初期クエリセット（クエリに基づいて質問をフィルタ）
    questions = Question.objects.all()

    # クエリがあればタイトルと内容を検索
    if query:
        questions = questions.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # 並び順適用
    if order == 'new':
        questions = questions.order_by('-created_at')  # 新しい順
    else:
        questions = questions.order_by('created_at')  # 古い順

    # カテゴリフィルタ適用
    if category_id:
        questions = questions.filter(category_id=category_id)

    # 解決ステータスフィルタ適用
    if status == 'resolved':
        questions = questions.filter(is_resolved=True)
    elif status == 'unresolved':
        questions = questions.filter(is_resolved=False)

    # 全カテゴリを取得（フィルタ用）
    categories = Category.objects.all()

    context = {
        'questions': questions,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'selected_status': status,
        'current_order': order,
        'query': query,
    }
    return render(request, 'questions/question_list.html', context)


@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    sort = request.GET.get('sort', 'new')  # 並び替えパラメータ取得。デフォルトは新しい順。

    # 並び替えロジック
    if sort == 'old':
        answers = Answer.objects.filter(question=question).order_by('created_at')  # 古い順
    elif sort == 'likes':
        answers = Answer.objects.filter(question=question).annotate(like_count=Count('likes')).order_by('-like_count')  # いいねが多い順
    else:
        answers = Answer.objects.filter(question=question).order_by('-created_at')  # 新しい順
    
    # POSTされた場合の処理
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
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
        form = QuestionForm(request.POST, request.FILES)
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
            return redirect('questions:question_detail', pk=answer.question.id)
    else:
        form = AnswerForm()
    return render(request, 'questions/answer_form.html', {'form': form, 'question': question})

@login_required
def toggle_resolution(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.created_by == request.user:
        question.is_resolved = not question.is_resolved
        question.save()
    return redirect('questions:question_detail', pk=question.id)


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.created_by == request.user:
        question.delete()
    return redirect('questions:question_list')

@login_required
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if answer.created_by == request.user:
        answer.delete()
    return redirect('questions:question_detail', pk=answer.question.id)

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from likes.models import Like
from .models import Answer

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    existing_like = Like.objects.filter(user=request.user, answer=answer).first()

    if existing_like:
        existing_like.delete()
    else:
        Like.objects.create(user=request.user, answer=answer)

    return redirect('questions:question_detail', pk=answer.question.id)
