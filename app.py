from openai import OpenAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
import json
import asyncio
llm = OpenAI()
import streamlit as st
import pandas as pd



final =[]
with st.sidebar:
    



    function_descriptions = [
        {
            "name": "get_property_details",
            "description": "Get the details of the property user wants to buy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city where the apartment is located."
                    },
                    "area": {
                        "type": "string",
                        "description": "The area within the city where the apartment is located. User might input more than one preferred area, separated by a comma."
                    },
                    "apartment_type": {
                        "type": "string",
                        "description": "The type of apartment (e.g., studio, 1BHK, 2BHK, etc.)."
                    },
                    "budget": {
                        "type": "number",
                        "description": "The budget for buying the apartment."
                    },
                    "number_of_bedrooms": {
                        "type": "string",
                        "description": "Number of bedrooms"
                    },
                    "size": {
                        "type": "string",
                        "description": "Size of the apartment needed , in marlas. i.e 2 Marla , 3 Marla"
                    },
                    "number_of_bathrooms": {
                        "type": "string",
                        "description": "Number of bathrooms"
                    }
                },
                "required": ["city", "apartment_type", "budget"],
            },
        }
    ]


# user_input = "I am looking for apartments under 30 million in islamabad f11"
input = st.text_input(placeholder='I am looking for apartments under 30 million in islamabad f11',label='Enter prompt here')

if user_input:

    st.markdown(

        """
        <style>
        body {
        
        
            background-color: #EC7063; /* Replace with your desired color */
        }

             </style>
        """,
        unsafe_allow_html=True
    )

    system_prompt = """You are an assistant that helps users find their desired apartments. Your job is to extract the needed details from the prompt.
    Make sure that the user atleast names the city in the input prompt. Ask for clarification if a user request is ambiguous.
    If user talks about anything else than about apartments , say you are not supposed to answer it. """
    completion = llm.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input}
        ],
        functions=function_descriptions,
        function_call="auto"
    )

    

    output = completion.choices[0].message
    

    function_arguments = json.loads(output.function_call.arguments)

    # Format the extracted details
    formatted_output = f"""
    City: {function_arguments['city']}
    Areas: {function_arguments.get('area', 'Not specified')}
    Apartment Type: {function_arguments['apartment_type']}
    Budget: {function_arguments['budget']}
    Number of Bedrooms: {function_arguments.get('number_of_bedrooms','Not specified')}
    Number of Batrooms: {function_arguments.get('number_of_bathrooms','Not specified')}
    Size: {function_arguments.get('size','Not specified')}
    """

    table_data = {
    "City": [function_arguments['city']],
    "Areas": [function_arguments.get('area', 'Not specified')],
    "Apartment Type": 'Any',
    "Budget": [function_arguments['budget']],
    "Number of Bedrooms": [function_arguments.get('number_of_bedrooms', 'Not specified')],
    "Number of Bathrooms": [function_arguments.get('number_of_bathrooms', 'Not specified')],
    "Size": [function_arguments.get('size', 'Not specified')],
    }

    with st.popover(label="Extracted details"):
        st.table(table_data)

    generate_prompt = PromptTemplate(
        template="""
    You are an AI assistant which helps users find their dream property.
    We will be using 'Zameen.com' website to find the user's needed type of property.
    You are provided with the description of user needs, your job is to convert it into a url like the one in examples below:

    Here are some URL examples along with their input details:

    City: "islamabad"
    Areas: "f10"
    Apartment Type: any
    Budget: 30
    Number of Bedrooms: 5
    Size in Marla: 30
    Generated URL: https://www.graana.com/sale/residential-properties-sale-f-10-islamabad-1-240/?page=1&maxPrice=300000000&maxSize=30&sizeUnit=Marla&bed=5

    If there is only one 'area' mentioned , GENERATE ONE LINK ONLY.

    If there are more than one 'areas' mentioned, then generate more than one url for each area.
    If you are generating more than one url , then seperate each url with a comma.

    Needed property description:
    City: {city}
    Areas: {areas}

    Budget: {budget}
    Number of Bedrooms: {number_of_bedrooms}
    Size in Marla: {size}

    Answer:
    """,
        input_variables=["city", "areas",  "budget", "number_of_bedrooms", "size"]
    )

   
    formatted_output_data = {
        "city": function_arguments['city'],
        "areas": function_arguments.get('area', 'Not specified'),
        
        "budget": function_arguments['budget'],
        "number_of_bedrooms": function_arguments.get('number_of_bedrooms','Not specified'),
        "size": function_arguments.get('size','Not specified'),
        "number of bathrooms ": function_arguments.get('number_of_bathrooms','Not specified'),

    }

   
    prompt = generate_prompt.format(**formatted_output_data)


    #llm call
    completion_prompt = llm.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
        ]
    )

    response = completion_prompt.choices[0].message.content



    url_list = []
    if len(url_list)==1:
        url_list=url_list[:-1]


    url_list = [url.strip() for url in response.split(",")]
    remove_dup = list( dict.fromkeys(url_list) )
    final_list_url= list( dict.fromkeys(remove_dup) )
    for u in final_list_url:
        st.write("For more details : ", u)

    from links import get_final_list_of_links
    property_links = get_final_list_of_links(final_list_url)

    final_list_url = list(dict.fromkeys(property_links))



    import asyncio
    from dotenv import load_dotenv
    import os
    from langchain_openai import ChatOpenAI
    from langchain.chains import create_extraction_chain
    from web_scrapper import run_playwright

    load_dotenv()
    openai_key = os.getenv("openai_key")


    schema = {
        "properties": {
            "PKR": {"type": "string"},
            "Number of bedrooms": {"type": "string"},
            "Size in Marlas/Sqft": {"type": "string"},
            "Features": {"type": "string"},
            "Condition": {"type": "string"},
        },
        'required': ['PKR', 'Number of bedrooms', 'Size in Marlas/Sqft', 'Features', 'Condition']
        }
    
    
    
    async def scrape_and_extract(url):
        site_data = await run_playwright(url)
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=openai_key)
        extraction_chain = create_extraction_chain(schema, llm)
        result = extraction_chain.run(site_data)
        return result

    async def scrape_and_extract(url):
        
        site_data = await run_playwright(url)
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=openai_key)
        extraction_chain = create_extraction_chain(schema, llm)
        result = extraction_chain.run(site_data)
        return result
    
    print(final_list_url)

    async def main():

        results = []
        for url in final_list_url:
            result = await scrape_and_extract(url)
            results.append(result)
        return results

                

    #Execute async 
    final = asyncio.run(main())
    if final:
        for i, current_property in enumerate(final):

            df = pd.DataFrame(current_property)
            df.index = [f'Property {i+1}' for i in range(len(df.index))]  
            df_transposed = df.T  
            st.write(df_transposed)  






