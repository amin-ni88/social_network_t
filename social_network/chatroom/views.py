from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import PrivateChat, GroupChat, Message
from .forms import MessageForm

@login_required
def chatroom_home(request):
    return render(request, 'chatroom/chatroom_home.html')

@login_required
def create_private_page(request):
    if request.method == 'POST':
        selected_user_id = request.POST['user']
        selected_user = User.objects.get(id=selected_user_id)
        private_chat = PrivateChat.objects.create(admin=request.user, user=selected_user)
        return redirect('private_chat', chat_id=private_chat.id)
    users = User.objects.exclude(id=request.user.id)
    private_chats = PrivateChat.objects.filter(admin=request.user) | PrivateChat.objects.filter(user=request.user)
    return render(request, 'chatroom/private_chats.html', {'users': users, 'private_chats': private_chats})

@login_required
def delete_private_chat(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id)
    if request.user == chat.admin or request.user == chat.user:
        chat.delete()
    return redirect('create_private_page')



@login_required
def create_group_page(request):
    if request.method == 'POST':
        group_name = request.POST['name']
        selected_users_ids = request.POST.getlist('users')
        group_chat = GroupChat.objects.create(name=group_name, admin=request.user)
        group_chat.members.add(request.user)
        for user_id in selected_users_ids:
            user = User.objects.get(id=user_id)
            group_chat.members.add(user)
        return redirect('group_chat', chat_id=group_chat.id)
    users = User.objects.exclude(id=request.user.id)
    group_chats = GroupChat.objects.filter(admin=request.user).distinct()
    return render(request, 'chatroom/group_chats.html', {'users': users, 'group_chats': group_chats})




@login_required
def delete_group_chat(request, chat_id):
    chat = get_object_or_404(GroupChat, id=chat_id)
    if request.user == chat.admin:
        chat.delete()
    return redirect('create_group_page')

@login_required
def leave_group_chat(request, chat_id):
    chat = get_object_or_404(GroupChat, id=chat_id)
    if request.user in chat.members.all():
        chat.members.remove(request.user)
    return redirect('create_group_page')

@login_required
def private_chat(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id)
    if request.user != chat.admin and request.user != chat.user:
        return redirect('chatroom_home')
    messages = Message.objects.filter(chat_type='private', chat_id=chat_id).order_by('-timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_type = 'private'
            message.chat_id = chat_id
            message.sender = request.user
            message.save()
            return redirect('private_chat', chat_id=chat_id)
    else:
        form = MessageForm()
    users = User.objects.exclude(id__in=[request.user.id, chat.admin.id, chat.user.id])
    return render(request, 'chatroom/private_chat.html', {'chat': chat, 'messages': messages, 'form': form, 'users': users})



@login_required
def group_chat(request, chat_id):
    chat = get_object_or_404(GroupChat, id=chat_id)
    if request.user not in chat.members.all():
        return redirect('chatroom_home')  # Redirect if the user is not part of the chat
    
    messages = Message.objects.filter(chat_type='group', chat_id=chat_id).order_by('-timestamp')
    form = MessageForm(request.POST or None)
    
    if request.method == 'POST':
        if 'content' in request.POST:
            if form.is_valid():
                message = form.save(commit=False)
                message.chat_type = 'group'
                message.chat_id = chat_id
                message.sender = request.user
                message.save()
                return redirect('group_chat', chat_id=chat_id)
        elif 'selected_users[]' in request.POST:
            selected_users = request.POST.getlist('selected_users[]')
            for user_id in selected_users:
                user = User.objects.get(id=user_id)
                chat.members.add(user)
            return JsonResponse({'status': 'success'})
        elif 'remove_user' in request.POST:
            remove_user_id = request.POST['remove_user']
            if request.user == chat.admin:
                user = User.objects.get(id=remove_user_id)
                chat.members.remove(user)
            return JsonResponse({'status': 'success'})
    
    users = User.objects.exclude(id__in=list(chat.members.values_list('id', flat=True)))
    return render(request, 'chatroom/group_chat.html', {'chat': chat, 'messages': messages, 'form': form, 'users': users})

