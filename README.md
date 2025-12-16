# Event Scheduling & Resource Allocation System (Flask)

## Overview
A small Flask web application to create events, resources, allocate resources,
detect conflicts, and produce a utilisation report.

## Features
- CRUD for Events and Resources
- Allocate resources to events
- Conflict detection (prevents double-booking)
- Conflict listing view
- Resource utilisation report by date range
- Sample data loader (creates 3 resources and 4 events with overlaps)

## Setup (local)
1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / macOS
   venv\Scripts\activate   # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize and run:
   ```bash
   python run.py
   ```

4. App will run at `http://127.0.0.1:5000/`

## Sample data
To load sample data, visit `/load_sample` route in the app after starting it.

## What to submit
- Push this repository to GitHub
- Include screenshots and a short screen recording showing features
- Email per assignment instructions

## Notes
- Date-time inputs use HTML `datetime-local`. Browser will send local datetime without timezone.
- Conflict detection logic treats overlapping intervals as conflicts when:
  `(start1 < end2) and (start2 < end1)`
