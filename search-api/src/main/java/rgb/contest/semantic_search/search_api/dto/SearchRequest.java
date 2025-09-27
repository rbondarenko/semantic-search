package rgb.contest.semantic_search.search_api.dto;

import lombok.Data;

@Data
public class SearchRequest {
    private String query;
    private int limit = 10;
}
