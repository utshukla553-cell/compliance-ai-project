# Compliance AI

Multilingual Regulatory Document Intelligence System

## Project Overview

Compliance AI is a document intelligence system designed to analyze regulatory and compliance-related documents.

The system accepts PDF and image documents, extracts readable text, detects the document language, and uses AI-based analysis to identify important clauses, compliance dates, document type, priority level, and actionable compliance checklist items.

## Key Features

- PDF and image document upload
- PDF text extraction
- OCR support for image documents
- Automatic language detection
- Google Gemini AI analysis
- Important clause extraction
- Compliance date detection
- Priority classification
- AI-generated compliance checklist
- Compliance deadline dashboard
- SQLite database storage
- Document details page
- Document deletion
- FastAPI backend
- Responsive web interface

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Google Gemini API
- PyMuPDF
- pdfplumber
- Tesseract OCR
- Pillow
- Pandas
- LangDetect
- Jinja2
- HTML
- CSS

## Application Workflow

Upload Document -> File Validation -> Text Extraction / OCR -> Language Detection -> Gemini AI Analysis -> Summary, Clauses, Dates, Checklist and Priority -> SQLite Database -> Dashboard

## AI Analysis

Google Gemini analyzes the extracted document text and generates:

- Document summary
- Important compliance clauses
- Compliance dates and deadlines
- Document type
- Priority level
- Actionable compliance checklist

## Priority Levels

### High

Used for urgent compliance requirements, penalties, legal action, deadlines, or non-compliance risks.

### Medium

Used for mandatory or important compliance requirements without strong urgent indicators.

### Low

Used for documents with limited immediate compliance risk.

## Compliance Checklist

The system generates short actionable tasks from regulatory documents.

Example:

1. Conduct an annual waste management audit.
2. Prepare the waste management audit report.
3. Submit the audit report before the required deadline.

## Database

The application uses SQLite with SQLAlchemy.

Document records contain:

- Filename
- File path
- Language
- Document type
- Summary
- Important clauses
- Compliance dates
- Compliance checklist
- Priority
- Creation timestamp

## Installation

Create a virtual environment:

python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

## Environment Variables

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here

Never share or commit the actual API key.

## Running the Application

Start the server:

python -m uvicorn app.main:app --reload

Dashboard:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## Supported Files

- PDF
- PNG
- JPG
- JPEG
- TIFF
- BMP

## Testing

Upload a regulatory PDF or image and verify:

1. Document appears on the dashboard.
2. Language is detected.
3. Document type is generated.
4. AI summary is displayed.
5. Important clauses are displayed.
6. Compliance dates appear.
7. Priority is assigned.
8. Compliance checklist is generated.
9. Checklist count appears on the dashboard.
10. Document details page displays the analysis.

## Project Status

Stage 1 - Research and Requirements: Completed

Stage 2 - Document Collection and Categorization: Completed

Stage 3 - AI Workflow and Document Analysis: Completed

Stage 4 - Compliance Framework and Dashboard: Completed

Stage 5 - Final Documentation and Submission: Completed

## Future Improvements

- User authentication
- Advanced multilingual OCR
- Email notifications for deadlines
- Calendar integration
- Compliance history and audit logs
- Advanced analytics
- Role-based access control
- Cloud database integration
- Production deployment

## Disclaimer

This project is intended for document analysis and compliance assistance. AI-generated results should be reviewed by qualified professionals before making legal or regulatory decisions.
