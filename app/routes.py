from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import Event, Resource, EventResourceAllocation
from . import db
from .forms import EventForm, ResourceForm, AllocationForm
from datetime import datetime
main = Blueprint('main', __name__)

def overlaps(s1,e1,s2,e2):
    return (s1 < e2) and (s2 < e1)

@main.route('/')
def index():
    return render_template('index.html')

# ------ EVENTS -------
@main.route('/events')
def list_events():
    events = Event.query.order_by(Event.start_time).all()
    return render_template('events/list_events.html', events=events)

@main.route('/events/add', methods=['GET','POST'])
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        s = form.start_time.data
        e = form.end_time.data
        if not s < e:
            flash('Start time must be before end time.', 'danger')
        else:
            event = Event(title=form.title.data, start_time=s, end_time=e, description=form.description.data)
            # check conflicts with existing allocations for resources already allocated to this event? none yet
            db.session.add(event)
            db.session.commit()
            flash('Event added.', 'success')
            return redirect(url_for('.list_events'))
    return render_template('events/add_event.html', form=form)

@main.route('/events/edit/<int:event_id>', methods=['GET','POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        s = form.start_time.data
        e = form.end_time.data
        if not s < e:
            flash('Start time must be before end time.', 'danger')
        else:
            # Before applying the edit, check for conflicts for resources allocated to this event
            allocations = [alloc.resource for alloc in event.allocations]
            # Temporarily set times to check
            new_s = s
            new_e = e
            conflict = None
            for r in allocations:
                # find other events that use this resource
                for alloc in r.allocations:
                    other = alloc.event
                    if other.event_id == event.event_id:
                        continue
                    if overlaps(new_s, new_e, other.start_time, other.end_time):
                        conflict = f"Resource '{r.resource_name}' conflicts with event '{other.title}' ({other.start_time} - {other.end_time})"
                        break
                if conflict:
                    break
            if conflict:
                flash(conflict, 'danger')
            else:
                event.title = form.title.data
                event.start_time = s
                event.end_time = e
                event.description = form.description.data
                db.session.commit()
                flash('Event updated.', 'success')
                return redirect(url_for('.list_events'))
    return render_template('events/edit_event.html', form=form, event=event)

@main.route('/events/<int:event_id>')
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('events/view_event.html', event=event)

# ------ RESOURCES -------
@main.route('/resources')
def list_resources():
    resources = Resource.query.order_by(Resource.resource_name).all()
    return render_template('resources/list_resources.html', resources=resources)

@main.route('/resources/add', methods=['GET','POST'])
def add_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        r = Resource(resource_name=form.resource_name.data, resource_type=form.resource_type.data)
        db.session.add(r)
        db.session.commit()
        flash('Resource added.', 'success')
        return redirect(url_for('.list_resources'))
    return render_template('resources/add_resource.html', form=form)

@main.route('/resources/edit/<int:resource_id>', methods=['GET','POST'])
def edit_resource(resource_id):
    r = Resource.query.get_or_404(resource_id)
    form = ResourceForm(obj=r)
    if form.validate_on_submit():
        r.resource_name = form.resource_name.data
        r.resource_type = form.resource_type.data
        db.session.commit()
        flash('Resource updated.', 'success')
        return redirect(url_for('.list_resources'))
    return render_template('resources/add_resource.html', form=form, resource=r)

# ------ ALLOCATIONS -------
@main.route('/allocate', methods=['GET','POST'])
def allocate():
    form = AllocationForm()
    form.event.choices = [(e.event_id, f"{e.title} ({e.start_time.strftime('%Y-%m-%d %H:%M')} - {e.end_time.strftime('%H:%M')})") for e in Event.query.order_by(Event.start_time).all()]
    form.resources.choices = [(r.resource_id, f"{r.resource_name} ({r.resource_type})") for r in Resource.query.order_by(Resource.resource_name).all()]
    if form.validate_on_submit():
        event = Event.query.get(form.event.data)
        selected_ids = form.resources.data
        errors = []
        for rid in selected_ids:
            r = Resource.query.get(rid)
            # check for conflicts with other events using this resource
            for alloc in r.allocations:
                other = alloc.event
                if other.event_id == event.event_id:
                    continue
                if overlaps(event.start_time, event.end_time, other.start_time, other.end_time):
                    errors.append(f"Resource '{r.resource_name}' is already booked by event '{other.title}' ({other.start_time} - {other.end_time})")
                    break
            if not errors:
                # create allocation if not already allocated
                existing = EventResourceAllocation.query.filter_by(event_id=event.event_id, resource_id=r.resource_id).first()
                if not existing:
                    a = EventResourceAllocation(event_id=event.event_id, resource_id=r.resource_id)
                    db.session.add(a)
        if errors:
            for e in errors:
                flash(e, 'danger')
        else:
            db.session.commit()
            flash('Resources allocated.', 'success')
            return redirect(url_for('.view_event', event_id=event.event_id))
    return render_template('allocations/allocate.html', form=form)

# ------ CONFLICTS -------
@main.route('/conflicts')
def conflicts():
    conflicts = []
    resources = Resource.query.all()
    for r in resources:
        allocs = sorted([a.event for a in r.allocations], key=lambda x: x.start_time)
        for i in range(len(allocs)):
            for j in range(i+1, len(allocs)):
                a = allocs[i]
                b = allocs[j]
                if overlaps(a.start_time, a.end_time, b.start_time, b.end_time):
                    conflicts.append({
                        'resource': r,
                        'event_a': a,
                        'event_b': b
                    })
    return render_template('conflicts.html', conflicts=conflicts)

# ------ REPORT -------
@main.route('/report', methods=['GET','POST'])
def report():
    start = request.args.get('start')
    end = request.args.get('end')
    results = []
    if start and end:
        try:
            s = datetime.fromisoformat(start)
            e = datetime.fromisoformat(end)
            resources = Resource.query.all()
            for r in resources:
                total_hours = 0.0
                upcoming = []
                for alloc in r.allocations:
                    ev = alloc.event
                    # consider only events that intersect [s,e]
                    if overlaps(ev.start_time, ev.end_time, s, e):
                        # compute overlap duration
                        overlap_start = max(ev.start_time, s)
                        overlap_end = min(ev.end_time, e)
                        hours = (overlap_end - overlap_start).total_seconds() / 3600.0
                        total_hours += hours
                    if ev.start_time >= datetime.now():
                        upcoming.append(ev)
                results.append({
                    'resource': r,
                    'total_hours': round(total_hours,2),
                    'upcoming': sorted(upcoming, key=lambda x: x.start_time)
                })
        except Exception as ex:
            flash('Invalid date format. Use ISO format: YYYY-MM-DDTHH:MM', 'danger')
    return render_template('report.html', results=results, start=start, end=end)

# ------ SAMPLE DATA LOADER -------
@main.route('/load_sample')
def load_sample():
    # clear existing
    EventResourceAllocation.query.delete()
    Event.query.delete()
    Resource.query.delete()
    db.session.commit()
    # create resources
    r1 = Resource(resource_name='Room 101', resource_type='room')
    r2 = Resource(resource_name='Instructor Alice', resource_type='instructor')
    r3 = Resource(resource_name='Projector X1', resource_type='equipment')
    db.session.add_all([r1,r2,r3])
    db.session.commit()
    # create events with overlaps
    now = datetime.now().replace(microsecond=0)
    e1 = Event(title='Morning Workshop', start_time=now.replace(hour=9, minute=0), end_time=now.replace(hour=11, minute=0), description='Intro workshop')
    e2 = Event(title='Intro Lecture', start_time=now.replace(hour=10, minute=30), end_time=now.replace(hour=12, minute=0), description='Lecture that overlaps with workshop')
    e3 = Event(title='Afternoon Lab', start_time=now.replace(hour=13, minute=0), end_time=now.replace(hour=15, minute=0), description='Lab session')
    e4 = Event(title='Quick Meeting', start_time=now.replace(hour=10, minute=0), end_time=now.replace(hour=10, minute=15), description='Short meeting inside overlap')
    db.session.add_all([e1,e2,e3,e4])
    db.session.commit()
    # allocate resources (some will create conflicts if attempted)
    a1 = EventResourceAllocation(event_id=e1.event_id, resource_id=r1.resource_id)
    a2 = EventResourceAllocation(event_id=e1.event_id, resource_id=r2.resource_id)
    a3 = EventResourceAllocation(event_id=e2.event_id, resource_id=r2.resource_id)  # conflict with e1 on instructor
    a4 = EventResourceAllocation(event_id=e3.event_id, resource_id=r3.resource_id)
    db.session.add_all([a1,a2,a3,a4])
    db.session.commit()
    flash('Sample data loaded. Created 3 resources and 4 events with some overlapping allocations.', 'success')
    return redirect(url_for('.index'))
