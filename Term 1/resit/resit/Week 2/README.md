# Silent Burnout Sentinel
### AI-Powered Employee Workload & Burnout Risk Assessment System

**AI for Good — Hackathon 2: Flow State**  
*Automate well-being with n8n*
Pavitra Pradeep

---

## Project Overview

Silent Burnout Sentinel is an AI-powered employee workload assessment system designed to identify potential signs of excessive workload and promote workplace well-being.

The system uses n8n workflow automation to process employee activity indicators, including screen usage, meeting schedules, working hours and historical workload patterns. These indicators are analyzed using AI to identify concerning workload patterns and generate personalized well-being recommendations.

The system automatically generates a workload assessment report and delivers it to the employee through Gmail.

Its primary purpose is to encourage employees to recognize unhealthy workload patterns earlier, take appropriate breaks and improve their work-life balance.

| | |
|---|---|
| **Project** | Silent Burnout Sentinel |
| **Hackathon** | AI for Good — Hackathon 2: Flow State |
| **Tool** | n8n |
| **SDG** | SDG 3 — Good Health and Well-being |
| **Focus** | Employee mental health and workplace well-being |
| **AI Technology** | OpenAI API |
| **Automation** | n8n |
| **Output** | Automated Gmail workload assessment report |

---

## Problem definition

Workplace burnout is a growing concern in modern working environments. Employees frequently experience excessive workloads, prolonged screen exposure, continuous meetings and insufficient opportunities to rest.

These conditions can contribute to chronic workplace stress, emotional exhaustion, reduced concentration and declining productivity.

One of the challenges is that employees do not always recognize or report these patterns themselves. Similarly, managers may not have sufficient visibility into workload distribution and employee well-being.

Traditional approaches often depend on periodic surveys, voluntary self-reporting or manual observation. These approaches may fail to identify concerning patterns early enough.

Silent Burnout Sentinel explores a proactive alternative: analyzing available workload indicators and using AI to identify patterns that may warrant attention.

### The problem we aim to solve

1. Employees may work for extended periods without sufficient breaks.
2. Excessive meetings can reduce time available for focused work.
3. Prolonged screen exposure may contribute to fatigue.
4. Repeated high-workload patterns can go unnoticed.
5. Employees may not recognize when their work habits are becoming unhealthy.

**Our central question:**

Can workflow automation and AI help employees recognize potentially unhealthy workload patterns and take proactive steps towards better mental well-being?

---

## SDG 3: Good Health and Well-being

SDG 3 focuses on ensuring healthy lives and promoting well-being for everyone at every age.

Mental health is an important part of overall health. Workplace stress and excessive workloads can negatively affect employees' psychological well-being and quality of life.

Silent Burnout Sentinel contributes to this goal by encouraging awareness of workload patterns and promoting healthier working habits.

The project focuses on:

- Promoting mental well-being in the workplace.
- Encouraging regular breaks and healthier working routines.
- Identifying potentially excessive workload patterns.
- Supporting work-life balance.
- Encouraging early awareness of possible burnout indicators.

The intended beneficiaries are employees who experience demanding digital work environments and organizations interested in supporting healthier workplace practices.

---

## User group

### Who uses Silent Burnout Sentinel?

The primary intended users are employees working in digitally intensive environments, particularly:

- Corporate employees.
- Software developers and IT professionals.
- Remote and hybrid workers.
- Employees who spend extended periods using computers.
- Professionals with frequent meetings and demanding schedules.

These employees may experience long screen hours, limited breaks and high meeting workloads.

### What do they need?

Our intended users need:

- Awareness of their daily workload patterns.
- Information about prolonged screen usage.
- Visibility into meeting-related workload.
- Identification of repeated workload concerns.
- Practical and achievable well-being recommendations.
- An automated assessment without requiring manual calculations.

### Who is not the intended user?

- Individuals seeking a clinical burnout diagnosis.
- Healthcare professionals seeking a medical diagnostic system.
- Employers seeking to monitor or rank employee productivity.
- Organizations seeking an automated employee performance evaluation system.

The project is designed as an employee well-being support tool, not an employee surveillance or medical diagnosis platform.

---

## Solution: From workload indicators to well-being recommendations

**Input:** Employee information and available workload indicators, including screen usage, meeting schedules and historical activity data.

**Processing:** n8n validates and processes the information, calculates workload metrics and sends structured indicators to an AI analysis node.

**Output:** A personalized workload assessment report containing observations, a risk category and practical recommendations, delivered automatically through Gmail.

### System architecture

```text
       Employee Information
                 |
                 v
       Employee Configuration
                 |
                 v
        Activity Data Input
                 |
          +------+------+
          |             |
          v             v
     Screen Usage   Calendar Data
          |             |
          +------+------+
                 |
                 v
         Input Validation
                 |
                 v
          Workload Metrics
                 |
                 v
         Historical Analysis
                 |
                 v
           AI Analysis
           (OpenAI API)
                 |
                 v
        Risk Classification
                 |
                 v
      Well-being Recommendations
                 |
                 v
         Report Generation
                 |
                 v
          Gmail Delivery
```

### Step-by-step workflow

1. **Employee configuration:** The workflow receives employee identification and email details.

2. **Activity data preparation:** Available screen-usage and calendar activity indicators are prepared for analysis.

3. **Input validation:** The workflow checks whether the required information is available and correctly structured.

4. **Workload calculation:** JavaScript processing calculates relevant workload indicators, such as screen time and meeting duration.

5. **Historical analysis:** Available historical records are examined to identify repeated workload patterns.

6. **AI analysis:** OpenAI receives the structured workload information and interprets potential well-being concerns.

7. **Risk classification:** The system organizes the assessment into workload risk categories.

8. **Recommendation generation:** The workflow produces practical suggestions based on the identified patterns.

9. **Report generation:** A structured assessment report is prepared.

10. **Automated delivery:** Gmail sends the assessment report to the employee.

---

## The AI model and how we use it

### AI integration

OpenAI acts as the intelligence layer of Silent Burnout Sentinel.

Rather than relying exclusively on fixed thresholds, the AI interprets the calculated workload indicators and generates understandable observations.

The AI analyzes available indicators such as:

- Daily screen exposure.
- Meeting frequency and duration.
- Extended working hours.
- Break frequency, where available.
- Repeated high-workload patterns.

It then generates a natural-language assessment and practical recommendations.

### Why AI is necessary

Without AI, the workflow would primarily calculate numerical indicators and compare them against predefined thresholds.

AI adds the ability to interpret multiple indicators together and communicate the results in understandable language.

For example, prolonged screen exposure combined with frequent meetings may warrant different recommendations from prolonged screen exposure with sufficient breaks.

The AI therefore contributes an interpretation and recommendation stage rather than simply formatting numerical results.

**AI technology:** OpenAI API  
**Model:** GPT-4o-mini (as specified in the implementation description)

The system provides indicative workload observations. It does not diagnose burnout, depression or any other medical condition.

---

## Workload risk assessment

The system uses workload indicators and AI-generated observations to organize assessments into four categories.

| Risk category | Interpretation |
|---|---|
| Low | Available workload indicators appear relatively balanced. |
| Moderate | Some workload patterns may require attention. |
| High | Excessive or repeated workload indicators suggest a need for changes. |
| Elevated | Persistent concerning workload patterns warrant proactive attention. |

These categories are intended to support awareness and self-reflection.

They should not be interpreted as validated clinical burnout scores.

---

## Automated email reporting

One of the main outputs is an automatically generated Gmail assessment report.

The report is intended to contain:

- Employee information.
- Screen-usage summary.
- Meeting workload analysis.
- Daily workload statistics.
- Historical workload observations.
- AI-generated assessment.
- Workload risk category.
- Personalized well-being recommendations.

Automated email delivery allows employees to receive their assessments without having to manually inspect the workflow.

---

## Technology stack

| Technology | Purpose |
|---|---|
| n8n | Workflow automation and orchestration |
| OpenAI API | AI-powered workload interpretation |
| JavaScript | Workload calculations and data processing |
| Gmail | Automated assessment delivery |
| Google Calendar | Calendar activity integration, where configured |
| JSON | Data exchange between workflow nodes |

---

## Working prototype

The prototype demonstrates how an automated workflow can transform workload information into an employee well-being assessment.

Its intended execution flow is:

```text
Employee Configuration
          |
          v
Activity Data Preparation
          |
          v
Input Validation
          |
          v
Workload Calculations
          |
          v
Historical Analysis
          |
          v
OpenAI Analysis
          |
          v
Risk Classification
          |
          v
Recommendations
          |
          v
Gmail Assessment Report
```

The workflow is designed to run automatically through its configured n8n trigger rather than requiring the user to manually initiate every assessment.

### Demonstration evidence

The GitHub submission should include:

- Complete n8n workflow JSON.
- Workflow execution screenshots.
- Evidence of the AI analysis node.
- Example input data.
- Example generated assessment.
- Gmail delivery screenshot.
- Presentation slides or demonstration video.

---

## How to run

### Prerequisites

- An n8n account or self-hosted n8n installation.
- OpenAI API key.
- Gmail account with OAuth2 access.
- Workflow JSON file.
- Required activity data or configured integrations.

### Setup instructions

1. Download the n8n workflow JSON file from this repository.
2. Open your n8n workspace.
3. Import the workflow JSON.
4. Configure the employee information and input data.
5. Configure the OpenAI API credentials.
6. Configure Gmail OAuth2 credentials.
7. Verify all node connections and expressions.
8. Configure the automatic trigger.
9. Activate the workflow.
10. Verify the execution and check the configured email inbox.

### Execution flow

```text
Configure Credentials
          |
          v
Import Workflow
          |
          v
Configure Input Data
          |
          v
Activate Automatic Trigger
          |
          v
Run Automated Assessment
          |
          v
Receive Gmail Report
```

---

## Privacy, security and ethical considerations

Silent Burnout Sentinel processes information that may reveal sensitive aspects of an employee's working habits and well-being.

Therefore, privacy and responsible AI use are essential.

The project follows these principles:

- Collect only the information necessary for workload assessment.
- Avoid collecting private screen contents or personal messages.
- Obtain employee consent before collecting activity information.
- Protect API keys and authentication credentials.
- Restrict access to individual assessment reports.
- Avoid sharing individual assessments with employers without explicit authorization.
- Establish appropriate data retention and deletion policies.
- Never use automated risk categories as the sole basis for employment decisions.

### Ethical reflection

The biggest risk is that an inaccurate assessment could either create unnecessary anxiety or falsely reassure an employee who is genuinely struggling. Screen time and meeting duration are imperfect indicators of mental well-being: someone may have a demanding but manageable schedule, while another person may experience significant stress despite apparently normal activity levels. OpenAI may also generate recommendations that do not fit an individual's circumstances. We therefore treat the output as an awareness tool rather than a medical diagnosis, make human judgment essential, and ensure employees retain control over their information. If the workflow fails, produces incomplete data or generates concerning results, employees should not rely on it as their only source of support. A human professional should take over whenever someone needs clinical or personal support. We would not trust automation alone to determine whether someone is experiencing burnout.

---

## Current implementation scope and limitations

The prototype demonstrates an automated workload assessment workflow.

The following distinctions are important:

- Prepared activity data is not equivalent to continuous real-time employee monitoring.
- Actual desktop monitoring requires a separately installed and authorized data-collection component.
- Live calendar analysis requires configured Google Calendar integration.
- Historical trend analysis depends on the availability of historical records.
- AI-generated assessments depend on valid API credentials and successful execution.
- Gmail delivery depends on successful OAuth2 configuration.
- Risk categories are indicative and are not clinically validated burnout assessments.

The system should be evaluated based on the functionality demonstrated in the actual n8n workflow.

---

## Future enhancements

- Live Google Calendar integration.
- Consent-based desktop activity collection.
- Automated daily and weekly workload assessments.
- Historical workload trend visualization.
- Employee-controlled well-being dashboard.
- Customizable workload thresholds.
- Improved recommendation personalization.
- Secure data storage and deletion mechanisms.
- Multilingual assessment reports.
- Integration with employee assistance and professional well-being resources.

---

## Conclusion

Silent Burnout Sentinel demonstrates how AI and workflow automation can be used to support employee mental health and workplace well-being.

By connecting activity data preparation, workload calculations, AI-powered interpretation, risk classification and automated email reporting, the project provides a proactive approach to identifying potentially unhealthy workload patterns.

Rather than replacing human judgment, the system aims to encourage awareness, self-reflection and healthier working habits.

Through the practical application of n8n and AI, Silent Burnout Sentinel contributes to SDG 3: Good Health and Well-being.

---

**Project:** Silent Burnout Sentinel  
**Category:** Artificial Intelligence | Workflow Automation | Employee Well-being  
**Primary Platform:** n8n  
**AI Engine:** OpenAI API  
**SDG:** 3 — Good Health and Well-being  
**Output:** Automated Gmail Workload Assessment Report
