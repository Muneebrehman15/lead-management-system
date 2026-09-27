# Lead Management System

A Streamlit-based lead management system for **Prime Properties Karachi**, a fictional real-estate company. The application helps a sales team record property inquiries, track progress, manage follow-ups, and review pipeline activity from a single dashboard.

## Live Demo

[Open the Prime Properties Karachi demo](https://lead-management-system-e2gseiuziyovbhqjshyxzc.streamlit.app/)

## Problem This System Solves

Real-estate inquiries can become difficult to manage when client details, property requirements, contact history, and follow-up dates are spread across messages or spreadsheets.

This system provides a central workspace to:

- Store lead and client information
- Track each lead through the sales process
- Identify leads that need attention
- Schedule and review follow-ups
- Understand lead sources, locations, and status distribution
- Export filtered lead data for further use

## Main Features

- **Lead management:** Store client details, contact information, property requirements, budget, location, source, notes, and contact dates.
- **Add, edit, and delete leads:** Create new inquiries, update existing records, or permanently delete a selected lead.
- **Lead status tracking:** Track leads through New, Contacted, Site Visit, Negotiation, Converted, and Lost statuses.
- **Dynamic lead priority:** Calculate High, Medium, or Low priority from the current status, budget, and follow-up date. Converted and Lost leads are always treated as Low priority.
- **Search and filtering:** Search by name, phone, or notes and filter by status, location, source, and priority.
- **Follow-up management:** Separate due or overdue follow-ups from upcoming follow-ups for active leads.
- **Dashboard and KPIs:** View total leads, open leads, converted leads, follow-ups due, open pipeline value, and priority counts.
- **Charts and analytics:** Review leads by status, source, and Karachi location using interactive Plotly charts.
- **CSV export:** Download the currently filtered lead list as a CSV file.

## Application Workflow

1. Open the dashboard to review pipeline KPIs, priority counts, charts, and follow-ups requiring attention.
2. Use **Add Lead** to record a new property inquiry.
3. Select a property type, location, budget, status, source, and contact dates.
4. Optionally schedule the next follow-up and add notes.
5. Use **All Leads** to search, filter, export, edit, or delete records.
6. Use the dashboard priority selector or the Priority filter to find High, Medium, or Low priority leads.
7. Use **Follow-ups** to review due, overdue, and upcoming client contacts.
8. Update lead status and follow-up dates as the sales conversation progresses.

## Technology Stack

- **Python**
- **Streamlit** for the web application interface
- **SQLite** for local data storage
- **Pandas** for tabular data processing
- **Plotly Express** for interactive charts and analytics

## Project Structure

```text
lead management system/
├── app.py            # Streamlit interface, dashboard, forms, filters, charts, and priority logic
├── database.py       # SQLite connection, schema creation, CRUD operations, follow-ups, and sample data
├── requirements.txt  # Python dependencies
├── leads.db          # Local SQLite database created and used by the application
├── .gitignore        # Ignored local files such as databases, virtual environments, and cache files
└── README.md         # Project documentation
```

## Run Locally

### 1. Clone or download the project

Open a terminal in the project directory:

```powershell
cd "lead management system"
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start the application

```powershell
streamlit run app.py
```

Streamlit will display a local URL, usually `http://localhost:8501`. Open that URL in a browser.

## Data and Demo Scope

This is a **portfolio and client-demo application** for the fictional company Prime Properties Karachi. It uses fictional sample lead data when the local database is empty. The application stores data in the local `leads.db` SQLite file and is not intended to represent a production deployment, secure multi-user CRM, or live real-estate database.
