# LLM-SPARQL : A HYBRID NEL AND NED FRAMEWORK

ABSTRACT:
-
This research tackles the complex issue of Named Entity Disambiguation (NED) by harnessing the power of Large Language Models (LLMs), such as Generative Pre-trained Transformers (GPTs), and integrating these with structured information from knowledge graphs like Wikidata. The overarching goal is to markedly enhance NED accuracy through a synergistic approach that combines the predictive prowess of advanced LLMs with the detailed semantic repositories of KGs. Our key innovation is the formulation of a novel methodology that employs SPARQL queries to methodically retrieve potential Uniform Resource Identifiers (URIs) from Wikidata. These URIs serve as candidate references for named entities. We then apply cutting-edge generative AI techniques to accurately match each entity's mention within texts to the most contextually relevant URI. This refined approach allows for a more sophisticated, context-aware resolution of entity references. We conducted extensive experiments to evaluate our method, which indicates a substantial achievemnet in performance, as evidenced by precision, recall, and F-measure. Impressively, our model achieves an F-measure of 96\% on the Wikidata-Disamb dataset, a meticulously curated benchmark specifically developed for robust, scalable evaluation of NED performance leveraging Wikidata entries.

Methodology:
-
<h2 align="center">
  Flow of Annotation Process:
  <img align="center" src="gpt-sparql.png" alt="...">
</h2>

CODE FILES:
-
- GPTEL.py: Contain all the functions for GPT. You can apply multiple function on your choice and requirement.
- SPARQEL.py: Contains the scripts and function to extract wikidata URIs through SPARQL Endpoint.
- NEL_proc.py: contains the main code to use GPTEL and SPARQEL functions for the task.

- llama2_candid.py: Contains the implemention of LLaMA2 model.
- llama3_candid.py: Contains the implemention with LLAMA3 model.


Directories:
-
- Data: Should download dataset in this directory. The link to the source paper is included.
- LLMs: Should download required llms in this directory. The links of applied variants of LLaMA model are included.

