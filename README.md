# Skylark Drones – Monday.com Business Intelligence Agent

## Overview

This project is an AI-powered Business Intelligence Agent built for the Skylark Drones technical assignment.

The agent enables founders and executives to ask business questions conversationally and receive data-driven insights from two monday.com boards:

* **Deal Funnel** – Sales pipeline and opportunity data
* **Work Order Tracker** – Project execution, billing, collection, and receivables data

The system dynamically fetches data from monday.com, cleans inconsistent and missing values, performs deterministic business calculations, and uses Google Gemini to understand business questions and generate executive-friendly responses.

The application does **not hardcode the CSV/Excel data**. The source data is queried dynamically from monday.com at runtime.

---

# Problem Statement

Founders and executives often need answers to questions such as:

* How is our pipeline looking this quarter?
* How many new opportunities were created this month?
* Which sector has the highest pipeline?
* What is our outstanding receivable amount?
* How is project execution performing?
* How much has been billed versus collected?
* Give me a leadership update.

Answering these questions manually requires:

1. Opening multiple monday.com boards.
2. Extracting data.
3. Cleaning inconsistent values.
4. Handling missing fields.
5. Combining sales and operational information.
6. Performing calculations.
7. Interpreting the results.

This project automates that workflow using an AI-powered conversational interface.

---

# Features

## 1. Conversational Business Intelligence

Users can ask natural language questions such as:

```text
How is our pipeline looking this quarter?
```

```text
How many new opportunities were created this month?
```

```text
Which sector has the highest pipeline?
```

```text
What is our collection rate?
```

```text
Give me a leadership update.
```

The AI agent interprets the question, determines the required dataset, performs the relevant analysis, and generates an executive-friendly response.

---

## 2. Monday.com Integration

The application integrates with monday.com using the monday.com GraphQL API.

The integration is read-only.

The backend dynamically fetches:

* Board metadata
* Column definitions
* Column IDs
* Column titles
* Board items
* Item values

The application maps monday.com column IDs to their visible column titles.

Example:

```text
Monday API Response

Column ID: numbers9
Column Title: Masked Deal value

↓

Backend Row

{
    "Masked Deal value": "500000"
}
```

This allows the analytics layer to work with meaningful dataset column names instead of internal monday.com column IDs.

---

## 3. Dynamic Data Access

The project does not load the original Excel or CSV files during analysis.

Instead:

```text
User Question
      ↓
FastAPI Backend
      ↓
Monday.com API
      ↓
Current Board Data
      ↓
Data Cleaning
      ↓
Business Analytics
      ↓
Gemini Response Generation
      ↓
User
```

This ensures the agent analyzes the latest available data from monday.com.

---

# System Architecture

```text
                         ┌─────────────────────┐
                         │     React Frontend  │
                         │                     │
                         │ Conversational Chat │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP Request
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend   │
                         │                     │
                         │      API Layer      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      BI Agent       │
                         │                     │
                         │ Query Orchestration │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │  Gemini Service │    │ Monday Service  │    │ Analytics       │
    │                 │    │                 │    │ Service         │
    │ Query Intent    │    │ Dynamic Board   │    │ Deterministic   │
    │ Understanding   │    │ Data Retrieval  │    │ Calculations    │
    └─────────────────┘    └────────┬────────┘    └────────┬────────┘
                                     │                      │
                                     ▼                      │
                            ┌─────────────────┐             │
                            │   monday.com    │             │
                            │                 │             │
                            │  Deals Board    │             │
                            │  Work Orders    │             │
                            └─────────────────┘             │
                                                            │
                                     ┌──────────────────────┘
                                     ▼
                            ┌─────────────────┐
                            │ Data Cleaner    │
                            │                 │
                            │ Dates           │
                            │ Numbers         │
                            │ Missing Values  │
                            │ Categories      │
                            └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │ Gemini Service  │
                            │                 │
                            │ Executive       │
                            │ Explanation     │
                            └────────┬────────┘
                                     │
                                     ▼
                              Final Response
```

---

# Architecture Design

The system separates AI reasoning from numerical calculations.

## Gemini Responsibilities

Gemini is responsible for:

* Understanding natural language questions
* Identifying user intent
* Extracting filters
* Identifying relevant datasets
* Generating executive-friendly explanations

Example:

```text
Question:

How many new opportunities were created this month?

↓

Gemini Output:

{
    "intent": "opportunity_generation",
    "sector": null,
    "time_period": "current_month",
    "needs_deals": true,
    "needs_work_orders": false
}
```

---

## Python Analytics Responsibilities

Python is responsible for:

* Filtering datasets
* Date calculations
* Aggregations
* Revenue calculations
* Pipeline calculations
* Collection calculations
* Receivable calculations
* Counting records
* Percentage calculations

Example:

```text
Created Date
     ↓
Filter current month
     ↓
Count records
     ↓
New opportunities count
```

This design prevents the LLM from inventing or incorrectly calculating business metrics.

---

# Dataset Schema

The project uses two datasets.

---

## 1. Deal Funnel

The Deal Funnel dataset represents the sales pipeline.

Key fields include:

| Column               | Type     | Business Purpose          |
| -------------------- | -------- | ------------------------- |
| Deal Name            | Text     | Opportunity identifier    |
| Owner code           | Text     | Deal owner                |
| Client Code          | Text     | Client identifier         |
| Deal Status          | Category | Open, Won, Dead, etc.     |
| Close Date (A)       | Date     | Actual close date         |
| Closure Probability  | Category | Probability of closing    |
| Masked Deal value    | Numeric  | Potential deal value      |
| Tentative Close Date | Date     | Expected closing date     |
| Deal Stage           | Category | Sales funnel stage        |
| Product deal         | Text     | Product or service        |
| Sector/service       | Category | Industry sector           |
| Created Date         | Date     | Opportunity creation date |

### Business Questions Supported

Examples:

```text
What is the total pipeline?
```

```text
How many new opportunities were created this month?
```

```text
Which sector has the highest pipeline?
```

```text
How is the pipeline distributed across deal stages?
```

```text
What opportunities are expected to close this quarter?
```

---

# 2. Work Order Tracker

The Work Order Tracker represents project execution and financial performance after business has been secured.

Key business fields include:

| Column                                  | Type     | Business Purpose            |
| --------------------------------------- | -------- | --------------------------- |
| Deal name masked                        | Text     | Deal reference              |
| Customer Name Code                      | Text     | Customer identifier         |
| Serial #                                | Text     | Work order reference        |
| Nature of Work                          | Category | Type of engagement          |
| Execution Status                        | Category | Project execution status    |
| Data Delivery Date                      | Date     | Deliverable date            |
| Date of PO/LOI                          | Date     | Purchase order date         |
| Probable Start Date                     | Date     | Expected start              |
| Probable End Date                       | Date     | Expected completion         |
| Sector                                  | Category | Industry sector             |
| Type of Work                            | Category | Operational service         |
| Amount in Rupees (Incl of GST) (Masked) | Numeric  | Work order value            |
| Billed Value                            | Numeric  | Amount invoiced             |
| Collected Amount                        | Numeric  | Amount collected            |
| Amount to be billed                     | Numeric  | Remaining billing           |
| Amount Receivable                       | Numeric  | Outstanding receivables     |
| Invoice Status                          | Category | Invoice progress            |
| Collection status                       | Category | Payment collection progress |
| Billing Status                          | Category | Billing progress            |

### Business Questions Supported

Examples:

```text
What is our collection rate?
```

```text
How much is outstanding in receivables?
```

```text
How much work has been billed?
```

```text
How is project execution performing?
```

```text
Which projects are incomplete?
```

---

# Dataset Schema Layer

The application includes a dedicated schema definition file:

```text
app/dataset_schema.py
```

This file contains:

* Dataset names
* Expected column names
* Data types
* Business descriptions

The schema acts as a business metadata layer.

Architecture:

```text
dataset_schema.py
        │
        ├── Expected Columns
        ├── Data Types
        ├── Business Meaning
        │
        ▼
data_cleaner.py
        │
        ▼
llm_service.py
        │
        ▼
analytics_service.py
```

The schema is not the actual data.

The actual data is always fetched dynamically from monday.com.

---

# Data Resilience

Real-world business data can contain:

* Missing values
* Empty strings
* Numbers stored as text
* Currency symbols
* Comma separators
* Invalid dates
* Inconsistent capitalization
* Inconsistent category names
* Unexpected column names

The `data_cleaner.py` service normalizes these values before analysis.

---

## Numeric Cleaning

Example input:

```text
₹1,25,000
```

Becomes:

```text
125000
```

Invalid numeric values become:

```text
NaN
```

instead of causing the application to crash.

---

## Date Cleaning

Dates are converted using:

```python
pd.to_datetime(
    value,
    errors="coerce"
)
```

Invalid dates become:

```text
NaT
```

and are handled safely during analysis.

---

## Category Cleaning

Values such as:

```text
Mining
 mining
MINING
```

can be normalized for filtering and comparison.

---

## Missing Data

Missing data does not stop analysis.

Instead, the BI agent:

1. Continues using valid records.
2. Calculates metrics using available data.
3. Tracks missing values in important fields.
4. Includes data quality notes in the final response.

Example:

```text
Data Quality Note:

3 opportunities have missing deal values.
Pipeline totals are calculated using records with valid values.
```

---

# Project Structure

```text
project-root/
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── api.js
│   │
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│
│   ├── app/
│   │
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── schemas.py
│   │   ├── dataset_schema.py
│   │
│   │   ├── api/
│   │   │   └── chat.py
│   │
│   │   ├── agents/
│   │   │   └── bi_agent.py
│   │
│   │   └── services/
│   │       ├── monday_client.py
│   │       ├── data_cleaner.py
│   │       ├── analytics_service.py
│   │       └── llm_service.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── README.md
├── Decision_Log.md
└── .gitignore
```

---

# Backend Request Flow

The complete request lifecycle is:

```text
User
 │
 │ "How many new opportunities were created this month?"
 ▼
React Frontend
 │
 │ POST /api/chat
 ▼
FastAPI API Layer
 │
 ▼
BI Agent
 │
 ├──────────────────────────────┐
 │                              │
 ▼                              ▼
Gemini                    Monday.com
Intent Analysis           Data Fetch
 │                              │
 ▼                              ▼
Intent + Filters           Raw Records
 │                              │
 └──────────────┬───────────────┘
                │
                ▼
          Data Cleaner
                │
                ▼
         Analytics Service
                │
                ▼
       Deterministic Result
                │
                ▼
          Gemini Service
                │
                ▼
       Executive Explanation
                │
                ▼
         FastAPI Response
                │
                ▼
         React Frontend
```

---

# Example Query Flow

## User Question

```text
How many new opportunities were created this month?
```

## Step 1: Intent Understanding

Gemini identifies:

```json
{
    "intent": "opportunity_generation",
    "sector": null,
    "time_period": "current_month",
    "needs_deals": true,
    "needs_work_orders": false
}
```

---

## Step 2: Data Retrieval

The agent fetches the Deal Funnel board from monday.com.

---

## Step 3: Data Cleaning

The `Created Date` column is converted into datetime format.

---

## Step 4: Analytics

The analytics service filters:

```text
Created Date = Current Month
```

Then calculates:

```text
Number of matching opportunities
```

It may also calculate:

```text
Total value of newly created opportunities
```

---

## Step 5: Response Generation

The calculated result is passed to Gemini.

Gemini explains the result without performing new calculations or inventing metrics.

---

# Supported Intents

The BI Agent currently supports the following intent categories.

## Pipeline Analysis

Questions about:

* Total pipeline value
* Open opportunities
* Pipeline health
* Pipeline stages
* Closure probability
* Expected closing periods

Intent:

```text
pipeline_analysis
```

---

## Pipeline by Sector

Questions about:

* Sector comparison
* Highest-value sectors
* Pipeline distribution across sectors

Intent:

```text
pipeline_by_sector
```

---

## Opportunity Generation

Questions about:

* New opportunities
* Deals created
* Opportunities created this month
* New pipeline generation

Uses:

```text
Created Date
```

Intent:

```text
opportunity_generation
```

---

## Work Order Analysis

Questions about:

* Execution
* Billing
* Collection
* Receivables
* Work order performance

Intent:

```text
work_order_analysis
```

---

## Business Overview

Questions requiring both datasets.

Examples:

```text
How is the business performing overall?
```

Intent:

```text
business_overview
```

---

## Leadership Update

Provides an executive-level summary of:

* Sales pipeline
* Operations
* Billing
* Collections
* Receivables
* Data quality risks

Intent:

```text
leadership_update
```

---

# Technology Stack

## Frontend

* React
* Vite
* JavaScript
* CSS

The frontend provides the conversational interface.

---

## Backend

* Python
* FastAPI
* Pandas
* Pydantic

FastAPI handles API requests.

Pandas performs deterministic data transformation and business calculations.

---

## AI

* Google Gemini API

Gemini is used for:

* Natural language understanding
* Intent extraction
* Filter extraction
* Executive response generation

---

## Business Data Source

* monday.com GraphQL API

The application uses monday.com as the source of truth.

The integration is read-only.

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <project-folder>
```

---

# 2. Configure monday.com

Create two boards in monday.com:

```text
Deal Funnel
```

and:

```text
Work Order Tracker
```

Import the provided datasets into their respective boards.

Configure the column types appropriately.

Recommended column types:

### Deal Funnel

```text
Deal Name → Text

Owner code → Text

Client Code → Text

Deal Status → Status

Close Date (A) → Date

Closure Probability → Status / Dropdown

Masked Deal value → Numbers

Tentative Close Date → Date

Deal Stage → Status / Dropdown

Product deal → Text

Sector/service → Dropdown / Status

Created Date → Date
```

---

### Work Order Tracker

```text
Deal name masked → Text

Customer Name Code → Text

Serial # → Text

Nature of Work → Status / Dropdown

Execution Status → Status

Data Delivery Date → Date

Date of PO/LOI → Date

Probable Start Date → Date

Probable End Date → Date

Sector → Status / Dropdown

Type of Work → Status / Dropdown

Financial Values → Numbers

Invoice Status → Status

Collection status → Status

Billing Status → Status
```

---

# 3. Generate monday.com API Token

In monday.com:

1. Open the developer settings.
2. Generate a personal API token.
3. Copy the token.
4. Store it in the backend `.env` file.

Example:

```env
MONDAY_API_TOKEN=your_token
```

Never commit the token to GitHub.

---

# 4. Get monday.com Board IDs

Open each monday.com board.

Obtain the board IDs for:

```text
Deal Funnel
```

and:

```text
Work Order Tracker
```

Add them to `.env`:

```env
DEALS_BOARD_ID=123456789
WORK_ORDERS_BOARD_ID=987654321
```

---

# 5. Configure Gemini

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

---

# 6. Configure Environment Variables

Create:

```text
backend/.env
```

Example:

```env
MONDAY_API_TOKEN=your_monday_token

DEALS_BOARD_ID=your_deals_board_id

WORK_ORDERS_BOARD_ID=your_work_orders_board_id

GEMINI_API_KEY=your_gemini_api_key

FRONTEND_URL=http://localhost:5173
```

---

# 7. Backend Setup

Navigate to:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it.

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

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

The backend will run at:

```text
http://localhost:8000
```

---

# 8. Frontend Setup

Navigate to:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will typically run at:

```text
http://localhost:5173
```

---

# API

## Chat Endpoint

### Request

```http
POST /api/chat
```

Request body:

```json
{
    "message": "How is our pipeline looking this quarter?"
}
```

---

### Response

```json
{
    "answer": "Executive summary of the analysis.",
    "intent": "pipeline_analysis",
    "analysis": {
        "analysis_type": "pipeline",
        "record_count": 10,
        "total_pipeline_value": 5000000
    },
    "data_quality": [
        "2 deal records have missing values."
    ]
}
```

---

# Data Quality and Error Handling

The system is designed to handle common data problems.

## Missing Values

Missing values are safely converted to null values and excluded where necessary from calculations.

---

## Invalid Numbers

Invalid numeric values are converted using:

```python
pd.to_numeric(
    value,
    errors="coerce"
)
```

---

## Invalid Dates

Invalid dates are converted using:

```python
pd.to_datetime(
    value,
    errors="coerce"
)
```

---

## Empty Boards

If no records are returned from monday.com, the agent returns a meaningful response instead of crashing.

---

## monday.com API Failures

API errors are captured and surfaced to the backend rather than silently producing incorrect results.

---

## AI API Failures and Offline Fallback

Given that generative AI models (like Gemini) can experience rate limits (e.g., `429 RESOURCE_EXHAUSTED`) or high-demand outages, the agent includes a robust **Offline Fallback Mechanism**:

1. **Intent Parsing Fallback**: If the LLM fails to interpret the user's natural language question, the system falls back to a RegEx/keyword-based semantic parser to route the question to the correct deterministic analytics function.
2. **Response Generation Fallback**: If the LLM fails to generate the final executive explanation, the system bypasses the LLM entirely and uses a deterministic Markdown generator to present the raw structured data directly to the user.
3. **Graceful Error Display**: The frontend displays a highlighted `API Error Alert` explaining the fallback (e.g. "High demand/Rate limited") so the user understands why the response is auto-generated, while protecting internal system error stack traces from the end user.

This ensures the BI Agent remains highly available and functional even if external AI services are completely down.

---

# Security

Sensitive credentials are stored in environment variables.

The following files should not be committed:

```text
.env
```

Example `.gitignore`:

```text
.env
venv/
__pycache__/
node_modules/
dist/
```

---

# Design Decisions

## Why monday.com API Instead of Hardcoded Files?

The assignment requires the agent to query monday.com dynamically.

Using the API ensures:

* Current data is analyzed.
* The source of truth remains monday.com.
* No CSV data is hardcoded into analytics logic.

---

## Why Gemini Is Not Used for Calculations

LLMs can generate fluent explanations but are not ideal for deterministic financial calculations.

Therefore:

```text
Gemini
    ↓
Understands Question

Python/Pandas
    ↓
Calculates Metrics

Gemini
    ↓
Explains Results
```

This separation improves reliability and reduces the risk of hallucinated metrics.

---

## Why a Dedicated Dataset Schema Exists

`dataset_schema.py` provides a structured definition of:

* Available datasets
* Expected columns
* Data types
* Business meaning

This helps:

* LLM query understanding
* Data validation
* Code maintainability
* Future extension of the agent

---

# Leadership Updates

The optional requirement:

> The agent should help prepare data for leadership updates.

is implemented through the `leadership_update` intent.

The agent can summarize:

## Sales

* Pipeline value
* Pipeline stages
* Opportunity generation
* Sector performance

## Operations

* Work order value
* Execution status
* Completion progress

## Finance

* Billed value
* Collected value
* Collection rate
* Outstanding receivables
* Remaining billing

## Data Risks

* Missing financial values
* Missing dates
* Missing sectors
* Incomplete records

This provides an executive-oriented summary instead of only raw data.

---

# Limitations

The current prototype has several limitations.

## Current

* Data is fetched from monday.com at query time.
* Analysis is limited to currently implemented business metrics.
* Some business questions may require new analytics intents.
* Cross-board relationships depend on the available masked identifiers.
* Date interpretation uses the backend server date.

---

## Future Improvements

With additional development time, the system could include:

* Automated metric registry
* More advanced cross-board joins
* Trend analysis
* Month-over-month comparisons
* Forecasting
* Persistent caching
* Query history
* Follow-up conversational context
* Interactive charts
* Scheduled leadership reports
* Role-based access control
* More advanced data quality scoring

---

# Key Design Principle

The core design principle of this project is:

```text
Use AI for understanding and explanation.

Use deterministic code for business calculations.

Use monday.com as the source of truth.
```

This architecture allows the agent to provide conversational, executive-friendly business intelligence while maintaining reliable and reproducible calculations.

---

# Deliverables

The project includes:

* Hosted React frontend
* Hosted FastAPI backend
* monday.com read-only integration
* Gemini-powered conversational interface
* Dynamic data retrieval
* Data cleaning and normalization
* Deterministic BI analytics
* Data quality reporting
* Leadership update capability
* Decision Log
* Source code and setup instructions

---

# Example Founder Questions

```text
How is our pipeline looking?
```

```text
How is the energy sector pipeline looking this quarter?
```

```text
How many new opportunities were created this month?
```

```text
Which sector has the highest pipeline?
```

```text
What is our total outstanding receivable?
```

```text
How much have we billed versus collected?
```

```text
How is work order execution performing?
```

```text
Give me a leadership update.
```
