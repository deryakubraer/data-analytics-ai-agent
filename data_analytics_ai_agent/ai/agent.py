import json
from openai import OpenAI
from ai.tools import  get_data_df, display_chart
from ai.tools import TOOLS
import streamlit as st

def call_ai(messages_ai):
    llm_api_key = st.session_state.get("llm_api_key", "")
    selected_model = st.session_state.get("selected_model", "")

    # Initialize the OpenAI client
    # Pick a different API endpoint depending on the selected model
    if selected_model.startswith("gpt"):
        client = OpenAI(api_key=llm_api_key)
    elif selected_model.startswith("gemini"):
        client = OpenAI(api_key=llm_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    else:
        raise ValueError(f"Unsupported model: {selected_model}") # Fail fast for unsupported models

    # Make a ChatGPT API call with tool calling
    completion = client.chat.completions.create(
        model=selected_model,
        tools=TOOLS, # here we pass the tools to the LLM
        messages=messages_ai,
    )

    # Get the response from the LLM
    response = completion.choices[0].message

    # Parse the response to get the tool call arguments
    if response.tool_calls:
        # Process each tool call
        for tool_call in response.tool_calls:
            # Get the tool call arguments
            tool_call_arguments = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "get_data_df":
                stream_result = get_data_df(tool_call_arguments["sql_query"])
                return {'ai':{ "role": "assistant", "content": 'Table displayed successfully.' },
                        'streamlit': stream_result}
            
            # add graph tool call handling here if needed
            elif tool_call.function.name == "display_chart":
                stream_result = display_chart(tool_call_arguments["sql_query"], 
                                              tool_call_arguments["chart_type"],
                                              tool_call_arguments['explanation'],
                                              tool_call_arguments['x'],
                                              tool_call_arguments['y'],
                                              tool_call_arguments['color'])
                return {'ai':{ "role": "assistant", "content": 'Chart displayed successfully.' },
                        'streamlit': stream_result}
    else:
        # If there are no tool calls, return the response content
        return {'ai':{ "role": "assistant", "content": response.content },
                'streamlit': {'role': "assistant", "content": {"type": "text", "text": response.content}}}