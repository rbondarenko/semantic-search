package rgb.contest.semantic_search.search_api.service;

import lombok.extern.log4j.Log4j2;
import rgb.contest.semantic_search.search_api.dto.SearchRequest;
import rgb.contest.semantic_search.search_api.dto.SearchResponse;
import rgb.contest.semantic_search.search_api.model.Product;
import rgb.contest.semantic_search.search_api.repository.ProductJdbcRepository;
import rgb.contest.semantic_search.search_api.repository.ProductRepository;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Log4j2
public class SearchService {

    private final ProductJdbcRepository repository;
    private final RestTemplate restTemplate;
    private final String embeddingUrl; // LLM service URL

    public SearchService(ProductJdbcRepository repository) {
        this.repository = repository;
        this.restTemplate = new RestTemplate();
        this.embeddingUrl = System.getenv("LLM_ENDPOINT"); // passed via ECS task env var
    }

    public SearchResponse search(SearchRequest request) {
        var payload = new java.util.HashMap<String, String>();
        payload.put("text", request.getQuery());

        @SuppressWarnings("unchecked")
        var response = restTemplate.postForObject(embeddingUrl + "/embed", payload, java.util.Map.class);
        var embedding = (List<Double>) response.get("embedding");

        String embeddingVector = embedding.stream()
                .map(Object::toString)
                .collect(Collectors.joining(",", "[", "]"));

        log.warn("Embeddings string: {}", embeddingVector);

        List<Product> results = repository.searchByEmbedding(embeddingVector, request.getLimit());
        return new SearchResponse(results, results.size());
    }
}
