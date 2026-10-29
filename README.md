<p align="center">
  <img src="Trustnode_logo.png" alt="TrustNode Logo" width="250">
</p>

# TrustNode 🚀
**Automated AI-Powered Escrow & Code Evaluation Platform**

TrustNode is an end-to-end bounty management platform built for freelance developers and sponsors. It eliminates the friction of manual code reviews and delayed payments by using AI to instantly evaluate code submissions and automatically triggering secure, instant payouts. 

## 💡 The Problem
In the freelance developer ecosystem, sponsors spend hours manually reviewing code bounties, while freelancers wait days for their work to be approved and their payments to clear. TrustNode automates the trust layer: code is evaluated instantly, and funds are released the second the criteria are met.

## ✨ Key Features
* **Freelancer Submission Portal:** A clean, responsive Tailwind CSS interface for developers to submit their solutions and PayPal details.
* **AI Code Evaluation:** Integrates with Groq's LLM to automatically parse submitted code against the sponsor's specific success criteria.
* **Automated Escrow Payouts:** Directly integrates the **PayPal Payouts API** to securely disburse funds with zero human intervention once the AI approves the code.
* **Real-Time Sponsor Dashboard:** A dynamic AG Grid interface for sponsors to track submission statuses, AI feedback, and PayPal transaction Batch IDs in real-time.

## 🛠️ Tech Stack
* **Backend:** Django, Django REST Framework, Python
* **Frontend:** HTML5, Tailwind CSS, AG Grid
* **AI / Evaluation:** Groq AI (LLM for automated code review)
* **Payments:** PayPal Payouts API (Sandbox Environment)
* **Database:** SQLite (Development) / PostgreSQL (Production)

## 🌍 Live Demo
The application is deployed on Render and connected to a live production PostgreSQL database. You can test the full automated escrow flow here:

* **Freelancer Submission Portal:** [https://trustnode-nkx1.onrender.com/api/submit/](https://trustnode-nkx1.onrender.com/api/submit/)
* **Sponsor Dashboard:** [https://trustnode-nkx1.onrender.com/api/dashboard/](https://trustnode-nkx1.onrender.com/api/dashboard/)

## 🚀 Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/raghudipghosh862-glitch/TrustNode.git](https://github.com/raghudipghosh862-glitch/TrustNode.git)
   cd TrustNode

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

3. **Set up Environment Variables:**

 Create a .env file in the root directory and add your API keys:

 **PAYPAL_CLIENT_ID**=your_paypal_sandbox_client_id,

 **PAYPAL_SECRET**=your_paypal_sandbox_secret,

 **GROQ_API_KEY**=your_groq_api_key

4. **Run Database Migrations:**
   ```bash
    python manage.py makemigrations
    python manage.py migrate

5. **Start the Development Server:**
   ```bash
    python manage.py runserver


6. **Access the Submission Portal:**
   ```bash
   [http://127.0.0.1:8000/api/submit/]

7. **Access the Sponsor Dashboard:**
   ```bash
   [http://127.0.0.1:8000/api/dashboard/]