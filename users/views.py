from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm - Created Our Own Form
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

# def register(request):
#     if request.method == 'POST':
#         form =  UserRegisterForm(request.POST) # Used to instantiate User Cretion with That Post data otherwise blank form
#         if form.is_valid():
#             user = form.save() # Save the User form detail - Create User
#             # user.is_active = False # Helps In Validating the Email Id
#             username = form.cleaned_data.get('username') # Getting the User name from the form
#             messages.success(request, f'Account is Successfully Created for {username}, Now You Can Log In') # after this import redirect the user to home page - after validation 
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form' : form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request):
    if request.method == 'POST':
        userUpdateForm = UserUpdateForm(request.POST,instance=request.user)
        profileUpdateForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if userUpdateForm.is_valid and profileUpdateForm.is_valid:
            userUpdateForm.save()
            profileUpdateForm.save()
            messages.success(request, f'Profile is Successfully Updated') # after this import redirect the user to home page - after validation 
            return redirect('profile')
    else:
        userUpdateForm = UserUpdateForm(instance= request.user)
        profileUpdateForm = ProfileUpdateForm(instance=None)
    context = {
        'userUpdateForm' : userUpdateForm,
        'profileUpdateForm' : profileUpdateForm
    }
    return render(request, 'users/profile.html', context)
