from django.shortcuts import get_object_or_404, redirect
from questions.models import Question
from polls.models import Poll

def like_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.likes.add(request.user)  # Assuming a ManyToMany field for likes
    return redirect('questions:question_detail', question_id=question.id)

def like_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    poll.likes.add(request.user)  # Assuming a ManyToMany field for likes
    return redirect('polls:poll_detail', poll_id=poll.id)

def like_add_view(request, content_id):
    # content_idに基づいて質問か投票かを判断
    question = get_object_or_404(Question, id=content_id)
    question.likes.add(request.user)  # ユーザーをいいねリストに追加
    return redirect('questions:question_detail', question_id=content_id)

def like_remove_view(request, content_id):
    # content_idに基づいて質問か投票かを判断
    question = get_object_or_404(Question, id=content_id)
    question.likes.remove(request.user)  # ユーザーをいいねリストから削除
    return redirect('questions:question_detail', question_id=content_id)

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Answer, Like

@login_required
def like_answer(request, answer_id):
    # 回答を取得
    answer = get_object_or_404(Answer, id=answer_id)

    # 既存の「いいね」が存在するか確認
    existing_like = Like.objects.filter(user=request.user, answer=answer).first()

    if existing_like:
        # すでに「いいね」している場合、解除
        existing_like.delete()
    else:
        # 新しい「いいね」を作成
        Like.objects.create(user=request.user, answer=answer)

    # 回答が属する質問の詳細ページにリダイレクト
    return redirect('questions:question_detail', question_id=answer.question.id)
