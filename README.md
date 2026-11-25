# Data Redundancy Removal System

## Project Overview
The Data Redundancy Removal System is a web-based application developed using Python and Flask. It helps maintain accurate database records by detecting duplicate entries before they are saved.

## Project Objectives
- Identify duplicate records.
- Validate new records before saving.
- Prevent duplicate data from entering the database.
- Maintain accurate and reliable records.
- Reduce unnecessary data redundancy.

## Features
- Add new records using a web form.
- Validate names, email addresses and phone numbers.
- Detect duplicate records using SHA-256 fingerprints.
- Identify similar names for manual review.
- Store verified records in an SQLite database.
- Display saved records.

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS
- SHA-256 Hashing

## Installation and Setup

1. Clone this repository:

   `git clone https://github.com/Danittoboy/CodeAlpha_Data_Redundancy_Removal_System.git`

2. Install the required dependencies:

   `pip install -r requirements.txt`

3. Run the application:

   `python app.py`

4. Open your browser and visit:

   `http://127.0.0.1:5000`

## How It Works
The system validates submitted records and generates a unique SHA-256 fingerprint using the normalized name and email address.

If the fingerprint already exists, the system identifies the entry as a duplicate and prevents it from being saved.

Similar names with different email addresses are flagged for review instead of automatically being rejected.

## Health Check
Visit `/health` to check whether the application is running.

## Project Status
Developed as part of the CodeAlpha Cloud Computing Internship.

## Author
CodeAlpha Internship Project
