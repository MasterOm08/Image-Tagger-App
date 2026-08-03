# Image-Tagger-App
A mini-project for Cloud Application Development

# AI Image Tagger & Metadata Catalog

An automated, server-less web application built with **Flask** and deployed on **Google Cloud Platform (GCP)**. The app allows users to upload images, automatically analyzes their content using **Google Cloud Vision API**, stores the raw assets in **Google Cloud Storage (GCS)**, and indexes the resulting metadata in **Google Cloud Firestore**.

---

## Architecture & Cloud Services

This project integrates four core Google Cloud services:

* **Google App Engine (Standard Environment)**: Hosts the Python 3.12 Flask app behind a managed Gunicorn WSGI server.
* **Google Cloud Storage (GCS)**: Stores raw user-uploaded image files securely in a cloud bucket.
* **Google Cloud Vision API**: Performs automated image label detection to extract relevant tags and confidence scores.
* **Google Cloud Firestore**: A NoSQL document database storing image metadata (GCS URL, generated tags, upload timestamp).

---

## Tech Stack & Dependencies

* **Language**: Python 3.12
* **Web Framework**: Flask
* **WSGI Server**: Gunicorn
* **GCP SDKs**: `google-cloud-storage`, `google-cloud-vision`, `google-cloud-firestore`

---

## Local Development Setup

### 1. Prerequisites
* Python 3.12 installed
* Google Cloud SDK (gcloud CLI) installed and authenticated
* A GCP Project with Vision, Firestore, and Storage APIs enabled

### 2. Installation

1. **Clone the repository:**
   git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   cd YOUR_REPOSITORY_NAME

2. **Create and activate a virtual environment:**
   python -m venv venv
   .\venv\Scripts\activate

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Set Local Environment Variables:**
   $env:GOOGLE_APPLICATION_CREDENTIALS="path\to\your\service-account-key.json"

5. **Run locally:**
   python app.py

---

## Production Deployment (GCP App Engine)

The production app utilizes **Application Default Credentials (ADC)** provided natively by App Engine, eliminating the need to hardcode service account keys in production.

1. **Deploy to App Engine:**
   gcloud app deploy

2. **Launch the application:**
   gcloud app browse

---

## Configuration Files

* `app.yaml`: Defines App Engine runtime (`python312`) and startup entrypoint (`gunicorn -b :$PORT app:app`).
* `requirements.txt`: Manages production dependencies for build isolation.
* `.gitignore`: Ensures local credentials, `venv`, and temporary files are strictly excluded from git tracking.
