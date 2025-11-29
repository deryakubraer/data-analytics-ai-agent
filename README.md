# AXIS | Data Intelligence 💠

## About The Project

**AXIS** is an **intelligent data agent panel** designed to provide **real-time, accelerated business intelligence** [1].

The application allows users to ask complex data questions using natural language [1, 2]. The system, which operates as a "senior data analyst" [2], instantly processes these queries and delivers visualized answers, either as charts or tables [1, 3].

AXIS automatically handles database connectivity, SQL generation, and visualization, following a strict set of rules to ensure safe query execution [3, 4].

### Key Features

*   **Intelligent Agent:** Uses advanced AI (GPT models) for tool calling to execute data tasks [5].
*   **Database Analysis:** Detects the SQL dialect (e.g., PostgreSQL, MySQL) and analyzes the database schema to ensure accurate query generation [2, 6].
*   **Visualizations:** Supports displaying results as tables (DataFrames) [7] or various chart types (line, bar, scatter, pie) using Plotly [7, 8]. Charts are styled using a specialized color palette (Gold, Cyan, Orchid, Orange, Silver) [9, 10].
*   **Secure Connection:** Requires a database connection key, which is handled securely using a password input type [11].
*   **Structured Feedback:** Provides concise technical summaries and explanations after generating charts [12, 13].

### Built With

This project relies on a modern data and AI stack:

*   **Python** (Base language)
*   **Anaconda** (Environment management)
*   **Streamlit** (Web application framework) [14]
*   **OpenAI** (LLM integration via client and API calls) [5, 14]
*   **Plotly** (Advanced chart generation) [14, 15]
*   **SQLAlchemy** (Database connection and SQL execution) [15]
*   **Pandas** (Data manipulation and DataFrame handling) [15]

---

# Getting Started

To run AXIS, you must first ensure you have the necessary Python environment set up and the required dependencies installed.

### Prerequisites

You need access to an OpenAI API key and a valid database connection string [11].

### Installation

Follow these steps to set up your project locally:

1.  **Clone the repository.**
    ```bash
    git clone https://github.com/deryakubraer/data-analytics-ai-agent.git
    
    cd data-analytics-ai-agent
    ```

2.  **Install Python dependencies** using the provided `requirements.txt` file (assuming standard installation practice, as complex libraries like SQLAlchemy and Plotly are used [14, 15]).
    ```bash
    pip install -r requirements.txt
    ```
 

3.  **Run the Streamlit application.**
    ```bash
    streamlit run app.py
    ```
    *(The main page configuration sets the app title to "AXIS | Data Intelligence" and uses a wide layout with a collapsed sidebar initially [9, 14]. The application file typically starts by importing `streamlit` and setting the page configuration [14].)*

4.  **Connect to your Database.**
    Upon launch, the application will prompt you to enter your database connection string (e.g., `mysql+pymysql://user:password@localhost:3306/db_name`) to establish the connection [1, 11].

## Usage
GIF

## Roadmap
[Notion linki]
*(This is a placeholder for your detailed roadmap link.)*

## License
MIT

## Contact
For questions and comments please contact me via [my Linkedin profile](https://www.linkedin.com/in/deryakubraer).

## Acknowlegments:

This project, AXIS, wouldn't have been possible without some key people and my fur babies.

First, I want to give a massive thank you to my dear teacher, Nicolas Mirabet. He is absolutely excellent at his job. He listened, understood, gave me the necessary nudge when I needed it, and always showed me the right path. He is a visionary, incredibly patient, and it’s clear he genuinely loves what he does, which is why he’s so successful. Thank you for making the educational contents slightly less terrifying. And yeah, it is always a tuple. 

Second, a huge thank you to my husband, Can Hosgor, for his support and compassion. He not only encouraged me to attend the bootcamp but also believed in me every step of the way. He was the rock who supported me through all the late nights and wiped away my tears when those impossible error messages felt like personal attacks. I hope he feels incredibly proud when he sees what we built with AXIS!

Finally, my deepest appreciation goes to my lovely cats Sütlaç and Pesto. While their main form of "compassion" involved demanding food, walking across my keyboard at critical moments, and silently judging me, their presence made the long hours bearable. Without them, the world is just... meeh.