from . import db

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    allocations = db.relationship('EventResourceAllocation', backref='event', cascade="all,delete-orphan")

    def duration_hours(self):
        return (self.end_time - self.start_time).total_seconds() / 3600.0

class Resource(db.Model):
    resource_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(200), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)
    allocations = db.relationship('EventResourceAllocation', backref='resource', cascade="all,delete-orphan")

class EventResourceAllocation(db.Model):
    allocation_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.resource_id'), nullable=False)
