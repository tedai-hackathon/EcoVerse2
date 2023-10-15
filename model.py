from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
import os
import replicate
import re


os.environ["OPENAI_API_KEY"] = "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"
os.environ["REPLICATE_API_TOKEN"] = "r8_TWs3Bhg1pYdQKkvrhyeTEnPOYpI30lu0Lc7Oh"
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


def get_usable_area(user_input_string):
    llm_output = chat(
        [
            HumanMessage(
                content=f"You are a helpful AI assistant. User has provided a textual description of usable area for installing a solar panel. {user_input}. Extract the usable area in sq ft from the description: "
            )
        ]
    )
    # return float(llm_output)
    return 100


def get_total_area(user_input_string):
    llm_output = chat(
        [
            HumanMessage(
                content=f"You are a helpful AI assistant. User has provided a textual description of usable area for installing a solar panel. {user_input}. Extract the total area in sq ft from the description: "
            )
        ]
    )
    # return float(llm_output)
    return 100


def get_area_llava(image_data):
    prompt_text = "Extract the land area in square meters in this image. Provide only the number in square meters in the answer without any text"
    output = replicate.run(
        "yorickvp/llava-13b:6bc1c7bb0d2a34e413301fee8f7cc728d2d4e75bfab186aa995f63292bda92fc",
        input={"image": image_data, "prompt": prompt_text, "temparature": 0},
    )
    return list(output)[1]


def extract_cost(input_string):
    # Define a regular expression pattern to match the cost value
    pattern = r'COST: (\d{1,3}(?:,\d{3})*(?:\.\d+)?) USD'

    # Search for the pattern in the input string
    match = re.search(pattern, input_string)

    # Extract and convert the matched cost value to a floating-point number
    if match:
        cost_str = match.group(1).replace(',', '')  # Remove commas from the cost string
        cost_float = float(cost_str)
        return cost_float
    else:
        return None


# Solar Panel Installation Cost data pulled from the https://www.irena.org/Data/View-data-by-topic/Costs/Solar-costs
install_cost_data = """
Figure 3.5 Detailed breakdown of utility-scale solar PV total installed costs by country, 2019																						
																					
	Total installed cost (2019 USD/kW)																					
		Category	Cost Component	Russian Federation	Japan	Canada	South Africa	Argentina	Brazil	Republic of Korea	Mexico	Australia	United States	Indonesia	United Kingdom	Saudi Arabia	France	Turkey	Germany	Italy	China	India
		Module and inverter hardware	Modules	399.4	450.8	554.1	557.0	340.0	306.0	339.5	274.1	293.7	358.1	410.3	362.2	282.1	237.0	358.5	374.9	357.2	266.6	277.9
			Inverters	100.0	223.7	69.1	89.8	91.7	71.2	67.2	58.8	62.5	68.4	31.3	54.8	72.9	71.6	63.3	53.6	50.5	42.2	44.4
		"BoS
hardware"	Racking and mounting	109.6	116.5	118.3	108.5	78.1	182.0	92.2	122.4	161.3	113.7	121.9	47.2	56.2	98.0	47.4	85.4	65.0	8.7	31.3
			Grid connection	192.5	112.1	92.3	53.4	95.2	60.1	83.5	81.3	62.2	61.8	92.0	62.1	36.5	138.7	44.7	82.0	58.5	61.7	29.4
			Cabling/ wiring	78.5	69.9	39.3	47.8	67.4	59.8	65.3	55.3	56.5	42.5	50.4	39.7	21.2	47.2	26.9	29.8	30.4	33.4	29.3
			Safety and security	21.9	19.9	17.2	22.7	12.6	33.5	22.2	22.7	33.3	18.7	34.5	14.4	10.4	11.4	9.4	12.9	8.7	6.4	21.3
			Monitoring and control	15.2	18.1	5.2	25.3	9.4	36.5	12.7	23.0	41.6	16.6	26.3	5.9	8.7	5.3	6.0	2.6	3.5	2.2	0.7
		Installation	Mechanical installation	230.5	456.2	125.7	46.1	84.3	171.6	67.0	107.8	186.6	180.2	23.3	98.3	75.6	133.9	49.6	76.5	41.7	74.5	31.2
			Electrical installation	215.6	292.1	42.0	31.4	101.0	95.2	45.2	45.7	83.4	68.3	18.2	73.0	28.5	39.6	32.1	26.1	20.0	34.5	14.6
			Inspection	26.8	34.7	7.6	3.3	10.6	8.7	8.9	15.5	8.1	21.4	6.6	12.2	11.6	2.8	5.6	5.3	2.0	25.6	3.7
		Soft costs	Margin	212.8	123.7	202.0	104.0	144.2	65.1	197.2	260.9	86.7	173.3	139.6	63.1	217.4	116.7	99.4	99.1	104.1	91.1	25.6
			Financing costs	156.6	63.5	13.3	60.6	110.6	41.2	76.1	35.4	43.0	19.8	63.9	66.0	38.3	4.0	61.9	5.5	21.0	73.3	40.6
			System design	65.7	5.1	75.4	79.5	9.9	62.7	24.4	32.1	53.5	22.8	35.1	17.5	30.5	21.6	13.4	36.4	34.4	30.1	19.9
			Permitting	192.7	50.2	7.5	58.1	122.4	37.5	83.1	15.6	38.2	8.9	54.6	69.4	15.9	31.9	60.1	4.3	22.8	11.5	14.2
			Incentive application	84.6	27.2	21.7	18.8	29.8	11.1	58.3	72.0	10.2	38.6	33.6	28.0	75.6	15.1	37.4	0.9	4.5	18.7	21.9
			Costumer acquisition	14.4	6.2	13.2	14.8	4.8	13.0	9.4	15.7	14.8	7.5	16.1	3.7	15.0	4.1	5.3	3.7	6.0	14.1	12.2

"""


# returns the cost of installing given number of solar panels
def get_cost_of_installing(number_of_panels, country):
    system_prompt = """
    ---BEGIN FORMAT TEMPLATE---
    Given this table of costs of installing a solar panel, what is the cost of installing ${NUMBER OF PANELS} solar panels for ${COUNTRY} ? You can assume each panel produces 0.3kW
    ${TABLE}
    COST: ${FLOATING POINT NUMBER}
    ---END FORMAT TEMPLATE---
    ---BEGIN USER INPUT---
    """
    prompt_text = f"Given this table of costs of installing a solar panel, what is the cost of installing {number_of_panels} solar panels for {country} ? You can assume each panel produces 0.3kW"
    output_format = "COST: "
    llm_output = chat(
        [
            HumanMessage(
                content=f"{system_prompt} {prompt_text} {install_cost_data} {output_format} "
            )
        ]
    )
        
    return extract_cost( llm_output.content )