#**Output**

<img width="1920" height="1080" alt="Screenshot (39)" src="https://github.com/user-attachments/assets/180fcce6-0865-4b6c-8416-42358245bd25" />
<img width="1920" height="1080" alt="Screenshot (40)" src="https://github.com/user-attachments/assets/1d370d71-6bd9-4442-89d4-19edb5a6b124" />
<img width="1920" height="1080" alt="Screenshot (41)" src="https://github.com/user-attachments/assets/90df14ef-5e24-4732-ab84-7f3bce186ab1" />
<img width="1920" height="1080" alt="Screenshot (42)" src="https://github.com/user-attachments/assets/e290315e-5921-47d9-bc00-1108569e4847" />
<img width="1920" height="1080" alt="Screenshot (43)" src="https://github.com/user-attachments/assets/9ecdcd12-0152-475c-bb84-06c769509806" />
<img width="1920" height="1080" alt="Screenshot (44)" src="https://github.com/user-attachments/assets/e38b203e-180f-4c71-8ecd-86e432b59bc5" />
<img width="1920" height="1080" alt="Screenshot (45)" src="https://github.com/user-attachments/assets/547bea0d-a971-411a-a099-ec2316826c16" />
<img width="1920" height="1080" alt="Screenshot (46)" src="https://github.com/user-attachments/assets/72dae2a4-f105-4499-a338-a7d10e49b1d7" />

# Drive Link - 
https://drive.google.com/file/d/1124j8V3ejzhqzqV1pDAWW2FHBhH25vBR/view?usp=sharing

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
