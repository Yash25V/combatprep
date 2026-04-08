from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from records.models import SoldierProfile, Assessment
from accounts.models import User
from .forms import CustomUserCreationForm

@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    if user.is_admin():
        context['total_users'] = User.objects.count()
        context['total_soldiers'] = User.objects.filter(role='SOLDIER').count()
        context['total_assessments'] = Assessment.objects.count()
        context['all_soldiers'] = User.objects.filter(role='SOLDIER').order_by('username')
        context['all_officers'] = User.objects.filter(role='OFFICER').order_by('username')
        context['all_assessments'] = Assessment.objects.all().order_by('-date_recorded')
    elif user.is_officer():
        context['total_soldiers'] = User.objects.filter(role='SOLDIER').count()
        context['recent_assessments'] = Assessment.objects.filter(officer=user).order_by('-date_recorded')[:5]
    elif user.is_soldier():
        try:
            profile = user.profile
        except SoldierProfile.DoesNotExist:
            profile = SoldierProfile.objects.create(user=user)
        context['profile'] = profile
        context['assessments'] = user.assessments.order_by('-date_recorded')
        
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
