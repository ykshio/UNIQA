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
