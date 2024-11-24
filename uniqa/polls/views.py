from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, PollOption
from .forms import PollForm

def poll_list(request):
    polls = Poll.objects.all()
    return render(request, 'polls/poll_list.html', {'polls': polls})

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'polls/poll_detail.html', {'poll': poll})

def poll_create(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            return redirect('polls:poll_list')
    else:
        form = PollForm()
    return render(request, 'polls/poll_form.html', {'form': form})

