from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import Event, Category
from .forms import EventForm, CategoryForm


def permission_denied_view(request):
    """View to show when user doesn't have permission"""
    return render(request, 'events/no-permission.html', status=403)


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())


def is_organizer(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Organizer').exists())


def is_participant(user):
    return user.is_authenticated and user.groups.filter(name='Participant').exists()


def is_admin_or_organizer(user):
    """Check if user is Admin or Organizer (both can manage events and categories)"""
    return user.is_authenticated and (
        user.is_superuser or 
        user.groups.filter(name__in=['Admin', 'Organizer']).exists()
    )


# --- Home View ---

def home(request):
    """Homepage with hero section and upcoming events"""
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).select_related('category').order_by('date')[:6]
    total_events = Event.objects.count()
    total_categories = Category.objects.count()
    
    # Count total RSVPs across all events
    total_rsvps = Event.objects.aggregate(Count('rsvped_users'))['rsvped_users__count'] or 0
    
    context = {
        'upcoming_events': upcoming_events,
        'total_events': total_events,
        'total_categories': total_categories,
        'total_rsvps': total_rsvps,
    }
    return render(request, 'events/home.html', context)

# --- Dashboard Views ---

@login_required
def dashboard(request):
    """Redirect to appropriate dashboard based on user role"""
    user = request.user
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        return redirect('admin_dashboard')
    elif user.groups.filter(name='Organizer').exists():
        return redirect('organizer_dashboard')
    elif user.groups.filter(name='Participant').exists():
        return redirect('participant_dashboard')
    else:
        # Default to participant dashboard for users without specific role
        return redirect('participant_dashboard')


@login_required
@user_passes_test(is_admin, login_url='/no-permission/')
def admin_dashboard(request):
    """Admin Dashboard: Manage all events, participants, and categories"""
    today = timezone.now().date()
    
    # Stats Grid
    total_rsvps = Event.objects.aggregate(Count('rsvped_users'))['rsvped_users__count'] or 0
    total_events = Event.objects.count()
    upcoming_events_count = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()
    total_categories = Category.objects.count()
    
    # Event List with filters
    filter_type = request.GET.get('filter', 'upcoming')
    
    if filter_type == 'upcoming':
        events = Event.objects.filter(date__gte=today).select_related('category').prefetch_related('rsvped_users')
        list_title = "Upcoming Events"
    elif filter_type == 'past':
        events = Event.objects.filter(date__lt=today).select_related('category').prefetch_related('rsvped_users')
        list_title = "Past Events"
    elif filter_type == 'all':
        events = Event.objects.all().select_related('category').prefetch_related('rsvped_users')
        list_title = "All Events"
    else:
        events = Event.objects.filter(date=today).select_related('category').prefetch_related('rsvped_users')
        list_title = "Today's Events"

    context = {
        'total_rsvps': total_rsvps,
        'total_events': total_events,
        'upcoming_events': upcoming_events_count,
        'past_events_count': past_events_count,
        'total_categories': total_categories,
        'events': events,
        'list_title': list_title,
        'dashboard_type': 'admin',
    }
    return render(request, 'events/admin_dashboard.html', context)


@login_required
@user_passes_test(is_organizer, login_url='/no-permission/')
def organizer_dashboard(request):
    """Organizer Dashboard: Manage events and categories"""
    today = timezone.now().date()
    
    # Stats Grid
    total_rsvps = Event.objects.aggregate(Count('rsvped_users'))['rsvped_users__count'] or 0
    total_events = Event.objects.count()
    upcoming_events_count = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()
    total_categories = Category.objects.count()
    
    # Event List with filters
    filter_type = request.GET.get('filter', 'upcoming')
    
    if filter_type == 'upcoming':
        events = Event.objects.filter(date__gte=today).select_related('category').prefetch_related('rsvped_users')
        list_title = "Upcoming Events"
    elif filter_type == 'past':
        events = Event.objects.filter(date__lt=today).select_related('category').prefetch_related('rsvped_users')
        list_title = "Past Events"
    elif filter_type == 'all':
        events = Event.objects.all().select_related('category').prefetch_related('rsvped_users')
        list_title = "All Events"
    else:
        events = Event.objects.filter(date=today).select_related('category').prefetch_related('rsvped_users')
        list_title = "Today's Events"

    context = {
        'total_rsvps': total_rsvps,
        'total_events': total_events,
        'upcoming_events': upcoming_events_count,
        'past_events_count': past_events_count,
        'total_categories': total_categories,
        'events': events,
        'list_title': list_title,
        'dashboard_type': 'organizer',
    }
    return render(request, 'events/organizer_dashboard.html', context)


@login_required
def participant_dashboard(request):
    """Participant Dashboard: View events they have RSVP'd to"""
    today = timezone.now().date()
    user = request.user
    
    # Get events user has RSVP'd to
    rsvped_events = Event.objects.filter(rsvped_users=user).select_related('category').prefetch_related('rsvped_users')
    
    # Stats Grid
    my_rsvps_count = rsvped_events.count()
    upcoming_rsvps_count = rsvped_events.filter(date__gte=today).count()
    past_rsvps_count = rsvped_events.filter(date__lt=today).count()
    
    # Event List with filters
    filter_type = request.GET.get('filter', 'upcoming')
    
    if filter_type == 'upcoming':
        events = rsvped_events.filter(date__gte=today)
        list_title = "My Upcoming Events"
    elif filter_type == 'past':
        events = rsvped_events.filter(date__lt=today)
        list_title = "My Past Events"
    elif filter_type == 'all':
        events = rsvped_events
        list_title = "All My Events"
    else:
        events = rsvped_events.filter(date=today)
        list_title = "My Events Today"

    context = {
        'total_rsvps': my_rsvps_count,
        'total_events': my_rsvps_count,
        'upcoming_events': upcoming_rsvps_count,
        'past_events_count': past_rsvps_count,
        'events': events,
        'list_title': list_title,
        'dashboard_type': 'participant',
    }
    return render(request, 'events/participant_dashboard.html', context)


# --- Event CRUD & List ---

def event_list(request):
    # Base query with RSVP count
    queryset = Event.objects.select_related('category').annotate(
        rsvp_count=Count('rsvped_users')
    )
    
    # Get query params
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Search
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )
    
    # Filter by category
    if category_id:
        queryset = queryset.filter(category_id=category_id)
        
    # Filter by date range
    if start_date and end_date:
        queryset = queryset.filter(date__range=[start_date, end_date])
    
    categories = Category.objects.all()

    context = {
        'events': queryset.order_by('-date'),
        'categories': categories,
    }
    return render(request, 'events/event_list.html', context)

@login_required
def event_detail(request, id):
    # Optimized query with RSVP users
    event = get_object_or_404(
        Event.objects.select_related('category').prefetch_related('rsvped_users'),
        id=id
    )
    
    # Check if current user has RSVP'd
    user_has_rsvped = False
    if request.user.is_authenticated:
        user_has_rsvped = event.rsvped_users.filter(id=request.user.id).exists()
    
    # Check if user can edit/delete (admin or organizer)
    can_manage_event = is_admin_or_organizer(request.user)
    
    context = {
        'event': event,
        'user_has_rsvped': user_has_rsvped,
        'can_manage_event': can_manage_event,
    }
    return render(request, 'events/event_detail.html', context)

@login_required
@user_passes_test(is_admin_or_organizer, login_url='/no-permission/')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})

@login_required
@user_passes_test(is_admin_or_organizer, login_url='/no-permission/')
def event_update(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', id=id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Update Event'})

@login_required
@user_passes_test(is_admin_or_organizer, login_url='/no-permission/')
def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'object': event})

# --- Category CRUD ---

def category_list(request):
    categories = Category.objects.annotate(event_count=Count('events'))
    return render(request, 'events/category_list.html', {'categories': categories})

@login_required
@user_passes_test(is_admin_or_organizer, login_url='/no-permission/')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Create Category'})

@login_required
@user_passes_test(is_admin_or_organizer, login_url='/no-permission/')
def category_update(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Update Category'})

@login_required
@user_passes_test(is_admin_or_organizer, login_url='/no-permission/')
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'events/confirm_delete.html', {'object': category})

# --- RSVP Views ---

@login_required
def event_rsvp(request, id):
    """Add user RSVP to event"""
    event = get_object_or_404(Event, id=id)
    
    if request.user in event.rsvped_users.all():
        messages.warning(request, 'You have already RSVP\'d to this event!')
    else:
        event.rsvped_users.add(request.user)
        messages.success(request, f'Successfully RSVP\'d to {event.name}!')
    
    return redirect('event_detail', id=id)

@login_required
def event_cancel_rsvp(request, id):
    """Cancel user RSVP to event"""
    event = get_object_or_404(Event, id=id)
    
    if request.user not in event.rsvped_users.all():
        messages.warning(request, 'You have not RSVP\'d to this event!')
    else:
        event.rsvped_users.remove(request.user)
        messages.success(request, f'RSVP cancelled for {event.name}!')
    
    return redirect('event_detail', id=id)