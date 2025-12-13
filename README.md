

**Student Name:** Linah Fathima
**Student ID:** M01086284
**Course:** CST1510 – CW2 – Multi-Domain Intelligence Platform

---

# Week 7: Secure Authentication System

## Project Description

This project implements a **secure command-line authentication system** using modern password security practices.
The system allows users to **register accounts** and **log in securely** without storing plaintext passwords.

The focus of this implementation is on **security, validation, and safe credential handling**, forming the foundation for later integration into the Multi-Domain Intelligence Platform.

---

## Features

- Secure password hashing using **bcrypt** with automatic salt generation
- User registration with **duplicate username prevention**
- User login with **hashed password verification**
- Input validation for usernames and passwords
- File-based user data persistence

---

## Technical Implementation

- **Hashing Algorithm:** bcrypt with automatic salting
- **Data Storage:** Plain text file (`users.txt`) using comma-separated values
- **Password Security:** One-way hashing (no plaintext password storage)
- **Validation Rules:**
  - Username: 3–20 characters, alphanumeric only
  - Password: 6–50 characters, minimum strength enforced

---

## Security Considerations

- Passwords are **never stored or displayed in plaintext**
- Each password is hashed with a **unique salt**
- Login attempts verify hashed values only
- Prevents common vulnerabilities such as:
  - Password reuse exposure
  - Plaintext credential leaks

---

## How to Run

1. Ensure Python is installed
2. Install required dependency:
   ```bash
   pip install bcrypt
---

# Week 8: SQL Data Pipeline and CRUD Operations

## Project Description

This project implements a **relational SQL data layer** with a complete **data pipeline and CRUD functionality** for the Multi-Domain Intelligence Platform.

The system connects Python applications to a SQLite database, creates domain-specific tables, loads data from CSV files, and provides reusable CRUD operations for multiple intelligence domains.

---

## Core Components

### 1. Database Connection (`db.py`)

A centralized database connection module ensures:
- Consistent database access
- Proper connection handling
- Reusability across the application

**Responsibilities:**
- Establish SQLite connection
- Return active connection object
- Define database file location

---

### 2. Database Schema Creation

The database schema is designed to support **multi-domain intelligence data**, including:

#### Tables Created
- `users`
- `cyber_incidents`
- `datasets_metadata`
- `it_tickets`

Each table includes:
- Primary key (`id`)
- Relevant domain attributes
- Timestamp/date fields for auditing
- Proper data types and constraints

---

## Data Pipeline Implementation

### CSV to SQL Pipeline (`csvfile.py`)

This module handles bulk data ingestion:

**Pipeline Flow:**
1. Load CSV files using Pandas
2. Validate column structure
3. Insert data into SQL tables
4. Prevent duplicate inserts when tables are already populated

This enables rapid initialization of the database with sample data.

---

## CRUD Modules by Domain

Each domain has its **own Python module** responsible for database operations.

---

### 3. Cyber Incidents Module (`incidents.py`)

**Purpose:** Manage cybersecurity incidents

**Implemented Functions:**
- `get_all_incidents()` – Retrieve all incident records
- `insert_incident()` – Add a new cyber incident
- `update_incident_status()` – Modify incident status
- `delete_incident()` – Remove an incident

**Key Fields:**
- Timestamp
- Category
- Severity
- Status
- Description
- Reported by

---

### 4. Datasets Metadata Module (`datasets.py`)

**Purpose:** Manage data science datasets

**Implemented Functions:**
- `get_all_datasets()` – Fetch dataset metadata
- `insert_datasets()` – Add new dataset information
- `update_dataset_category()` – Update dataset classification
- `delete_dataset()` – Remove dataset records

**Key Fields:**
- Dataset name
- Category
- Source
- Record count
- File size
- Created / last updated dates

---

### 5. IT Tickets Module (`tickets.py`)

**Purpose:** Manage IT operations tickets

**Implemented Functions:**
- `get_all_tickets()` – Retrieve ticket data
- `insert_tickets()` – Create new IT tickets
- `update_tickets_status()` – Update ticket resolution status
- `delete_ticket()` – Delete tickets

**Key Fields:**
- Priority
- Status
- Assigned technician
- Resolution time
- Created timestamp

---

## SQL & Security Practices

- Uses **parameterized SQL queries**
- Prevents SQL injection attacks
- Enforces controlled database access
- Ensures clean separation of concerns

---

## Technology Stack

- **Language:** Python
- **Database:** SQLite
- **Libraries:** `sqlite3`, `pandas`
- **Data Source:** CSV files
- **Architecture:** Modular data access layer

---

## How to Run

1. Ensure Python is installed
2. Install required dependencies:
   ```bash
   pip install pandas
   pip install sqlite3

---

# Week 9: Streamlit Web Application

## Project Description

A web-based dashboard built using Streamlit to provide an interactive interface for the Multi-Domain Intelligence Platform.
The application connects to an SQL database and allows users to view, manage, and analyse data across Cybersecurity, Data Science, and IT Operations domains using role-based access control.

## Features

- Streamlit multipage web application
- User authentication with session management
- Role-based access control (User, Analyst, Admin)
- Interactive dashboards with tables and charts
- Secure CRUD operations based on user role
- AI-assisted querying for database insights
- Automatic page navigation using Streamlit sidebar

## Technical Implementation

- Frontend Framework: Streamlit
- Page Structure: Streamlit auto multipage system (`pages/` folder)
- State Management: `st.session_state`
- Data Handling: Pandas DataFrames
- Visualisation: `st.dataframe`, `st.bar_chart`, `st.area_chart`
- Database: SQLite accessed via Python

## Role Permissions

- User: View dashboards and ask AI questions
- Analyst: CRUD access for Datasets and IT Tickets
- Admin: Full CRUD access across all domains

## Pages Implemented

- Cybersecurity Dashboard
- Data Science Dashboard
- IT Operations Dashboard

Each page displays live data from the database and provides domain-specific visualisation and AI-assisted analysis.

## Learning Outcomes

- Developing interactive web applications with Streamlit
- Implementing session-based authentication
- Applying role-based access control
- Connecting SQL databases to a frontend
- Designing user-friendly dashboards



## How to Run


1. Ensure Python is installed
2. Install required dependencies:
   ```bash
   pip install pandas
   pip install streamlit


---

# Week 10: API Integration using GROQ

## Project Description
A Streamlit interface integrating external APIs using **GROQ** queries and LLMs.  
This system allows users to ask questions to AI assistants in multiple domains (Cybersecurity, Data Science, IT Operations), with context from recent datasets, tickets, or incidents.

## Features
- AI-assisted querying using GROQ and LLMs
- Multi-domain support: Cybersecurity, Data Science, IT Operations
- Dynamic display of AI responses in Streamlit
- Uses database/table context (DataFrames) for more accurate answers
- Interactive sidebar and input fields for domain-specific questions

## Technical Implementation
- **API Integration**: `groq.Client` with `GENAI_API_KEY` stored in `.env`
- **LLM Interaction**: `meta-llama/llama-4-scout-17b-16e-instruct` for chat completions
- **Context Handling**: Fetch recent rows from DataFrames (`get_all_incidents`, `get_all_datasets`, `get_all_tickets`) as context
- **Streamlit UI**: Multiple `text_input` and buttons for domain-specific AI queries
- **Error Handling**: Validates environment variables and callable table functions

---
# Week 11: Project Refactor to Object-Oriented Programming (OOP)
Student Name: [Your Name]  
Student ID: [Your Student_ID]  
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
A full refactor of the Multi-Domain Intelligence Platform into **Object-Oriented Programming (OOP)**.  
This refactor improves code modularity, maintainability, and scalability by encapsulating logic into classes and methods.

## Features
- Modular class-based architecture for each domain (Cybersecurity, Data Science, IT Operations)
- Encapsulation of AI query handling in `AIQueryManager`
- Database/table interactions encapsulated in manager classes (`IncidentManager`, `DatasetManager`, `TicketManager`)
- Streamlit UI refactored to use class instances for all actions
- Easy to extend: adding new features or domains requires minimal code changes
- Cleaner and more maintainable project structure

## Technical Implementation
- **OOP Design**: Each major module is now a class with methods for functionality
- **AI Query Handling**: `AIQueryManager` handles API requests and context-aware queries
- **Data Managers**: Separate manager classes handle data fetching, updating, and context for AI
- **Streamlit UI**: Uses instances of classes for displaying data and handling user interactions
- **Error Handling**: Centralized in methods for validation and API calls
- **File Structure**:

---


# Week 11: Project Refactor to Object-Oriented Programming (OOP

## Project Description
A full refactor of the Multi-Domain Intelligence Platform into **Object-Oriented Programming (OOP)**.  
This refactor improves code modularity, maintainability, and scalability by encapsulating logic into classes and methods.

## Features
- Modular class-based architecture for each domain (Cybersecurity, Data Science, IT Operations)
- Encapsulation of AI query handling in `AIQueryManager`
- Database/table interactions encapsulated in manager classes (`IncidentManager`, `DatasetManager`, `TicketManager`)
- Streamlit UI refactored to use class instances for all actions
- Easy to extend: adding new features or domains requires minimal code changes
- Cleaner and more maintainable project structure

## Technical Implementation
- **OOP Design**: Each major module is now a class with methods for functionality
- **AI Query Handling**: `AIQueryManager` handles API requests and context-aware queries
- **Data Managers**: Separate manager classes handle data fetching, updating, and context for AI
- **Streamlit UI**: Uses instances of classes for displaying data and handling user interactions
- **Error Handling**: Centralized in methods for validation and API calls
- **File Structure**:
