# Problem Statement 

Design and implement a Semantic Search capability for an e-commerce application. 
The problem is broken into two parts - (1) data engineering pipeline and (2) the search engine.

1. Data engineering pipeline -
   - Refer to this open source dataset of Amazon products. Ingest the data to a database of your choice, 
   which should have the vector search capability. 
   - Choose an LLM model of your choice from https://huggingface.co/ and deploy its inference endpoint 
   as a service, preferably in an ECS Fargate cluster. 
   - The ingested data should have vector fields which could be generated on certain fields of your choice, 
   they should be relevant to the searchable fields. 
2. Search Engine - 
   - Implement a POST API using Java Spring Boot which should take a search string as request body. 
   - The API should be able to perform a vector search against the database table where the product metadata 
      along with the vector field is already ingested. 
   - The result should be sorted in order of relevance of the search terms. 

3. Bonus - 
   - fine tune the model to improve the relevancy of retrieval and show the improvement in relevancy using a metric.