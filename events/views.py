# events/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

# --- Home View ---

def home(request):
    """Homepage with hero section and upcoming events"""
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).select_related('category').order_by('date')[:6]
    total_events = Event.objects.count()
    total_categories = Category.objects.count()
    total_participants = Participant.objects.count()
    
    context = {
        'upcoming_events': upcoming_events,
        'total_events': total_events,
        'total_categories': total_categories,
        'total_participants': total_participants,
    }
    return render(request, 'events/home.html', context)

# --- Dashboard View ---

def dashboard(request):
    today = timezone.now().date()
    
    # 1. Stats Grid Data
    total_participants = Participant.objects.count() # Aggregate query 1
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()
    
    # 2. Interactive List Logic
    filter_type = request.GET.get('filter', 'upcoming') # Default to 'upcoming'
    
    if filter_type == 'upcoming':
        events = Event.objects.filter(date__gte=today).select_related('category')
        list_title = "Upcoming Events"
    elif filter_type == 'past':
        events = Event.objects.filter(date__lt=today).select_related('category')
        list_title = "Past Events"
    elif filter_type == 'all':
        events = Event.objects.all().select_related('category')
        list_title = "All Events"
    else: # 'today'
        events = Event.objects.filter(date=today).select_related('category')
        list_title = "Today's Events"

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events_count': past_events_count,
        'events': events,
        'list_title': list_title,
    }
    return render(request, 'events/dashboard.html', context)


# --- Event CRUD & List Views ---

def event_list(request):
    # Base query: Optimized with select_related and annotate
    queryset = Event.objects.select_related('category').annotate(
        participant_count=Count('participants')
    )
    
    # Get query params for search and filtering
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # 5. Search Feature
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )
    
    # 3. Filter Query (Category)
    if category_id:
        queryset = queryset.filter(category_id=category_id)
        
    # 3. Filter Query (Date Range)
    if start_date and end_date:
        queryset = queryset.filter(date__range=[start_date, end_date])
    
    categories = Category.objects.all()

    context = {
        'events': queryset.order_by('-date'),
        'categories': categories,
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, id):
    # Optimized query: Use select_related for category (FK) and prefetch_related for participants (M2M)
    event = get_object_or_404(
        Event.objects.select_related('category').prefetch_related('participants'),
        id=id
    )
    context = {'event': event}
    return render(request, 'events/event_detail.html', context)

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})

def event_update(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', id=id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Update Event'})

def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'object': event})

# --- Category CRUD ---

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Create Category'})

def category_update(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {'form': form, 'title': 'Update Category'})

def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'events/confirm_delete.html', {'object': category})

# --- Participant CRUD ---

def participant_list(request):
    participants = Participant.objects.prefetch_related('events') # Prefetch events for efficiency
    return render(request, 'events/participant_list.html', {'participants': participants})

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'events/participant_form.html', {'form': form, 'title': 'Create Participant'})

def participant_update(request, id):
    participant = get_object_or_404(Participant, id=id)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'events/participant_form.html', {'form': form, 'title': 'Update Participant'})

def participant_delete(request, id):
    participant = get_object_or_404(Participant, id=id)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'events/confirm_delete.html', {'object': participant})