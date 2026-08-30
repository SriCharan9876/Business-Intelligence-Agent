"# Business-Intelligence-Agent" 
# Skylark Drones Business Intelligence Agent

## Overview

This project is a conversational Business Intelligence Agent built for the Skylark Drones technical assignment.

The agent allows founders and executives to ask natural-language questions about sales pipeline and operational performance. It retrieves live data from monday.com, cleans and normalizes inconsistent records, performs deterministic analytics, and generates concise business insights.

The application integrates two monday.com boards:

* **Deals** — Sales pipeline and deal information
* **Work Orders** — Project execution and operational information

The system is designed to handle messy and incomplete business data and communicate relevant data-quality limitations when they affect the analysis.

---

# Architecture

## High-Level Architecture

```text
┌─────────────────────────────────────────────┐
│                 User / Founder              │
│                                             │
│   "How is the Energy pipeline this quarter?"│
└───────────────────────┬─────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────┐
│              React Frontend                 │
│                                             │
│  Conversational Chat Interface              │
└───────────────────────┬─────────────────────┘
                        │
                        │ REST API
                        │ POST /api/chat
                        ▼
┌─────────────────────────────────────────────┐
│               FastAPI Backend               │
│                                             │
│               BI Agent                      │
└───────────────────────┬─────────────────────┘
                        │
          ┌─────────────┼──────────────┐
          ▼             ▼              ▼
┌────────────────┐ ┌─────────────┐ ┌────────────────┐
│ Query          │ │ Analytics   │ │ Data           │
│ Understanding  │ │ Engine      │ │ Quality Layer  │
│                │ │             │ │                │
│ Gemini         │ │ Pandas      │ │ Normalization  │
└───────┬────────┘ └──────┬──────┘ └──────┬─────────┘
        │                 │               │
        └─────────────────┼───────────────┘
                          │
                          ▼
             ┌────────────────────────┐
             │ monday.com Integration │
             │                        │
             │ GraphQL API - Read Only│
             └────────────┬───────────┘
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
        ┌────────────────┐ ┌────────────────┐
        │ Deals Board    │ │ Work Orders    │
        │                │ │ Board          │
        └────────────────┘ └────────────────┘
```

---

# Architecture Principles

The application separates responsibilities between the AI model, analytics layer, and data source.

```text
Gemini
  ↓
Understands the business question
  ↓
FastAPI Agent
  ↓
Selects required data and analysis
  ↓
monday.com
  ↓
Provides live board data
  ↓
Data Cleaning Layer
  ↓
Normalizes messy records
  ↓
Pandas Analytics
  ↓
Performs deterministic calculations
  ↓
Gemini
  ↓
Converts results into executive insights
```

This design ensures that the AI model does not independently calculate business metrics.

### Responsibility Separation

| Component    | Responsibility                             |
| ------------ | ------------------------------------------ |
| React        | Conversational user interface              |
| FastAPI      | API and agent orchestration                |
| monday.com   | Source of business data                    |
| Data Cleaner | Data normalization and validation          |
| Pandas       | Business calculations and analytics        |
| Gemini       | Query understanding and insight generation |

---

# Data Flow

For a question such as:

> How is the Energy sector pipeline this quarter?

The system performs the following workflow.

```text
1. User enters question in React
          ↓
2. React sends POST /api/chat
          ↓
3. FastAPI receives the question
          ↓
4. Gemini extracts structured intent

   {
     "intent": "pipeline_analysis",
     "sector": "Energy",
     "time_period": "current_quarter"
   }

          ↓
5. BI Agent determines that the Deals board is required
          ↓
6. monday.com API retrieves current board data
          ↓
7. Data Cleaner normalizes:
   - sectors
   - dates
   - numeric values
   - missing values
          ↓
8. Pandas calculates:
   - total pipeline
   - number of deals
   - average deal value
   - pipeline by stage
          ↓
9. Gemini generates an executive-friendly explanation
          ↓
10. FastAPI returns the response
          ↓
11. React displays the result
```

---

# Project Structure

```text
skylark-bi-agent/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── main.py
│   │   │   FastAPI application entry point
│   │   │
│   │   ├── config.py
│   │   │   Environment configuration
│   │   │
│   │   ├── schemas.py
│   │   │   Request and response models
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── chat.py
│   │   │       Chat API endpoint
│   │   │
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   └── bi_agent.py
│   │   │       Orchestrates the BI workflow
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── monday_client.py
│   │   │   │   monday.com API integration
│   │   │   │
│   │   │   ├── data_cleaner.py
│   │   │   │   Data normalization
│   │   │   │
│   │   │   ├── analytics_service.py
│   │   │   │   Pandas analytics
│   │   │   │
│   │   │   └── llm_service.py
│   │   │       Gemini integration
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── dates.py
│   │           Date and quarter utilities
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   └── SuggestedQuestions.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── Decision_Log.md
```

---

# Technology Stack

## Frontend

* React
* Vite
* Axios

## Backend

* Python
* FastAPI
* Uvicorn

## Data Processing

* Pandas

## AI

* Google Gemini API

Gemini is used for:

* Understanding natural-language business questions
* Extracting structured query intent
* Generating executive-friendly business insights

## Business Data Source

* monday.com
* GraphQL API
* Read-only access

---

# monday.com Configuration

## 1. Create monday.com Boards

Create two separate boards:

```text
Deals
Work Orders
```

The two boards should be populated using the provided assignment datasets.

---

## 2. Import Deals Dataset

Import:

```text
Deal funnel Data.xlsx
```

Recommended important columns include:

| Dataset Field        | Recommended Type  |
| -------------------- | ----------------- |
| Deal Name            | Item Name         |
| Owner code           | Text              |
| Client Code          | Text              |
| Deal Status          | Status            |
| Close Date           | Date              |
| Closure Probability  | Status or Numbers |
| Deal Value           | Numbers           |
| Tentative Close Date | Date              |
| Deal Stage           | Status            |
| Product Deal         | Text              |
| Sector/Service       | Dropdown/Text     |
| Created Date         | Date              |

The exact monday.com column names should match the configured dataset fields used by the backend.

---

## 3. Import Work Orders Dataset

Import:

```text
Work_Order_Tracker Data.xlsx
```

Important fields include:

| Dataset Field          | Recommended Type |
| ---------------------- | ---------------- |
| Work Order / Deal Name | Item Name        |
| Customer               | Text             |
| Nature of Work         | Text/Dropdown    |
| Execution Status       | Status           |
| Data Delivery Date     | Date             |
| Probable Start Date    | Date             |
| Probable End Date      | Date             |
| Sector                 | Dropdown/Text    |
| Work Order Value       | Numbers          |
| Billed Value           | Numbers          |
| Collected Amount       | Numbers          |
| Amount Receivable      | Numbers          |
| Billing Status         | Status           |
| Collection Status      | Status           |

---

# monday.com API Configuration

## Generate API Token

Create a monday.com API token from the monday.com developer/account settings.

Store the token in the backend `.env` file.

Do not commit the API token to source control.

---

## Find Board IDs

The board ID can be found in the monday.com board URL.

Example:

```text
https://your-account.monday.com/boards/1234567890
```

The board ID is:

```text
1234567890
```

---

# Environment Configuration

Create:

```text
backend/.env
```

Example:

```env
MONDAY_API_TOKEN=your_monday_api_token

DEALS_BOARD_ID=your_deals_board_id

WORK_ORDERS_BOARD_ID=your_work_orders_board_id

GEMINI_API_KEY=your_gemini_api_key

FRONTEND_URL=http://localhost:5173
```

A `.env.example` file should be committed instead of the actual `.env` file.

---

# Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it.

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

# Supported Business Queries

The prototype supports questions in the following categories.

## Sales Pipeline

Examples:

```text
How is our pipeline looking overall?

How is the Energy sector pipeline?

What is our pipeline this quarter?

What is the average deal value?
```

---

## Work Order Performance

Examples:

```text
How many work orders are completed?

What is our work order completion rate?

How are work orders performing in the Energy sector?

What is the total work order value?
```

---

## Cross-Board Analysis

Examples:

```text
Compare pipeline and work order value by sector.

Which sectors have the strongest sales and execution activity?

Compare sales opportunities with operational work by sector.
```

---

## Leadership Updates

Example:

```text
Prepare a leadership update.
```

The agent combines relevant sales and operational information and provides an executive summary covering:

* Pipeline
* Operational performance
* Sector insights
* Risks
* Data quality caveats

---

# Data Resilience

The datasets contain real-world inconsistencies and incomplete records.

The backend performs data normalization before calculations.

The system handles:

* Missing values
* Invalid dates
* Inconsistent date formats
* Currency symbols
* Comma-separated numbers
* Numeric values stored as text
* Text capitalization differences
* Inconsistent sector naming

Where missing data materially affects a calculation, the agent can communicate the limitation in the response.

Example:

> The average deal value was calculated using records with valid deal values. Records with missing values were excluded from the average calculation.

---

# monday.com Integration Design

The application uses monday.com as the dynamic source of truth.

```text
User Question
      ↓
FastAPI BI Agent
      ↓
monday.com GraphQL API
      ↓
Retrieve Board Items
      ↓
Convert to DataFrame
      ↓
Normalize Data
      ↓
Perform Analytics
      ↓
Generate Response
```

The application does not use hardcoded CSV records for business analysis.

The original Excel files are used only for the initial monday.com board setup.

---

# Error Handling

The application handles several categories of errors.

## monday.com API Errors

Examples:

* Invalid API token
* Board not found
* API timeout
* Invalid GraphQL response

## Data Errors

Examples:

* Missing deal values
* Invalid dates
* Missing sector values
* Numeric conversion errors

## AI Errors

Examples:

* Gemini API quota issues
* Invalid structured response
* Unsupported query classification

The backend should return a user-friendly error message rather than exposing internal exceptions.

---

# Key Design Decision

The application deliberately separates language intelligence from numerical calculations.

```text
Gemini
    ↓
Understands Question

Pandas
    ↓
Calculates Metrics

Gemini
    ↓
Explains Results
```

This approach improves reliability by preventing the language model from independently calculating business metrics.

---

# Future Improvements

With additional development time, the following improvements would be added:

* Support for monday.com pagination
* Intelligent API caching
* Follow-up conversation context
* More flexible query planning
* Automated column mapping
* Data-quality scoring
* Visual charts and tables
* Automated tests
* Structured logging and monitoring
* Production authentication

---

# Submission Contents

The submission contains:

* Hosted prototype
* Source code
* README.md
* Decision_Log.md

The prototype is designed to demonstrate dynamic monday.com integration, resilient data processing, conversational query understanding, deterministic business analytics, and executive-level business insights.
