# Contributing to "Before You Go" Assistant 

First off, thank you for considering contributing to our project! Hackathons thrive on collaboration, and we are thrilled to have you look through our codebase.

---

# Deployment URL: 
https://before-you-go-f92u.onrender.com/

##  Why We Chose This Topic ("The Why")

Bureaucracy can be incredibly overwhelming. Almost everyone has a story about standing in a long queue at a government office (for a passport, ration card, or certificate) only to turn back because they missed a single photocopy or brought the wrong fee amount. 

We chose **"Before You Go"** because it addresses a universal real-world problem: **wasted time and civic frustration.** By building a lightweight, zero-nonsense assistant, our goal is to empower citizens with immediate, clear, and actionable data before they ever step out of their house. We want to convert bureaucratic confusion into absolute clarity.

---

##  Welcome Newcomers! How to Join and Help

Whether you are a seasoned developer or this is your very first hackathon, there is a place for you here. If you want to jump in right now, follow this quick guide:

### Step 1: Claim or Suggest a Task
1. Look at our open issues or our "Future Roadmap" in the `README.md`.
2. If you see something you like, drop a comment saying: *"I'd like to work on this!"*
3. Have a completely new feature idea? Open a new issue and briefly outline it.

### Step 2: Set Up Your Environment
Get the codebase running locally on your machine in under 2 minutes:
```bash
# Clone the repository
git clone [https://code.swecha.org/Bhavana132007/before-you-go-assistent.git](https://code.swecha.org/Bhavana132007/before-you-go-assistent.git)
cd before-you-go-assistent

# Set up your python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Flask
pip install flask

# Start the server
python app.py
```
---

## 🛠️ Step-by-Step Contribution Workflow
To keep the codebase stable during the fast-paced hackathon, please follow this standard workflow for your code changes:

1. **Create a Feature Branch**
Never work directly on the main or master branch. Create a descriptive branch for your task:

Bash
git checkout -b feature/your-feature-name
# Example: git checkout -b feature/add-drivers-license

2. **Implement Your Changes**
Keep your code clean, readable, and follow the existing patterns in app.py and the templates.

If you are adding a new government service, locate our central data configuration file (e.g., data.py or the service configuration array) and append your new structured text arrays there.

3. **Test Your Changes Locally**
Before saving your progress to the cloud, run the application locally to verify everything works:

Fire up the server with python app.py.

Open [https://before-you-go-f92u.onrender.com/](https://before-you-go-f92u.onrender.com/) in your browser.

Test the manual dropdown menu and search functions to confirm your new data or UI adjustments display perfectly without throwing internal server errors (500 errors).

4. **Commit and Push**
Write a clear, descriptive commit message detailing what you fixed or added:

Bash
git add .
git commit -m "Add required document data for Driver's License renewal"
git push origin feature/your-feature-name
5. Open a Pull Request (PR)
Head over to the repository page on the git platform.

Click Create Pull Request or New Merge Request.

Fill out the PR template by describing what you did and link it to the issue you claimed (e.g., Closes #12).

Wait for a core Team PRISM maintainer to review and merge your code!

---

### Project Context & Technical Architecture
To help you understand how the system works before you write code, here is how our Flask application is structured:

1. **Data Driven Hierarchy:** The application uses a central data configuration setup (such as a local Python dictionary or text array structure) to dynamically render requirements. This ensures adding a new government department doesn't require rewriting core HTML.

2. **State Verification Logic:** The template engine dynamically processes profile variables (e.g., distinguishing between standard requirements and special configurations like Tatkal/Expedited pathways).

3. **Offline-Ready Design:** The interface targets highly scannable, lightweight elements to ensure fast client-side rendering under constrained remote connections.

---

### Strategic Contribution Targets
To maximize our development speed during this hackathon block, we are looking for tactical support in these core domains:

* Core UI Layout Refinement: Adjusting cascading alignment styles within the interface templates to guarantee smooth element spacing on extreme small-screen viewports.


* Dynamic Exception Warnings: Writing clear, context-specific warning blocks for common procedural traps (e.g., missing original verification documents, out-of-state identity processing rules).

* Service Dataset Expansion: Standardizing procedural text arrays for secondary government services (Driver's Licenses, Ration Card processing, Local Registrations) into structured template variables.

---