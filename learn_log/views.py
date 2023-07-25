from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    """ The home page for learn_log"""
    return render(request, 'learn_log/index.html')


@login_required
def topics(request):
    """ Show all topics """
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learn_log/topics.html', context)


def topic(request, topic_id):
    """ Show a single topic and all it's entries. """
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learn_log/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form. 
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learn_log:topics')
        
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learn_log/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    # Add a new entry for a particular topic/
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data submitted, create a blank form.
        form = EntryForm()
    else:
        # POST data submitted, process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learn_log: topic_id=topic_id')
        
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learn_log/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learn_log:topic', topic_id=topic.id)
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learn_log/edit_entry.html', context)