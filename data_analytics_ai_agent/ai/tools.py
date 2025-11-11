import os
import uuid
import streamlit as st
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()

# Define the tools
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                    },
                    "required": ["location"]
                },
            },
    },
    {
        "type": "function",
        "function": {
            "name": "get_data_df",
            "description": "Get data from the database and return a pandas dataframe",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string"}
                },
                "required": ["sql_query"]
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "display_chart",
            "description": "Display a pandas charts in the Streamlit app",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string"}
                },
                "required": ["sql_query"]
            },
        },
    }
]

# Define the weather tool python function
def get_weather(location):
    # Here we simulate the weather function with hardcoded values, just for testing
    return f"The weather in {location} is sunny and 22°C"

# Define the get_data_df tool python function
def get_data_df(sql_query):
    # Create SQL engine
    password = os.getenv("DB_PASSWORD")
    connection_string = 'mysql+pymysql://root:' + password + '@localhost/sakila'
    engine = create_engine(connection_string)
    # Execute query and create dataframe
    with engine.connect() as connection:    
        sql_query = text(sql_query)
        result = connection.execute(sql_query)
        df = pd.DataFrame(result.all())
        # Show the SQL query
        expander = st.expander("SQL Query")
        expander.write(sql_query)
        # Show the dataframe
        st.dataframe(df)
    return "Found the data you were looking for."

#  Define a graphic tool for displaying dataframes in Streamlit

def display_chart(sql_query):
    print("Displaying chart with query:", sql_query)
    try:
# Create SQL engine
        password = os.getenv("DB_PASSWORD")
        connection_string = 'mysql+pymysql://root:' + password + '@localhost/sakila'
        engine = create_engine(connection_string)
        # Execute query and create dataframe
        with engine.connect() as connection:    
            sql_query_obj = text(sql_query)
            result = connection.execute(sql_query_obj)
            columns = result.keys()
            rows = result.fetchall()
            df = pd.DataFrame(rows, columns=columns)
            # Show the SQL query
            expander = st.expander("Chart SQL Query")
            expander.code(sql_query,language="sql")
            # Check if dataframe has data
            if df.empty:
                st.warning("No data returned from query")
                return "Query returned no data to chart."
            # Show the chart
            if len(df.columns) > 1:
                chart_df = df.set_index(df.columns[0])
                st.line_chart(chart_df)
            else:
                st.line_chart(df)
        
            return f"Successfully displayed a line chart with {len(df)} data points and {len(df.columns)} columns."

    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return f"Error creating chart: {str(e)}"

