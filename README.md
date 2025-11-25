# 🪴 LifeMonitor

<div align="center">
[cite_start]Your Personal Operating System for Growth, Habits, and Vision. [cite: 3]
</div>

[cite_start]LifeMonitor [cite: 1] [cite_start]is a hybrid cross-platform application designed to help users track their daily habits, journal their thoughts, manage tasks, and visualize their long-term goals[cite: 6].

[cite_start]Unlike standard web apps, LifeMonitor is built to run as a **standalone native application** on Android and Desktop systems[cite: 7]. [cite_start]It packages a full Django backend inside a native Toga shell, offering the power of a web framework with the privacy and portability of a local app[cite: 8].

---

## ✨ Key Features

1.  ### 🏠 Central Dashboard
    * [cite_start]A beautiful, iOS-inspired **Bento Grid** interface provides instant access to all modules[cite: 12].
    * [cite_start]**Quick Capture:** An iMessage-style input bar to instantly save thoughts or quotes without leaving the home screen[cite: 13].
    * [cite_start]**Daily Manifesto:** A slide-up bottom sheet reminding you of your core principles[cite: 14].
    * [cite_start]**Inspiration:** A masonry grid displaying your saved quotes and ideas[cite: 15].

2.  ### ✅ The Ritual (Habit Tracking)
    * [cite_start]A dedicated "**Daily Log**" interface designed for end-of-day reflection[cite: 17].
    * [cite_start]**Habit Stacks:** Toggle habits via interactive "pills"[cite: 18].
    * [cite_start]**Journaling:** A clean writing space to capture daily summaries and lessons[cite: 19].
    * [cite_start]**Social Connection:** Specifically track who you connected with or appreciated each day[cite: 20].

3.  ### 📊 Analytics & Insights
    * [cite_start]Visualize your progress with interactive charts powered by Chart.js[cite: 22].
    * [cite_start]**Consistency Graphs:** See your habit streaks and completion rates[cite: 23].
    * [cite_start]**Cumulative Score:** Track your "**Life Score**" growth over time based on positive vs. negative habit weights[cite: 24].
    * [cite_start]**Social Graph:** See a horizontal bar chart of the people you interact with most frequently[cite: 25].

4.  ### 📅 Task Management
    * [cite_start]**Interactive Calendar:** View tasks by month and day[cite: 27].
    * [cite_start]**Consolidated List:** Manage tasks with a "Swipe to Complete" gesture (mobile)[cite: 28].
    * [cite_start]**Task Types:** Distinguish between standard tasks and critical "**Day Tasks**"[cite: 29].

5.  ### 🚀 Vision Board
    * [cite_start]A timeline-based interface for strategic planning[cite: 31].
    * [cite_start]**Master Plans:** Create overarching goals (e.g., "Launch Startup")[cite: 32].
    * [cite_start]**Branching Steps:** Break goals down into actionable steps with detailed notes[cite: 33].

6.  ### 🔒 Privacy & Data Portability
    * [cite_start]**Local First:** All data is stored locally on your device using SQLite[cite: 35].
    * [cite_start]**Dynamic Database Switching:** The system allows users to own their data completely by saving it to local files that can be moved across devices[cite: 9].
    * [cite_start]The settings menu allows you to **Create**, **Load**, or **Switch** database files dynamically[cite: 36].
    * [cite_start]You can keep your data in a private internal folder or in the shared "Documents" folder for easy backup and syncing[cite: 37].

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5, Django Templates, Custom CSS, JavaScript (Chart.js) | [cite_start]Custom Glassmorphism/iOS Design System[cite: 46]. |
| **Backend** | Python 3.13, Django 5.1 | [cite_start]Provides the core application logic[cite: 47]. |
| **Native Wrapper** | BeeWare (Toga) | [cite_start]Renders the web app in a native system WebView[cite: 48]. |
| **Packaging** | Briefcase | [cite_start]Compiles the Python environment into an APK (Android) or Executable (Linux/Windows)[cite: 49]. |
| **Database** | SQLite3 | [cite_start]Used for local, dynamically pathing data storage[cite: 50]. |

---

## 🚀 Getting Started (Development)

To run this project locally on your machine for development:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/anony43ctrl/LifeMonitor.git](https://github.com/anony43ctrl/LifeMonitor.git)
    cd LifeMonitor
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    You need **Briefcase** to run the native wrapper mode.
    ```bash
    [cite_start]pip install briefcase [cite: 55]
    ```

4.  **Run in Dev Mode:**
    This launches the app on your desktop as a native window.
    ```bash
    [cite_start]briefcase dev [cite: 56]
    ```

---

## 📱 Building for Android

To compile the app into an APK file for your phone:

1.  **Install Prerequisites:**
    * [cite_start]Java JDK 17+ [cite: 60]
    * [cite_start]Android SDK (Briefcase handles this automatically) [cite: 61]

2.  **Create the Android Project:**
    ```bash
    [cite_start]briefcase create android [cite: 62]
    ```

3.  **Build the App:**
    ```bash
    [cite_start]briefcase build android [cite: 63]
    ```

4.  **Run on Device:**
    Connect your phone via USB (Enable USB Debugging) and run:
    ```bash
    [cite_start]briefcase run android -d [cite: 64]
    ```
