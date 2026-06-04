
# "Before You Go" Assistant — User Manual 📖🧭

Welcome to the official User Manual for the **Before You Go Assistant**, developed by Team **PRISM**. This guide will walk you through how to use the platform to plan your visits to government offices flawlessly using our AI-powered features.

---

## 🗺️ System Overview

The **Before You Go Assistant** acts as your digital civic consultant. By combining structured local databases with intelligent natural language processing, the application interprets your needs and outputs a structured plan so you never have to make a second trip to a government office.

---

## 🚀 How to Use the Application

### 1. Accessing the Platform
Once the local development server is active, open your web browser and navigate to:
```text
https://before-you-go-f92u.onrender.com/

```

### 2. Finding Your Government Service

Team **PRISM** provides two intuitive tracking methods on the homepage:

* **Method A (Drop-down Selector):** Click the service selection menu to choose from standardized categories (e.g., Fresh Passport Application, Ration Card Renewal, Income Certificate).
* **Method B (AI Search Bar):** Type your issue in plain, informal language. For example: "I need to fix the spelling of my name on my food card" or "What do I bring to get a passport for my newborn baby?" The application will automatically interpret your intent and match it with the correct procedural guide from our integrated service directory.

### 3. Reviewing Your Personalized Output Dashboard

After selecting or submitting your query, the application will display a clean layout divided into four critical tracking modules:

#### 📋 A. Required Documents Checklist

This module displays an interactive checklist. It clearly differentiates between:

* **Original Records:** Documents required by the officer for physical verification.
* **Photocopies:** The exact number of physical copies you must leave behind.
* *Tip: Use the on-screen checkboxes to cross-reference your paperwork physically before leaving your house.*

#### 💵 B. Fee Breakdown & Payment Modes

Avoid showing up with the wrong payment format. This window displays:

* The exact processing fee amount.
* The mandated payment methods (e.g., *Online Challan Only*, *Cash Accepted*, or *Demand Draft*).

#### ⏰ C. Estimated Processing Timeline

Displays the standard turnaround time (e.g., *15-20 Business Days*) required for the department to process your request so you can plan accordingly.

---

## 🛠️ Troubleshooting & Frequently Asked Questions

### Q1:The search bar doesn't return any results. What should I do?
**Cause:** Your phrase might be too unique, or the local service directory configuration file is missing from your project directory.

* **Solution:** Double-check that your server files are fully downloaded and try using simpler keywords (like "Passport" instead of a long sentence).Alternatively, utilize the manual drop-down selector to access standard database profiles directly. 
Ensure your environment variable is set up in your terminal before running `python app.py`:


### Q2: Can I download or print my finalized document checklist?

* **Status:** This is a planned roadmap feature for Phase 1 of our rollout. Currently, we recommend taking a screenshot of your generated dashboard on your mobile device before heading to the administrative facility.

### Q3: I found a mistake in the required document list for my region.

* **Solution:** Help Team PRISM expand our database accuracy! Head over to our CONTRIBUTION.md instructions to find out how to easily add or update entries in the local text files and service configuration data directories.