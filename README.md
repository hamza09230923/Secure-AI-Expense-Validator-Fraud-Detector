# Secure AI Expense Validator & Fraud Detector

![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CDK](https://img.shields.io/badge/AWS%20CDK-Orange?style=for-the-badge&logo=amazon-aws&logoColor=white)

## 📖 Overview
**Secure AI Expense Validator** is a serverless, event-driven pipeline designed to automate financial document processing.

Unlike standard OCR tools, this project focuses on **FinTech compliance**. It utilizes AI to automatically detect and redact PII (Personally Identifiable Information) for GDPR/KYC compliance and executes logic-based **Fraud Detection** on transaction amounts before storage.

The entire infrastructure is defined as code using **AWS CDK**, ensuring a reproducible and secure enterprise-grade environment.

---

## 🏗 Architecture
This project uses an event-driven architecture to decouple ingestion, processing, and storage.

![Architecture Diagram](https://via.placeholder.com/800x400?text=Insert+Your+Draw.io+Diagram+Here)
*(Note: Replace this image link with a screenshot of your actual architecture diagram)*

**The Data Flow:**
1.  **Ingestion:** Receipt image uploaded to **Amazon S3**.
2.  **Orchestration:** S3 Event triggers **AWS Step Functions**.
3.  **OCR Extraction:** **Amazon Textract** pulls raw text and financial data.
4.  **Compliance & Logic:**
    * **Amazon Comprehend** scans for PII (Names, Addresses).
    * **AWS Lambda** executes fraud rules (Velocity checks, Amount thresholds).
5.  **Storage:** Clean, redacted data is stored in **Amazon DynamoDB**.

---

## 💰 Financial Business Logic
This project implements specific logic to solve common back-office financial challenges:

### 1. GDPR & PII Redaction (Compliance)
To adhere to data privacy regulations (like GDPR and CCPA), raw receipt data is often unsafe to store in plain text.
* **Solution:** The pipeline uses NLP (Amazon Comprehend) to identify entities such as `PERSON`, `ADDRESS`, and `PHONE`. These are redacted (replaced with `[REDACTED]`) before the record is committed to the database.

### 2. Automated Fraud Rules (Risk Management)
The system applies immediate risk assessment logic:
* **High-Value Flag:** Transactions > **£500** are automatically tagged as `STATUS: MANUAL_REVIEW`.
* **Merchant Blacklisting:** Vendor names are checked against a mock "High Risk" list (e.g., Gambling, Crypto exchanges).
* **Currency Normalization:** Regex logic ensures all currency inputs are standardized to a strict float format for accounting accuracy.

---

## 🛠 Tech Stack

* **Infrastructure as Code:** AWS CDK (Python)
* **Orchestration:** AWS Step Functions
* **Compute:** AWS Lambda (Python 3.9)
* **Machine Learning:**
    * Amazon Textract (Optical Character Recognition)
    * Amazon Comprehend (Natural Language Processing)
* **Database:** Amazon DynamoDB (On-Demand Capacity)
* **Storage:** Amazon S3

---

## 🚀 How to Deploy

**Prerequisites:**
* AWS CLI installed and configured
* Node.js & AWS CDK installed
* Python 3.9+

**Steps:**
1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/your-username/secure-expense-validator.git](https://github.com/your-username/secure-expense-validator.git)
    cd secure-expense-validator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Deploy the stack:**
    ```bash
    cdk deploy
    ```

4.  **Test the pipeline:**
    * Upload a sample receipt image to the created S3 bucket.
    * Check DynamoDB for the processed record.

---

## 🧪 Challenges & Learnings

* **Infrastructure as Code (IaC):** Migrating from manual console configuration to AWS CDK was a steep learning curve but allowed for rapid iteration and "clean" teardowns of the environment.
* **OCR Consistency:** Amazon Textract occasionally misinterprets currency symbols. I implemented a regex cleaning layer in the Lambda function to handle edge cases (e.g., misreading `£` as `E`).
* **State Management:** Using Step Functions instead of a single monolithic Lambda allowed for better error handling and retry logic, specifically for handling API throttling from the AI services.

---

## 🔮 Future Improvements
* **Integration:** Add API Gateway to allow receipt uploads via a mobile frontend.
* **Analytics:** Connect Amazon QuickSight to DynamoDB to visualize spending trends.
* **Advanced Fraud:** Implement Amazon Fraud Detector for ML-based anomaly detection.
* 
