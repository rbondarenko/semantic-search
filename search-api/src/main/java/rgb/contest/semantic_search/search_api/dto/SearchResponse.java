package rgb.contest.semantic_search.search_api.dto;

import rgb.contest.semantic_search.search_api.model.Product;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;

@Data
@AllArgsConstructor
public class SearchResponse {
    private List<Product> results;
}
