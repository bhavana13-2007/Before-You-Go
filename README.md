## Deployment URL:https://before-you-go-f92u.onrender.com/
# Before You Go Assistant 🗺️💼

> **"Never make a second trip to a government office again."**

---

## Name
**Before You Go Assistant** — Developed by Team **PRISM**

---

## Description
The "Before You Go" Assistant is a web application designed by Team PRISM to eliminate the frustration of administrative bureaucracy. Too often, citizens spend hours commuting to and queuing at government offices only to realize they are missing a specific document, have brought the incorrect application fee, or lack the proper photocopy formats.

Our application serves as a digital concierge. By leveraging an intuitive frontend combined with a robust Flask backend, the system parses user requests for civic services (such as passport applications, ration card renewals, or income certificate issuances) and instantly generates an intelligent, foolproof breakdown of everything needed to complete the task successfully on the first visit.


### Planned Core Features
* **Dynamic Document Checklist:** Clear breakdowns of exactly what to bring, distinguishing between original documents and required photocopies.
* **Transparent Fee Breakdown:** Real-time visibility into application fees and officially accepted methods of payment.
* **Processing Time Estimator:** Data-backed timeline expectations to help citizens plan their schedules effectively.
* **"Common Mistakes" Shield:** Intelligent parsing of typical bureaucratic pitfalls (e.g., specific photo background colors, exact name matching with state identity cards, or digital signature rejections) to protect users from common errors.

---

## Installation

Follow these steps to configure your local development environment and run the completed codebase.

### Requirements
* **Python:** Version 3.10 or higher.
* **Flask** 
* **JAVASCRIPT**
* **Operating System:** LINUX

### Set Up Instructions

**1. Clone the repository directly from the project server:**
```bash
git clone [https://code.swecha.org/Bhavana132007/before-you-go-assistent.git](https://code.swecha.org/Bhavana132007/before-you-go-assistent.git)
cd before-you-go-assistent

```

**2. Initialize and isolate your Python environment:**

```bash
# For macOS and Linux:
python3 -m venv venv
source venv/bin/activate

# For Windows (Command Prompt):
python -m venv venv
venv\Scripts\activate

```

**3. Install the required dependencies (Flask):**

```bash
pip install flask 

```

---

## Roadmap

Team **PRISM**  build this project sequentially over our 2-day hackathon sprint:

* [ ] **Step 1:** Initialize data architecture schemas (`services.json`) and test backend Gemini API prompt logic.
* [ ] **Step 2:** Develop the base Python backend framework (`app.py`) using Flask.
* [ ] **Step 3:** Implement the user-facing web interface layout (HTML/CSS).

---

## Budget Log Ledger Note

The current repository contains a `data.csv` source file used by the Flask application. The budget logger feature appends to `data.csv` only when the file already contains the expected budget ledger header:

`date,category,amount,description`

If `data.csv` contains a different schema, the logger will preserve the file unchanged and report a header mismatch.

---

## Contributing

We welcome developers, UI/UX designers, and data curators to help map this project out with Team PRISM.
 check the open issues or refer explicitly to our [CONTRIBUTION.md](https://www.google.com/search?q=./CONTRIBUTION.md) to see how you can contribute.

---

## Authors and Acknowledgment

This application is being conceptualized and engineered during a 2-day Hackathon event by Team **PRISM**.

Team PRISM — Core Architecture, Frontend Engineering, JavaScript Integration, and Flask Backend Design.

---

## Project Status

Completed / Fully Deployed. Team PRISM has successfully turned the initial architectural scope into a functional application. The platform is officially live and hosted for testing.
