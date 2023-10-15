# EcoVerse
**Problem statement:** How do we get more people using renewable energy sources in a sustainable manner? How do we help communities and individuals quickly determine a renewable energy project’s viability with the help of AI? Our solution is aligned with the UN SGD (“United Nations Sustainable Development Goals”) 7, “Ensure access to affordable, reliable, sustainable and modern energy for all.” 

**Solution:** Our solution aims to help analyze the potential for renewable energy generation in your surroundings and make recommendations for how to best optimize renewable energy for your location. The solution also compares the cost savings from installing and using renewable energy versus the traditional grid electricity pricing of the area. These tools could open up frontier markets where there is potential for wind and solar farms, but there is a need for a catalyst to make development decisions easier and quicker. 

**Our Target User**:
Our target user is part of the 840 million people around the world who are living in "energy poverty."  We want to make it simple for them to access information on the first introduction to sustainable energy, make it an easy step for figuring out next steps on equipment requirements based on square footage available and then allow the user to approach a crowdfunding opportunity to raise funds for the installation.  
This tool could also open up frontier markets where there is potential for wind and solar farms, but there is a need for a catalyst to make development decisions easier and quicker. 

**What does it do**: 
1.	Point camera and take photo of area such as a rooftop, the AI can calculates sq meters of the area available for solar panel installation on a rooftop. (Allow user to upload photo and then the query tool responds with how many solar panels needed.)
2. LLM provides feedback on recommendations on how many solar panels to deploy, the cost, and the ROI. 
3.	Provide a dashboard of weather metrics that are conducive to renewable energy such as solar radiance and wind speed.


For the photo data: we look at a matrix of vectors with 3 values, RGB. Computer reads the matrix, we give this matrix of number to text based LLM, we can ask how many pixels are of the same color. Sq m. of color most represented in this photo. Length and distance, and boundaries are analyzed. 

With real-time updates to the data, the dashboard will make it easy for energy communities to gain valuable insights and make faster decisions.  

With the rising global population and the increasing demand for energy, it is crucial to find sustainable and accessible solutions that can bridge the energy gap. The lack of access to electricity is a significant challenge faced by many communities around the world, especially those living in energy poverty.

Conventional power infrastructure often fails to reach remote and impoverished regions, leaving communities in darkness.  EcoVerse makes it easier to take the first step to help with bringing power generation and light to those communities around the world. 

Plans include developing a crowdfunding feature to allow those in off-grid locations and "energy poverty" to raise funds to install their sustainable energy projects.
Ecoverse AI - Optimizing renewable Energy Usage


To run the application 
1. Go to the project root dir
2. Install the dependencies, `pip install -r requirements.txt`
3. Update the Open-ai API Key in model.py
4. Run the server, `streamlit run main.py`



