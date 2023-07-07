from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .forms import RegistrationForm,CreatePollForm, ProfileUpdateForm, UserUpdateForm
from .models import Poll

class indexView(TemplateView):
    template_name = 'index.html'

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')

        form = RegistrationForm(request.POST)
        if form.is_valid():
            my_user = User.objects.create_user(username=username, email=email, password=pass1)
            my_user.save()
            return render(request, 'infobeans_polling_app/login.html', {})  # Redirect to the login page after successful registration
    else:
        # Clear the form errors to prevent them from being displayed on the page
        form = RegistrationForm()
    return render(request, 'infobeans_polling_app/registration.html', {'form': form})


def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Django's built-in authentication function:
        user = authenticate(request, username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return redirect('home')
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'infobeans_polling_app/login.html', {})

@login_required
def result(request):
    return render(request,'infobeans_polling_app/result.html')

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/userauth_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return render(request, 'index.html')

def home(request):
    try:
        polls = Poll.objects.all()
        print(polls)
    except Exception as e:
        print(f"Error occurred: {str(e)}")

    context = {
        'polls': polls,
    }
    return render(request, 'home.html', context)
def create(request):
    if request.method == 'POST':
        poll = Poll()
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {
        'form' : form
    }
    return render(request, 'infobeans_polling_app/create.html', context)


def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()
        return redirect('result', poll.id)

    context = {
        'poll' : poll
    }
    return render(request, 'vote.html', context)

def result(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll
    }
    return render(request, 'result.html', context)

# Update it here
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)
