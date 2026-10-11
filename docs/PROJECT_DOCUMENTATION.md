# Compliance AI - Project Documentation
## 1. Project Overview
Compliance AI is a multilingual regulatory document intelligence system designed to analyze compliance-related PDF and image documents.
The system extracts text, detects document language, analyzes important clauses, identifies compliance dates, assigns document type and priority, and generates actionable compliance checklist items.

## 2. Technology Stack
- Python 3.13.5
- FastAPI
- SQLAlchemy
- SQLite
- Google Gemini API
- PyMuPDF and pdfplumber
- Tesseract OCR
- Jinja2
- HTML and CSS

## 3. Application Workflow
1. User uploads a PDF or image document.
2. The system extracts text from the document.
3. OCR is used when readable text is not directly available.
4. The document language is detected.
5. Gemini AI analyzes the extracted content.
6. Important clauses, compliance dates, document type and priority are identified.
7. Actionable compliance checklist tasks are generated.
8. The analysis is stored in the SQLite database.
9. Results are displayed through the FastAPI web dashboard.

## 4. AI Analysis
The system uses the Google Gemini API to analyze extracted regulatory document text.
The AI analysis identifies the document summary, important compliance clauses, compliance dates, document type, priority level, and actionable checklist tasks.
The AI response is processed as structured data so that the results can be stored in the database and displayed on the dashboard.
Priority levels are classified as Low, Medium, or High based on the urgency and importance of compliance requirements.

## 5. Database
SQLite is used as the local database and SQLAlchemy is used for database interaction.
Each uploaded document is stored with its filename, file path, detected language, document type, summary, important clauses, compliance dates, checklist, priority, and creation timestamp.

## 6. Dashboard
The web dashboard provides an overview of uploaded compliance documents.
It displays document statistics, priority information, compliance deadlines, and checklist task counts.
Users can open a document to view its detailed AI analysis, compliance dates, important clauses, priority, and compliance checklist.

## 7. Testing
The application was tested by running the FastAPI development server and uploading compliance-related documents through the web interface.
The document upload, text extraction, OCR processing, language detection, Gemini AI analysis, database storage, deadline tracking, priority display, and compliance checklist features were verified.
The FastAPI Swagger documentation is available through the /docs endpoint for API testing.

## 8. Installation and Running
1. Create and activate the Python virtual environment.
2. Install the required packages using requirements.txt.
3. Configure the GEMINI_API_KEY environment variable in the .env file.
4. Start the FastAPI application using Uvicorn.
5. Open the web dashboard in a browser and upload a supported document.

## 9. Supported Documents
The system supports PDF documents and common image formats that can be processed through OCR.


## 10. Project Status
Stage 1: Research and requirements - Completed.
Stage 2: Document collection and categorization - Completed.
Stage 3: AI workflow - Completed.
Stage 4: Compliance framework and dashboard - Completed.
Stage 5: Final documentation and submission - Completed.

## 11. Future Improvements
- Add user authentication and role-based access.
- Add advanced search and filtering.
- Add email or notification reminders for upcoming compliance deadlines.
- Improve multilingual OCR and document processing.
- Add cloud deployment and production monitoring.

## 12. Conclusion
Compliance AI provides an end-to-end workflow for converting regulatory documents into structured and actionable compliance information.
The project combines document processing, OCR, language detection, generative AI, database management, deadline tracking, and a web dashboard to support compliance-related document analysis.
