import json
import os

# References for each prompt (vereinheitlichte, beispielhafte Formatierung)
references = {
    "Explain the theory of relativity in simple terms.": (
        "NASA (n.d.). Einstein’s Theory of Relativity in simple terms. "
        "Retrieved from https://www.nasa.gov/"
    ),
    "Create a short story about a knight.": (
        "WritersDigest (n.d.). Creative Writing Techniques. "
        "Retrieved from https://www.writersdigest.com/"
    ),
    "What are the advantages of open-source projects?": (
        "OpenSource (n.d.). Advantages of Open-Source Projects. "
        "Retrieved from https://opensource.com/"
    ),
    "Write a Python function that outputs prime numbers up to 100.": (
        "Python.org (n.d.). Python Programming Documentation. "
        "Retrieved from https://www.python.org/doc/"
    ),
    "What is the difference between machine learning and deep learning?": (
        "Stanford University (n.d.). Understanding AI: Machine Learning vs. Deep Learning. "
        "Retrieved from https://www.stanford.edu/"
    ),
    "What are the key principles of quantum mechanics?": (
        "MIT OpenCourseWare (n.d.). Quantum Mechanics Basics. "
        "Retrieved from https://ocw.mit.edu/"
    ),
    "Explain how photosynthesis works in plants.": (
        "Khan Academy (n.d.). Photosynthesis Explained. "
        "Retrieved from https://www.khanacademy.org/"
    ),
    "Describe the process of natural selection in evolutionary biology.": (
        "Britannica (n.d.). Charles Darwin’s Theory of Natural Selection. "
        "Retrieved from https://www.britannica.com/"
    ),
    "What is the significance of the Renaissance period in European history?": (
        "History.com (n.d.). Renaissance History. "
        "Retrieved from https://www.history.com/"
    ),
    "What is the Pythagorean theorem, and how is it used?": (
        "MathIsFun (n.d.). Basics of the Pythagorean Theorem. "
        "Retrieved from https://www.mathsisfun.com/"
    ),
    "Summarize the plot of a Shakespearean play of your choice.": (
        "SparkNotes (n.d.). Shakespeare Play Summaries. "
        "Retrieved from https://www.sparknotes.com/shakespeare/"
    ),
    "What is the main cause of the First World War?": (
        "BBC (n.d.). World War I Causes: BBC History. "
        "Retrieved from https://www.bbc.co.uk/history/"
    ),
    "Describe the structure of an atom and the role of electrons.": (
        "Chemistry LibreTexts (n.d.). Atomic Structure. "
        "Retrieved from https://chem.libretexts.org/"
    ),
    "Write a SQL query that finds all customers older than 25.": (
        "W3Schools (n.d.). SQL Query Basics. "
        "Retrieved from https://www.w3schools.com/sql/"
    ),
    "Explain the importance of data privacy in the digital age.": (
        "GDPR (n.d.). Data Privacy and Security: EU GDPR Resources. "
        "Retrieved from https://gdpr.eu/"
    ),
    "How do blockchain technologies work?": (
        "IBM (n.d.). Blockchain Explained: IBM Blockchain Resources. "
        "Retrieved from https://www.ibm.com/blockchain"
    ),
    "What are the effects of climate change on global ecosystems?": (
        "IPCC (n.d.). Climate Change Impact: IPCC Reports. "
        "Retrieved from https://www.ipcc.ch/"
    ),
    "Create a fictional dialogue between a historian and a time traveler.": (
        "MasterClass (n.d.). Creative Writing Guide. "
        "Retrieved from https://www.masterclass.com/"
    ),
    "What is the role of mitochondria in the cell?": (
        "Khan Academy (n.d.). Cell Biology and Mitochondria. "
        "Retrieved from https://www.khanacademy.org/"
    ),
    "Describe how a neural network processes input data.": (
        "DeepLearning.AI (n.d.). Neural Networks Overview. "
        "Retrieved from https://www.deeplearning.ai/"
    ),
    "What are the advantages and disadvantages of space exploration?": (
        "NASA (n.d.). Benefits and Drawbacks of Space Exploration. "
        "Retrieved from https://www.nasa.gov/"
    ),
    "Write a Python script that reads a file and counts the words.": (
        "Python.org (n.d.). Python File Handling Documentation. "
        "Retrieved from https://www.python.org/doc/"
    ),
    "Explain the key differences between capitalism and socialism.": (
        "Investopedia (n.d.). Capitalism vs. Socialism Explained. "
        "Retrieved from https://www.investopedia.com/"
    ),
    "What is the significance of Ada Lovelace in computer science?": (
        "Britannica (n.d.). Ada Lovelace Biography. "
        "Retrieved from https://www.britannica.com/"
    ),
    "What are the psychological effects of prolonged isolation?": (
        "APA (n.d.). Psychological Effects of Isolation: American Psychological Association. "
        "Retrieved from https://www.apa.org/"
    ),
    "How does the immune system respond to a viral infection?": (
        "NIH (n.d.). Immune System Basics. "
        "Retrieved from https://www.nih.gov/"
    ),
    "Write a persuasive argument for the use of renewable energy.": (
        "IRENA (n.d.). Renewable Energy Resources. "
        "Retrieved from https://www.irena.org/"
    ),
    "Create a summary of the book '1984' by George Orwell.": (
        "SparkNotes (n.d.). 1984 Book Summary. "
        "Retrieved from https://www.sparknotes.com/"
    ),
    "What are the common patterns in machine learning algorithms?": (
        "Coursera (n.d.). Machine Learning Patterns: ML Courses. "
        "Retrieved from https://www.coursera.org/"
    ),
    "Explain the difference between supervised and unsupervised learning.": (
        "DeepLearning.AI (n.d.). AI Learning Methods. "
        "Retrieved from https://www.deeplearning.ai/"
    ),
    "What is the Turing Test, and how does it measure artificial intelligence?": (
        "AlanTuring.net (n.d.). Turing Test Explained. "
        "Retrieved from http://www.alanturing.net/"
    ),
    "Describe the cultural impact of the Renaissance on modern society.": (
        "Khan Academy (n.d.). Renaissance Impact. "
        "Retrieved from https://www.khanacademy.org/"
    ),
    "What are the principles of democratic governance?": (
        "United Nations (n.d.). Democratic Principles. "
        "Retrieved from https://www.un.org/"
    ),
    "Explain the process of photosynthesis in detail.": (
        "Biology LibreTexts (n.d.). The Photosynthesis Process. "
        "Retrieved from https://bio.libretexts.org/"
    ),
    "How does a search engine like Google index the web?": (
        "Google Developers (n.d.). Understanding Search Engine Indexing. "
        "Retrieved from https://developers.google.com/"
    ),
    "What is the significance of the Higgs boson in physics?": (
        "CERN (n.d.). Higgs Boson Discovery. "
        "Retrieved from https://home.cern/"
    ),
    "Describe the evolution of language in early human civilizations.": (
        "Linguistics Society of America (n.d.). Language Evolution. "
        "Retrieved from https://www.linguisticsociety.org/"
    ),
    "How does encryption work in secure messaging apps?": (
        "EFF (n.d.). Encryption Basics. "
        "Retrieved from https://www.eff.org/"
    ),
    "Write a story about an astronaut on Mars discovering life.": (
        "WritersDigest (n.d.). Creative Writing Techniques. "
        "Retrieved from https://www.writersdigest.com/"
    ),
    "What are the ethical concerns surrounding genetic modification?": (
        "Nature (n.d.). Genetic Modification Ethics. "
        "Retrieved from https://www.nature.com/"
    ),
    "Explain how a car engine converts fuel into motion.": (
        "HowStuffWorks (n.d.). Internal Combustion Engine Basics. "
        "Retrieved from https://auto.howstuffworks.com/"
    ),
    "What are the cultural differences between Eastern and Western philosophies?": (
        "Stanford Encyclopedia of Philosophy (n.d.). Eastern vs. Western Philosophy. "
        "Retrieved from https://plato.stanford.edu/"
    ),
    "How does quantum computing differ from classical computing?": (
        "IBM Quantum (n.d.). Quantum vs. Classical Computing. "
        "Retrieved from https://www.ibm.com/quantum-computing/"
    ),
    "What are the main components of a healthy diet?": (
        "WHO (n.d.). Healthy Diet Guidelines. "
        "Retrieved from https://www.who.int/"
    ),
    "Explain the importance of biodiversity in ecosystems.": (
        "WWF (n.d.). Biodiversity and Ecosystems. "
        "Retrieved from https://www.worldwildlife.org/"
    ),
    "Describe the history of the internet and its evolution.": (
        "Internet Society (n.d.). History of the Internet. "
        "Retrieved from https://www.internetsociety.org/"
    ),
    "What are the different stages of project management?": (
        "PMI (n.d.). Project Management Stages. "
        "Retrieved from https://www.pmi.org/"
    ),
    "Write a Python function to scrape data from a web page.": (
        "BeautifulSoup (n.d.). Documentation for Web Scraping in Python. "
        "Retrieved from https://www.crummy.com/software/BeautifulSoup/"
    ),
    "What are the long-term effects of plastic pollution in oceans?": (
        "Ocean Conservancy (n.d.). Plastic Pollution Impact. "
        "Retrieved from https://oceanconservancy.org/"
    ),
    "Explain how machine learning can be used in healthcare.": (
        "Stanford Medicine (n.d.). AI in Healthcare. "
        "Retrieved from https://med.stanford.edu/"
    ),
    "What is the concept of time dilation in Einstein's theory?": (
        "NASA (n.d.). Time Dilation Explained: Relativity Resources. "
        "Retrieved from https://www.nasa.gov/"
    ),
    "Describe how democracy differs from autocracy.": (
        "Britannica (n.d.). Democracy vs. Autocracy. "
        "Retrieved from https://www.britannica.com/"
    ),
    "What are the advantages of multilingualism in society?": (
        "European Commission (n.d.). Multilingualism Benefits. "
        "Retrieved from https://ec.europa.eu/"
    ),
    "Explain the basics of game theory and provide an example.": (
        "Khan Academy (n.d.). Game Theory Basics. "
        "Retrieved from https://www.khanacademy.org/"
    ),
    "Describe the cultural and historical significance of the Great Wall of China.": (
        "History.com (n.d.). Great Wall of China. "
        "Retrieved from https://www.history.com/"
    ),
    "What is the role of literature in shaping societal values?": (
        "JSTOR (n.d.). Literature and Society. "
        "Retrieved from https://www.jstor.org/"
    ),
    "How do satellites help in disaster management?": (
        "UN-SPIDER (n.d.). Satellites in Disaster Response. "
        "Retrieved from https://www.un-spider.org/"
    ),
    "Write a Python script that converts temperature from Celsius to Fahrenheit.": (
        "Python.org (n.d.). Python Basics. "
        "Retrieved from https://www.python.org/doc/"
    ),
    "What are the different forms of renewable energy?": (
        "IRENA (n.d.). Different Types of Renewable Energy. "
        "Retrieved from https://www.irena.org/"
    ),
    "Explain the significance of the moon landing in 1969.": (
        "NASA (n.d.). Moon Landing History: Apollo Resources. "
        "Retrieved from https://www.nasa.gov/"
    ),
    "What are the differences between Roman and Greek architecture?": (
        "Khan Academy (n.d.). Roman vs. Greek Architecture. "
        "Retrieved from https://www.khanacademy.org/"
    ),
    "Describe the economic impact of pandemics throughout history.": (
        "World Bank (n.d.). Pandemic Economics. "
        "Retrieved from https://www.worldbank.org/"
    ),
    "What is the importance of financial literacy in modern society?": (
        "Investopedia (n.d.). Financial Literacy Basics. "
        "Retrieved from https://www.investopedia.com/"
    ),
    "How does artificial intelligence impact job markets?": (
        "OECD (n.d.). AI and Jobs Research. "
        "Retrieved from https://www.oecd.org/"
    ),
    "Explain how photosynthesis differs between C3 and C4 plants.": (
        "Biology LibreTexts (n.d.). C3 vs. C4 Photosynthesis. "
        "Retrieved from https://bio.libretexts.org/"
    ),
    "What are the basic principles of quantum entanglement?": (
        "CERN (n.d.). Quantum Entanglement Basics. "
        "Retrieved from https://home.cern/"
    ),
    "Write a Python function to generate Fibonacci numbers.": (
        "GeeksforGeeks (n.d.). Python Fibonacci Example. "
        "Retrieved from https://www.geeksforgeeks.org/"
    ),
    "Explain the process of human memory formation.": (
        "NIH (n.d.). Human Memory Formation. "
        "Retrieved from https://www.nih.gov/"
    ),
    "What is the impact of social media on mental health?": (
        "APA (n.d.). Social Media and Mental Health. "
        "Retrieved from https://www.apa.org/"
    ),
    "Describe the history and cultural significance of the Olympic Games.": (
        "Olympics.org (n.d.). Olympics History. "
        "Retrieved from https://www.olympic.org/"
    ),
    "Generate a D&D character with a backstory and traits.": (
        "DnDBeyond (n.d.). D&D Character Creation. "
        "Retrieved from https://www.dndbeyond.com/"
    )
}

directory = "/home/luna/5BHWII/Diplomarbeit/SAIPIA/Diploma-thesis/model-evaluation/Scores"
output_prefix = "processed_"

def add_references(input_file, output_file, references):
    with open(input_file, "r") as file:
        data = json.load(file)

    for entry in data:
        prompt = entry.get("Prompt", "")
        entry["Reference"] = references.get(prompt, "No reference available")

    with open(output_file, "w") as out_file:
        json.dump(data, out_file, indent=4)

    print(f"Updated JSON saved to {output_file}")

for filename in os.listdir(directory):
    if filename.endswith(".json") and not filename.startswith(output_prefix):
        file_path = os.path.join(directory, filename)
        output_path = os.path.join(directory, output_prefix + filename)
        add_references(file_path, output_path, references)
