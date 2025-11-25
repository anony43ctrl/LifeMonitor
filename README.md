# LifeMonitor

<div align="center">

**Your Personal Operating System for Growth, Habits, and Vision.**

</div>

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Framework-Django%205.1-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Platforms](https://img.shields.io/badge/Platforms-Android%20%7C%20Desktop-333333?style=flat)](https://beeware.org/)
[![License](https://img.shields.io/badge/License-SEE%20FILE-yellow?style=flat)](LICENSE)

---

## 📖 Overview

LifeMonitor is a **hybrid cross-platform application** designed to help users **track their daily habits**, **journal their thoughts**, **manage tasks**, and **visualize their long-term goals**.

Unlike standard web apps, LifeMonitor is engineered to run as a **standalone native application** on **Android** and **Desktop** systems. It cleverly packages a full **Django backend** inside a native **Toga shell** (part of the BeeWare project), offering the power and maturity of a web framework with the privacy and portability of a local app.

A core feature is the **"Dynamic Database Switching"** system, which empowers users to fully own their data by storing it in local SQLite files that can be moved and synced across devices, ensuring **complete data privacy** and portability.

---

## ✨ Key Features

### 🏠 Central Dashboard

* A beautiful, **iOS-inspired Bento Grid** interface provides instant access to all application modules.
* **Quick Capture:** An iMessage-style input bar to instantly save thoughts or quotes without leaving the home screen.
* **Daily Manifesto:** A slide-up bottom sheet reminding you of your core principles.
* **Inspiration Feed:** A masonry grid displaying your saved quotes and ideas.

### ✅ The Ritual (Habit Tracking)

* A dedicated **"Daily Log"** interface designed for end-of-day reflection.
* **Habit Stacks:** Easily toggle habits via interactive "pills."
* **Journaling:** A clean writing space to capture daily summaries and lessons.
* **Social Connection:** Specifically track who you connected with or appreciated each day.

### 📊 Analytics & Insights

* Visualize your progress with interactive charts powered by **Chart.js**.
* **Consistency Graphs:** See your habit streaks and completion rates over time.
* **Cumulative Score:** Track your **"Life Score"** growth based on positive vs. negative habit weights.
* **Social Graph:** See a horizontal bar chart of the people you interact with most frequently.

### 📅 Task Management

* **Interactive Calendar:** View and plan tasks by month and day.
* **Consolidated List:** Manage tasks efficiently with a **"Swipe to Complete"** gesture (optimized for mobile).
* **Task Types:** Distinguish between standard tasks and critical **"Day Tasks."**

### 🚀 Vision Board

* A **timeline-based interface** for strategic planning and long-term goal visualization.
* **Master Plans:** Create overarching goals (e.g., "Launch Startup").
* **Branching Steps:** Break master plans down into actionable steps with detailed notes.

### 🔒 Privacy & Data Portability

* **Local First:** All data is stored locally on your device using **SQLite**.
* **Dynamic Database Switching:** The settings menu allows you to **Create, Load, or Switch** database files dynamically, giving you complete control over backups and syncing.

---

## 🛠️ Tech Stack

LifeMonitor is built on a modern, robust, and highly portable technology stack.

| Component | Technology | Version / Description |
| :--- | :--- | :--- |
| **Backend** | **Python** | 3.13 |
| **Web Framework** | **Django** | 5.1 |
| **Native Wrapper** | **BeeWare (Toga)** | Renders the Django app in a native system WebView. |
| **Packaging** | **Briefcase** | Compiles Python environment into native executables (APK, EXE). |
| **Database** | **SQLite3** | Local-first, file-based storage. |
| **Frontend** | **HTML5, Custom CSS/JS** | iOS-inspired design with **Chart.js** for visualizations. |

---

## 📂 Repository Structure

This project follows a hybrid structure combining a standard Django web project with a BeeWare/Briefcase native wrapper to achieve cross-platform capability.
```
LifeMonitor/
├── pyproject.toml           # Briefcase configuration (Dependencies, Permissions)
├── src/
│   ├── lifemonitor/         # Native App Wrapper (Toga)
│   │   ├── app.py           # ENTRY POINT: Starts the Django server & WebView
│   │   ├── __main__.py      # Python execution entry
│   │   └── resources/       # App icons and native assets
│   │   
│   └── webapp/              # Django Project Source
│       ├── manage.py        # Standard Django CLI tool
│       ├── db_config.json   # Dynamic DB path configuration
│       ├── user_monitoring/ # Project Settings Root
│       │   ├── settings.py  # Adjusted for Android paths & WhiteNoise
│       │   ├── urls.py      # Main URL routing
│       │   └── wsgi.py      # WSGI entry for the threaded server
│       │   
│       └── monitor/         # Main Django App (Logic)
│           ├── models.py    # Database Schema (Habits, Entries, Tasks)
│           ├── views.py     # Business Logic & UI Rendering
│           ├── forms.py     # Input Validation
│           ├── urls.py      # App-specific routing
│           ├── static/      # CSS, Images, JS (Chart.js)
│           │   └── css/     # styles.css (The iOS Design System)
│           └── templates/   # HTML Templates
│               └── monitor/ # (home.html, input.html, chart.html, etc.)
└── tests/                   # Test suite
```

---

## 🚀 Getting Started (Development)

To run this project locally on your machine for development and testing:

### 1. Clone the Repository
```bash
git clone https://github.com/anony43ctrl/LifeMonitor.git
cd LifeMonitor
```

### 2. Setup Environment
```bash
# Create a Virtual Environment
python -m venv venv

# Activate the environment
source venv/bin/activate    # On Linux/macOS
# venv\Scripts\activate     # On Windows

# Install Briefcase and all dependencies
pip install briefcase
```

### 3. Run in Dev Mode

This command utilizes Briefcase to launch the application on your desktop as a native window, simulating the packaged environment.
```bash
briefcase dev
```

---

## 📱 Building for Android

To compile the app into an APK file for your phone:

### Prerequisites

* **Java JDK 17+** must be installed and correctly configured in your environment path.
* **Android SDK** (Briefcase will automatically manage the download and configuration of necessary components).

### Build Commands

**1. Create the Android Project Structure:**
```bash
briefcase create android
```

**2. Build the App (Generates the APK):**
```bash
briefcase build android
```

**3. Run on Device (Requires USB Debugging Enabled):**
```bash
briefcase run android -d
```

---

## 📄 License

This project is licensed under a proprietary license. Please see the **[LICENSE](LICENSE)** file at the root of the repository for full details.

---

## 🤝 Contributing

We welcome contributions! If you would like to contribute, please:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.
