<center><img src="axislogo.png" width="80" height="80"></center>

# <center>AXIS | Data Intelligence Agent</center>

## About The Project

**AXIS** is an **intelligent data agent** designed to provide **real-time, accelerated business intelligence**.

AXIS allows users to ask complex data questions using natural language. The system, which operates as a "senior data analyst", instantly processes these queries and delivers visualized answers, either as charts or tables.

It automatically handles database connectivity, SQL generation, and visualization, following a strict set of rules to ensure safe query execution.

### Key Features

*   **Intelligent Agent:** Uses advanced AI (GPT/Gemini models) for tool calling to execute data tasks.
*   **Database Analysis:** Detects the SQL dialect (e.g., PostgreSQL, MySQL) and analyzes the database schema to ensure accurate query generation.
*   **Visualizations:** Supports displaying results as tables (DataFrames) or various chart types (line, bar, scatter, pie) using Plotly. Charts are styled using a specialized color palette (Gold, Cyan, Orchid, Orange, Silver).
*   **Secure Connection:** Requires a database connection string and GPT/Gemini API key, which is handled securely using a password input type.
*   **Structured Feedback:** Provides concise technical summaries and explanations after generating charts.

### Built With

This project relies on a modern data and AI stack:

*   **Python** (Base language)
*   **Anaconda** (Environment management)
*   **Streamlit** (Web application framework)
*   **OpenAI** (LLM integration via client and API calls)
*   **Plotly** (Advanced chart generation)
*   **SQLAlchemy** (Database connection and SQL execution)
*   **Pandas** (Data manipulation and DataFrame handling)

---

## Getting Started

To run AXIS, you must first ensure you have the necessary Python environment set up and the required dependencies installed.

### Prerequisites

You need access to an OpenAI/Gemini API key and a valid database connection string.

### Installation

Follow these steps to set up your project locally:

1.  **Clone the repository.**
    ```bash
    git clone https://github.com/deryakubraer/data-analytics-ai-agent.git
    
    cd data-analytics-ai-agent
    ```

2.  **Install Python dependencies** using the provided `requirements.txt` file (assuming standard installation practice, as complex libraries like SQLAlchemy and Plotly are used).
    ```bash
    pip install -r requirements.txt
    ```
 

3.  **Run the Streamlit application.**
    ```bash
    streamlit run app.py
    ```
    *(The main page configuration sets the app title to "AXIS | Data Intelligence" and uses a wide layout with a collapsed sidebar initially. The application file typically starts by importing `streamlit` and setting the page configuration.)*

4.  **Connect to your Database.**
    Upon launch, the application will prompt you to enter your database connection string (e.g., `mysql+pymysql://user:password@localhost:3306/db_name`) to establish the connection.

## Usage
A sample session with AXIS!

![Demo Gif](demo.gif)

## Roadmap
[Notion Live Development Roadmap](https://www.notion.so/2aca19089f628011811dfb6b9ddf5e52?v=2aca19089f6280babf85000c990d1371&source=copy_link)

## License
MIT

## Contact
For questions and comments please contact me via [my Linkedin profile](https://www.linkedin.com/in/deryakubraer).

## Acknowlegments:

This project, AXIS, wouldn't have been possible without some key people and my fur babies.

First, I want to give a massive thank you to my dear teacher, Nicolas Mirabet. He is absolutely excellent at his job. He listened, understood, gave me the necessary nudge when I needed it, and always showed me the right path. He is a visionary, incredibly patient, and it’s clear he genuinely loves what he does, which is why he’s so successful. Thank you for making the educational contents slightly less terrifying. And yeah, it is always a tuple Nik! 

Second, a huge thank you to my husband, Can Hosgor, for his support and compassion. He not only encouraged me to attend the bootcamp but also believed in me every step of the way. He was the rock who supported me through all the late nights and wiped away my tears when those impossible error messages felt like personal attacks. I hope he feels incredibly proud when he sees what I built with AXIS!

Finally, my deepest appreciation goes to my lovely cats Sütlaç and Pesto. While their main form of "compassion" involved demanding food, walking across my keyboard at critical moments, and silently judging me, their presence made the long hours bearable. Without them, the world is just... meeh.