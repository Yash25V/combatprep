from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import SoldierProfile, Assessment, TrainingProgram
from accounts.models import User
from .forms import SoldierProfileForm, AssessmentForm, TrainingProgramForm, CSVUploadForm
import csv
import io

def is_officer_or_admin(user):
    return user.is_authenticated and (user.is_officer() or user.is_admin())

@login_required
@user_passes_test(is_officer_or_admin)
def soldier_list(request):
    soldiers = User.objects.filter(role='SOLDIER').select_related('profile')
    return render(request, 'records/soldier_list.html', {'soldiers': soldiers})

@login_required
@user_passes_test(is_officer_or_admin)
def soldier_detail(request, pk):
    soldier = get_object_or_404(User, pk=pk, role='SOLDIER')
    try:
        profile = soldier.profile
    except SoldierProfile.DoesNotExist:
        profile = SoldierProfile.objects.create(user=soldier)
    assessments = soldier.assessments.order_by('-date_recorded')
    return render(request, 'records/soldier_detail.html', {
        'soldier': soldier,
        'profile': profile,
        'assessments': assessments
    })

@login_required
@user_passes_test(lambda u: u.is_officer())
def add_assessment(request, pk):
    soldier = get_object_or_404(User, pk=pk, role='SOLDIER')
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.soldier = soldier
            assessment.officer = request.user
            assessment.save()
            messages.success(request, 'Assessment added successfully.')
            return redirect('soldier_detail', pk=pk)
    else:
        form = AssessmentForm()
    return render(request, 'records/assessment_form.html', {'form': form, 'soldier': soldier})

@login_required
def update_profile(request):
    try:
        profile = request.user.profile
    except SoldierProfile.DoesNotExist:
        profile = SoldierProfile.objects.create(user=request.user)
        
    if request.method == 'POST':
        form = SoldierProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:
        form = SoldierProfileForm(instance=profile)
        
    return render(request, 'records/profile_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_officer() or u.is_admin())
def create_training_program(request):
    if request.method == 'POST':
        form = TrainingProgramForm(request.POST)
        if form.is_valid():
            program = form.save(commit=False)
            program.officer = request.user
            program.save()
            messages.success(request, 'Training program created successfully.')
            return redirect('dashboard')
    else:
        form = TrainingProgramForm()
    return render(request, 'records/training_program_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_officer() or u.is_admin())
def upload_scores(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is not a CSV file.')
                return redirect('upload_scores')

            dataset = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(dataset)
            next(io_string) # Skip header

            count = 0
            for row in csv.reader(io_string, delimiter=',', quotechar='"'):
                # Format: Username, Physical Score, Technical Score, Training Score, Comments
                if len(row) >= 4:
                    username = row[0].strip()
                    try:
                        soldier = User.objects.get(username=username, role='SOLDIER')
                        Assessment.objects.create(
                            soldier=soldier,
                            officer=request.user,
                            physical_fitness_score=int(row[1]),
                            technical_skills_score=int(row[2]),
                            training_score=int(row[3]),
                            comments=row[4] if len(row) > 4 else ''
                        )
                        count += 1
                    except User.DoesNotExist:
                        continue
                    except ValueError:
                        continue
            
            messages.success(request, f'Successfully uploaded {count} assessments.')
            return redirect('dashboard')
    else:
        form = CSVUploadForm()
    
    return render(request, 'records/upload_scores.html', {'form': form})
