# Backend — MAiSIGNAL Alert System

Python application that sends pharmaceutical market intelligence alerts via the Ecomail transactional email API.

## Prerequisites

- Python 3
- pip
- Ecomail account with a valid API key

## Setup

1. Create a virtual environment:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create the environment file with your Ecomail API key:

   ```bash
   echo 'ECOMAIL_API_KEY=your-api-key-here' > config/.env
   ```

## Usage

```bash
python src/send_maisignal_alert.py
```

The script will:

- Load the API key from `config/.env`
- Read the HTML email template from `templates/`
- Send the email via `POST https://api2.ecomailapp.cz/transactional/send-message`
- Enable click and open tracking

## Structure

```
backend/
├── src/
│   └── send_maisignal_alert.py   # Alert sender script
├── templates/
│   └── sukl-alert-email-real-data.html  # HTML email template
├── config/
│   └── .env                      # API key (not committed)
└── requirements.txt
```
