# Bring in dependencies

import os
from apikey import openai_key, weather_api_key, pinecone_key
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import pinecone
import requests

# Set up API keys
openweathermap_api_key = weather_api_key
openseamap_api_key = os.environ.get('OPENSEAMAP_API_KEY')
wikitravel_api_key = os.environ.get('WIKITRAVEL_API_KEY')
gbif_api_key = os.environ.get('GBIF_API_KEY')
opencagedata_api_key = os.environ.get('OPENCAGEDATA_API_KEY')
marinetraffic_api_key = os.environ.get('MARINETRAFFIC_API_KEY')
worldbank_api_key = os.environ.get('WORLDBANK_API_KEY')
pinecone_api_key = pinecone_key
pinecone_index = "xyz_adventure_ideas"  # Replace with your Pinecone index name

# Set up Langchain
os.environ['OPENAI_API_KEY'] = openai_key
llm = OpenAI(temperature=0.9)


# Set up conversation memories
memory = ConversationBufferMemory(input_key='user_input', memory_key='chat_history')

# Set up prompt templates
booking_prompt_template = PromptTemplate(
    input_variables=['user_input'],
    template='TravelBot: {user_input}\nUser: {user_input}'
)

chatbot_chain = LLMChain(llm=llm, prompt=booking_prompt_template, verbose=False, output_key='response', memory=memory)

# Streamlit app framework
st.title('My Booking Chatbot')

# Chat history
chat_history = []

# Chatbot logic
user_input = st.text_input('Ask a question or provide a command')

if user_input:
    # Generate response using Langchain
    response = chatbot_chain.run(user_input)
    st.write(response)

# Helper functions for integrating open-source data
def get_weather_data(city):
     # Implement the logic to retrieve weather data from OpenWeatherMap using the provided API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermap_api_key}"
    response = requests.get(url)
    data = response.json()
    print(data)
    # Check if the 'weather' key is present in the response
    if 'weather' in data:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Prepare the weather information message
        weather_info = f"Weather in {city}:\n"
        weather_info += f"Description: {weather_description}\n"
        weather_info += f"Temperature: {temperature} K\n"
        weather_info += f"Humidity: {humidity}%\n"
        weather_info += f"Wind Speed: {wind_speed} m/s"

        return weather_info
    else:
        return f"Unable to retrieve weather information for {city}"
    
    pass

def get_seamap_data():
    # Implement the logic to retrieve data from OpenSeaMap using the provided API
    pass

def get_gbif_data():
    # Implement the logic to retrieve data from GBIF using the provided API
    pass

def get_opencage_data(query):
    # Implement the logic to retrieve data from OpenCageData using the provided API
    api_key = '66f8a507076c4f0c9074b1c7df8059d8'
    endpoint = 'https://api.opencagedata.com/geocode/v1/json'

    params = {
        'q': query,
        'key': api_key
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if data['results']:
        location = data['results'][0]['formatted']
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return location, latitude, longitude

    return None, None, None
    pass

def get_marinetraffic_data():
    # Implement the logic to retrieve data from MarineTraffic using the provided API
    pass

def get_worldbank_data():
    # Implement the logic to retrieve data from World Bank using the provided API
    pass

def search_adventure_ideas(query):
    # Search adventure ideas using Pinecone
    embeddings = pinecone_index.query(queries=[query])
    results = []
    for idx, score in embeddings[0].fetch():
        # Fetch details from your proprietary data based on the retrieved index IDs
        result = f"Adventure Idea {idx} (Score: {score})"
        results.append(result)
    return results

# Helper functions for Langchain integration
def generate_booking_response(user_input):
    return booking_chain.run(user_input)

# Set up Langchain
chatbot_chain = LLMChain(llm=llm, prompt=booking_prompt_template, verbose=False, output_key='response', memory=memory)

# Set up the booking chain
booking_template = PromptTemplate(
    input_variables=['user_input'],
    template='User: {user_input}\TravelBot:'
)
booking_memory = ConversationBufferMemory(input_key='user_input', memory_key='chat_history')
booking_llm = OpenAI(temperature=0.9)
booking_chain = LLMChain(llm=booking_llm, prompt=booking_template, verbose=False, output_key='response', memory=booking_memory)

# Main chatbot logic
if st.sidebar.button("Book a Trip"):
    destination = st.text_input('Enter your desired destination')
    # Implement the booking logic here based on the user's destination

if 'weather' in user_input.lower():
    city = st.text_input('Enter the city for weather information')
    # Display weather information to the user
    if city:
        weather_data = get_weather_data(city)
        if weather_data:
            weather_lines = weather_data.split('\n')
            for line in weather_lines:
                st.write(line)

    

if 'adventure' in user_input.lower():
    query = st.text_input('Enter your adventure idea query')
    adventure_ideas = search_adventure_ideas(query)
    # Display adventure ideas to the user

if any(keyword in user_input.lower() for keyword in ['geo', 'geocoding', 'location']):
    # Example usage
    query = st.text_input('Enter the query for geocoding')
    opencage_data = get_opencage_data(query)
    if opencage_data:
        if isinstance(opencage_data, tuple) and len(opencage_data) == 3:
            location, latitude, longitude = opencage_data
            st.write("Location:", location)
            st.write("Latitude:", latitude)
            st.write("Longitude:", longitude)
        else:
            opencage_lines = opencage_data.split('\n')
            for line in opencage_lines:
                st.write(line)
    else:
        st.write("No data found for the query.")


    # Display adventure ideas to the user

# Additional code for integrating other APIs and XYZ's proprietary data can be added here
