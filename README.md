The system enables users to register study sessions through Amazon Lex, saves the session information in DynamoDB, and automatically sends email reminders via SES fifteen minutes prior to the session using Lambda functions triggered by CloudWatch Events.

# AWS Virtual Study Group Bot 🎓🤖

This project is an **AWS-based Virtual Study Group Reminder Bot**.  
It allows users to register study sessions via **Amazon Lex**, stores details in **DynamoDB**, and automatically sends **email reminders** through **SES** 15 minutes before the session using **Lambda** and **CloudWatch Events**.

---

## 📌 Architecture

```mermaid
flowchart TD
    U[User] --> LEX[Amazon_Lex_Bot]
    LEX --> L1[Lambda_Logic_Handler]
    L1 --> DDB[(DynamoDB_Store_Session)]
    L1 --> CWE[CloudWatch_Events_Schedule]
    CWE --> L2[Lambda_Email_Sender]
    L2 --> SES[Amazon_SES_Send_Email]

````

---

## ⚙️ AWS Services Used

### 1. **Amazon Lex**

* Used to interact with the user via chat.
* Collects session details: **username, email, date, time, subject, etc.**
* **Slot Handling**:

  * Example slots: `Username`, `EmailId`, `SessionDate`, `SessionTime`, `Subject`.
  * If a slot is missing, Lex re-prompts the user.
  * One slot (e.g., backend-generated `session_id`) is filled programmatically, not by user.

📍 **Setup Path:**
`AWS Console → Amazon Lex V2 → Create Bot → Add Intents → Define Slots → Connect Lambda`

---

### 2. **AWS Lambda**

Two main Lambda functions:

* **Logic Lambda (Register Study Session)**

  * Triggered by Lex.
  * Stores session details into DynamoDB.
  * Creates reminders by scheduling **CloudWatch Events**.

* **Reminder Lambda (Send Email)**

  * Triggered by CloudWatch (every 15 mins).
  * Checks if a session is due within next 15 minutes.
  * Sends an **email reminder** using SES.

📍 **Setup Path:**
`AWS Console → Lambda → Create Function → Attach Execution Role (DynamoDB + SES + CloudWatch) → Deploy Code`

---

### 3. **Amazon DynamoDB**

* Table Name: `StudySession`
* Stores session data with attributes like:

  * `username`
  * `email`
  * `session_date`
  * `session_time`
  * `subject`
  * `session_id` (generated in backend)

📍 **Setup Path:**
`AWS Console → DynamoDB → Create Table → Primary Key = session_id`

---

### 4. **Amazon CloudWatch Events**

* Runs every **15 minutes**.
* Invokes **Reminder Lambda**.
* Ensures upcoming sessions (within 15 minutes) trigger reminders.

📍 **Setup Path:**
`AWS Console → CloudWatch → Rules → Create Schedule → Every 15 minutes → Target = Reminder Lambda`

---

### 5. **Amazon SES**

* Sends email reminders to registered users.
* Requires verification of **sender email**.
* Supports sandbox mode → only verified recipients can receive mail unless production access is granted.

📍 **Setup Path:**
`AWS Console → Simple Email Service → Verify Email Identity → Configure Domain (optional)`

---

## 🚀 How It Works

1. **User registers a study session** via **Lex bot**.
   Example: “I want to schedule a study session at 6:00 PM today for Physics.”

2. **Lex triggers Logic Lambda**, which:

   * Validates inputs.
   * Stores session in **DynamoDB**.
   * Logs scheduling via **CloudWatch Events**.

3. **CloudWatch triggers Reminder Lambda** every 15 mins:

   * Compares current time with session time.
   * If session is exactly 15 mins away → sends reminder.

4. **SES sends email** to the user:

   ```
   Subject: Study Session Reminder
   Body: Hey Ayush! This is a reminder for your Physics session at 18:00 UTC. See you soon!
   ```

---

🧪 Testing & Deployment
- Testing in AWS Console
- Test Lex Bot
- Go to Lex Console → Your Bot → Test Bot
- Try sample phrases: "Schedule a study session for Math on Friday at 3 PM"
- Test Lambda Functions
- Go to Lambda Console → Your Function → Test
- Create test events mimicking Lex request format
- Test DynamoDB
- Check DynamoDB Console for created entries
- Verify data structure and indexes
- Test SES
- Send test email through SES Console
- Verify email delivery and formatting

---

## 📅 Example Timeline

* Current Time: **20:00**
* Session Time: **20:15**
* Reminder Lambda runs at **20:00** → finds a session at 20:15 → sends reminder immediately. ✅
* Current Time: **20:04**
* Session Time: **20:15**
* Reminder Lambda runs at **20:00** (already missed window) → next run is at **20:15**, so reminder won’t go. ❌
  (This is expected — design works only on multiples of 15-min checks.)

---

## Common Issues
- Lex not triggering Lambda: Check IAM permissions and function configuration
- DynamoDB access denied: Verify Lambda execution role permissions
- SES delivery failures: Check email verification and sending limits
- CloudWatch Events not firing: Verify rule configuration and targets

## 🔮 Future Improvements
* Add **multi-channel notifications** (SMS via SNS, WhatsApp, etc.).
* Enhance Lex with **natural conversations** and multi-user session support.

---


## 📝 Author(s)
👤 **Ishita Chatterjee**, **Abhishek Roy**
