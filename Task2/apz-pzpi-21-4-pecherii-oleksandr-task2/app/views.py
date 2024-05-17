from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import HttpRequest, JsonResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import connection
from .backup_db import backup_database


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


class logIn(generic.View):
    form_class = LoginUserForm
    template_name = "app/login.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = LoginUserForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(
                        request, f"You are logged in as {username}")
                    return redirect('home')
                else:
                    messages.error(request, "Error")
            else:
                messages.error(request, "Username or password incorrect")
        form = LoginUserForm()
        return render(request, "app/login.html", {"form": form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = RegistrationForm()
    return render(request, 'app/register.html', {'form': form})



def index(request):
    user_email = request.user.email if request.user.is_authenticated else None
    return render(request, 'app/index.html', {'user_email': user_email})


# Organizer CRUD operations
def organizer_list(request):
    organizers = Organizer.objects.all()
    return render(request, 'app/organizer_list.html', {'organizers': organizers})


def organizer_detail(request, organizer_id):
    organizer = get_object_or_404(Organizer, pk=organizer_id)
    return render(request, 'app/organizer_detail.html', {'organizer': organizer})


@login_required
def organizer_create(request):
    if request.method == 'POST':
        if not request.user.role in ['org', 'admin']:
            messages.error(request, 'You are not permitted to perform this action.')
            return redirect('index')
        form = OrganizerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organizer_list')
    else:
        form = OrganizerForm()
    return render(request, 'app/organizer_form.html', {'form': form})


@login_required
def organizer_update(request, organizer_id):
    organizer = get_object_or_404(Organizer, pk=organizer_id)
    if request.method == 'POST':
        if not request.user.role in ['org', 'admin']:
            messages.error(request, 'You are not permitted to perform this action.')
            return redirect('index')
        form = OrganizerForm(request.POST, instance=organizer)
        if form.is_valid():
            form.save()
            return redirect('organizer_detail', organizer_id=organizer_id)
    else:
        form = OrganizerForm(instance=organizer)
    return render(request, 'app/organizer_form.html', {'form': form})


@login_required
def organizer_delete(request, organizer_id):
    organizer = get_object_or_404(Organizer, pk=organizer_id)
    if request.method == 'POST':
        if not request.user.role in ['org', 'admin']:
            messages.error(request, 'You are not permitted to perform this action.')
            return redirect('index')
        organizer.delete()
        return redirect('organizer_list')
    return render(request, 'organizer_confirm_delete.html', {'organizer': organizer})


# Gear CRUD operations
def gear_list(request):
    gears = Gear.objects.all()
    return render(request, 'app/gear_list.html', {'gears': gears})


def gear_detail(request, gear_id):
    gear = get_object_or_404(Gear, pk=gear_id)
    return render(request, 'app/gear_detail.html', {'gear': gear})


@login_required
def gear_create(request):
    if request.method == 'POST':
        if not request.user.role in ['org', 'admin']:
            messages.error(request, 'You are not permitted to perform this action.')
            return redirect('index')
        form = GearForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gear_list')
    else:
        form = GearForm()
    return render(request, 'app/gear_form.html', {'form': form})


@login_required
def gear_update(request, gear_id):
    gear = get_object_or_404(Gear, pk=gear_id)
    if request.method == 'POST':
        if not request.user.role in ['org', 'admin']:
            messages.error(request, 'You are not permitted to perform this action.')
            return redirect('index')
        form = GearForm(request.POST, instance=gear)
        if form.is_valid():
            form.save()
            return redirect('gear_detail', gear_id=gear_id)
    else:
        form = GearForm(instance=gear)
    return render(request, 'app/gear_form.html', {'form': form})


@login_required
def gear_delete(request, gear_id):
    gear = get_object_or_404(Gear, pk=gear_id)
    if request.method == 'POST':
        if not request.user.role in ['org', 'admin']:
            messages.error(request, 'You are not permitted to perform this action.')
            return redirect('index')
        gear.delete()
        return redirect('gear_list')
    return render(request, 'gear_confirm_delete.html', {'gear': gear})


# DiveComputer CRUD operations
def dive_computer_list(request):
    dive_computers = DiveComputer.objects.all()
    return render(request, 'app/dive_computer_list.html', {'dive_computers': dive_computers})


@login_required
def dive_computer_detail(request, dive_computer_id):
    dive_computer = get_object_or_404(DiveComputer, pk=dive_computer_id)
    return render(request, 'app/dive_computer_detail.html', {'dive_computer': dive_computer})


@login_required
def dive_computer_create(request):
    if request.method == 'POST':
        form = DiveComputerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dive_computer_list')
    else:
        form = DiveComputerForm()
    return render(request, 'app/dive_computer_form.html', {'form': form})


@login_required
def dive_computer_update(request, dive_computer_id):
    dive_computer = get_object_or_404(DiveComputer, pk=dive_computer_id)
    if request.method == 'POST':
        form = DiveComputerForm(request.POST, instance=dive_computer)
        if form.is_valid():
            form.save()
            return redirect('dive_computer_detail', dive_computer_id=dive_computer_id)
    else:
        form = DiveComputerForm(instance=dive_computer)
    return render(request, 'app/dive_computer_form.html', {'form': form})


@login_required
def dive_computer_delete(request, dive_computer_id):
    dive_computer = get_object_or_404(DiveComputer, pk=dive_computer_id)
    if request.method == 'POST':
        dive_computer.delete()
        return redirect('dive_computer_list')
    return render(request, 'dive_computer_confirm_delete.html', {'dive_computer': dive_computer})


# Activity CRUD operations
def activity_list(request):
    activities = Activity.objects.all()
    return render(request, 'app/activity_list.html', {'activities': activities})


def activity_detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    return render(request, 'app/activity_detail.html', {'activity': activity})


@login_required
def activity_create(request):
    if request.method == 'POST':
        if not request.user.role in ['org', 'admin']:
            messages.error(request, 'You are not permitted to perform this action.')
            return redirect('index')
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('activity_list')
    else:
        form = ActivityForm()
    return render(request, 'app/activity_form.html', {'form': form})


@login_required
def activity_update(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if request.method == 'POST':
        if not request.user.role in ['org', 'admin']:
            messages.error(request, 'You are not permitted to perform this action.')
            return redirect('index')
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activity_detail', activity_id=activity_id)
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'app/activity_form.html', {'form': form})


@login_required
def activity_delete(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if request.method == 'POST':
        if not request.user.role in ['org', 'admin']:
            messages.error(request, 'You are not permitted to perform this action.')
            return redirect('index')
        activity.delete()
        return redirect('activity_list')
    return render(request, 'activity_confirm_delete.html', {'activity': activity})


# Participation CRUD operations
def participation_list(request):
    participations = Participation.objects.all()
    return render(request, 'app/participation_list.html', {'participations': participations})

def participation_detail(request, participation_id):
    participation = get_object_or_404(Participation, pk=participation_id)
    return render(request, 'app/participation_detail.html', {'participation': participation})

@login_required  
def participation_create(request):
    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        if form.is_valid():
            user = request.user
            participation = form.save(commit=False)
            participation.user = user
            participation.save()
            return redirect('participation_list')
    else:
        form = ParticipationForm()
    return render(request, 'app/participation_form.html', {'form': form})


@login_required
def participation_update(request, participation_id):
    participation = get_object_or_404(Participation, pk=participation_id)
    if request.method == 'POST':
        form = ParticipationForm(request.POST, instance=participation)
        if form.is_valid():
            form.save()
            return redirect('participation_detail', participation_id=participation_id)
    else:
        form = ParticipationForm(instance=participation)
    return render(request, 'app/participation_form.html', {'form': form})

@login_required
def participation_delete(request, participation_id):
    participation = get_object_or_404(Participation, pk=participation_id)
    if request.method == 'POST':
        participation.delete()
        return redirect('participation_list')
    return render(request, 'participation_confirm_delete.html', {'participation': participation})


@login_required
def gear_distribution(request, activity_id):
    if request.method == 'POST':
        activity = get_object_or_404(Activity, id=activity_id)
        organizer = activity.organizer

        if not request.user.role in ['org', 'admin'] and request.user != organizer:
            return JsonResponse({'error': 'You are not permitted to perform this action.'}, status=403)

        participations = Participation.objects.filter(activity=activity)

        for participation in participations:
            # Get all available gear for the organizer
            available_gear = Gear.objects.filter(organizer=organizer, is_reserved=False)

            # Filter available gear by user's size and gear type
            for gear_type in Gear.GEAR_TYPE_CHOICES:
                user_gear = participations.filter(user=participation.user, gear__gear_type=gear_type[0]).first()

                if not user_gear:
                    # User does not have this type of gear yet
                    if gear_type[0] == 'Wetsuit':
                        # For wetsuits, also consider the wetsuit size
                        gear = available_gear.filter(
                            gear_type=gear_type[0],
                            wetsuit_size__size__in=[
                                participation.user.height,
                                participation.user.foot_size
                            ]
                        ).first()
                    else:
                        gear = available_gear.filter(
                            gear_type=gear_type[0],
                            size__in=[participation.user.height, participation.user.foot_size]
                        ).first()

                    if gear:
                        # Reserve the gear for this participation
                        gear.is_reserved = True
                        gear.save()

                        # Assign the reserved gear to the participation
                        participation.gear = gear
                        participation.is_gear_reserved = True
                        participation.save()

                        # Update gear_id field in participation
                        participation.gear_id = gear.id
                        participation.save()

                        # Ensure the user doesn't have more than one gear of each type
                        participations.filter(user=participation.user, gear__gear_type=gear_type[0]).exclude(
                            id=participation.id).update(is_gear_reserved=False)

                        break  # Stop searching for gear once one is found for this user

        return JsonResponse({'message': 'Gear distribution completed successfully.'})
    else:
        return JsonResponse({'error': 'This view only accepts POST requests.'}, status=405)

@login_required
def free_gear_for_activity(request, activity_id):
    if request.method == 'POST':
        if not request.user.role in ['org', 'admin']:
            messages.error(request, 'You are not permitted to perform this action.')
            return redirect('index')
        
        activity = Activity.objects.get(id=activity_id)

        # Reset gear for the activity
        Gear.objects.filter(participation__activity=activity).update(is_reserved=False)
        
        # Remove connections between gear and participations for the activity
        Participation.objects.filter(activity=activity).update(gear=None)

        return HttpResponse("Gear freed successfully.")
    else:
        return HttpResponse("This view only accepts POST requests.")


@login_required
def backup_database_view(request):
    if request.user.role != 'admin':
        return JsonResponse({'message': 'You are not permitted to perform this action.'}, status=403)

    # Call the backup function
    backup_database(
        host='localhost',
        port='5432',
        database='DeepDive',
        user='postgres',
        password='Postpassword123'
    )
    
    return JsonResponse({'message': 'Backup process initiated successfully.'})
