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
    group_chats = GroupChat.objects.filter(members=request.user).distinct()
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
def remove_user_from_group(request, chat_id):
    chat = get_object_or_404(GroupChat, id=chat_id)
    if request.user != chat.admin:
        return redirect('group_chat', chat_id=chat_id)
    
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user = get_object_or_404(User, id=user_id)
        chat.members.remove(user)
        return redirect('group_chat', chat_id=chat_id)
    
    return redirect('group_chat', chat_id=chat_id)


@login_required
def private_chat(request, chat_id):
    chat = get_object_or_404(PrivateChat, id=chat_id)
    if request.user != chat.admin and request.user != chat.user:
        return redirect('chatroom_home')
    messages = Message.objects.filter(chat_type='private', chat_id=chat_id).order_by('timestamp')
    form = MessageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid() and not 'forward_message' in request.POST and not 'emoji' in request.POST:
            message = form.save(commit=False)
            message.chat_type = 'private'
            message.chat_id = chat_id
            message.sender = request.user
            replied_to_id = request.POST.get('replied_to')
            forwarded_from_id = request.POST.get('forwarded_from')
            if replied_to_id:
                message.replied_message = Message.objects.get(id=replied_to_id)
            if forwarded_from_id:
                message.forwarded_message = Message.objects.get(id=forwarded_from_id)
            if request.FILES.get('file'):
                message.file = request.FILES.get('file')
            message.save()
            return redirect('private_chat', chat_id=chat_id)
        elif 'forward_message' in request.POST:
            original_message = Message.objects.get(id=request.POST['forward_message'])
            forward_to_type = request.POST['forward_to_type']
            forward_to_id = request.POST['forward_to_id']
            if forward_to_type == 'user':
                target_chat, created = PrivateChat.objects.get_or_create(admin=request.user, user=User.objects.get(id=forward_to_id))
                Message.objects.create(
                    chat_type='private',
                    chat_id=target_chat.id,
                    sender=request.user,
                    content=original_message.content,
                    forwarded_message=original_message,
                    file=original_message.file
                )
            elif forward_to_type == 'group_chat':
                target_chat = GroupChat.objects.get(id=forward_to_id)
                Message.objects.create(
                    chat_type='group',
                    chat_id=target_chat.id,
                    sender=request.user,
                    content=original_message.content,
                    forwarded_message=original_message,
                    file=original_message.file
                )
            return redirect('group_chat' if forward_to_type == 'group_chat' else 'private_chat', chat_id=forward_to_id)
        elif 'emoji' in request.POST:
            message = Message.objects.get(id=request.POST['message_id'])
            message.content += " " + request.POST['emoji']
            message.save()
            return JsonResponse({'status': 'success'})
    else:
        form = MessageForm()
    users = User.objects.exclude(id__in=[request.user.id, chat.admin.id, chat.user.id])
    group_chats = GroupChat.objects.filter(members=request.user)
    return render(request, 'chatroom/private_chat.html', {'chat': chat, 'messages': messages, 'form': form, 'users': users, 'group_chats': group_chats})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import GroupChat, Message
from .forms import MessageForm

@login_required
def group_chat(request, chat_id):
    chat = get_object_or_404(GroupChat, id=chat_id)
    if request.user not in chat.members.all():
        return redirect('chatroom_home')
    messages = Message.objects.filter(chat_type='group', chat_id=chat_id).order_by('timestamp')
    form = MessageForm(request.POST, request.FILES)
    
    if request.method == 'POST':
        if 'content' in request.POST:  # Sending a message
            if form.is_valid():
                message = form.save(commit=False)
                message.chat_type = 'group'
                message.chat_id = chat_id
                message.sender = request.user
                replied_to_id = request.POST.get('replied_to')
                if replied_to_id:
                    message.replied_message = Message.objects.get(id=replied_to_id)
                forwarded_from_id = request.POST.get('forwarded_from')
                if forwarded_from_id:
                    message.forwarded_message = Message.objects.get(id=forwarded_from_id)
                if request.FILES.get('file'):
                    message.file = request.FILES.get('file')
                message.save()
                return redirect('group_chat', chat_id=chat_id)
        
        elif 'forward_message' in request.POST:  # Forwarding a message
            original_message = Message.objects.get(id=request.POST['forward_message'])
            forward_to_type = request.POST['forward_to_type']
            forward_to_id = request.POST['forward_to_id']
            if forward_to_type == 'user':
                target_chat, created = PrivateChat.objects.get_or_create(admin=request.user, user=User.objects.get(id=forward_to_id))
                Message.objects.create(
                    chat_type='private',
                    chat_id=target_chat.id,
                    sender=request.user,
                    content=original_message.content,
                    forwarded_message=original_message,
                    file=original_message.file
                )
            elif forward_to_type == 'group_chat':
                target_chat = GroupChat.objects.get(id=forward_to_id)
                Message.objects.create(
                    chat_type='group',
                    chat_id=target_chat.id,
                    sender=request.user,
                    content=original_message.content,
                    forwarded_message=original_message,
                    file=original_message.file
                )
            return redirect('group_chat' if forward_to_type == 'group_chat' else 'private_chat', chat_id=forward_to_id)
        
        elif 'emoji' in request.POST:  # Adding an emoji
            message = Message.objects.get(id=request.POST['message_id'])
            message.content += " " + request.POST['emoji']
            message.save()
            return JsonResponse({'status': 'success'})
        
        elif 'selected_users[]' in request.POST:  # Adding users to the group
            selected_users = request.POST.getlist('selected_users[]')
            for user_id in selected_users:
                user = User.objects.get(id=user_id)
                chat.members.add(user)
            return JsonResponse({'status': 'success'})
        
        elif 'remove_user' in request.POST:  # Removing a user
            remove_user_id = request.POST['remove_user']
            if request.user == chat.admin:
                user = User.objects.get(id=remove_user_id)
                chat.members.remove(user)
            return JsonResponse({'status': 'success'})
    
    else:
        form = MessageForm()
    
    users = User.objects.exclude(id__in=list(chat.members.values_list('id', flat=True)))
    group_chats = GroupChat.objects.filter(members=request.user)
    
    return render(request, 'chatroom/group_chat.html', {
        'chat': chat,
        'messages': messages,
        'form': form,
        'users': users,
        'group_chats': group_chats
    })



