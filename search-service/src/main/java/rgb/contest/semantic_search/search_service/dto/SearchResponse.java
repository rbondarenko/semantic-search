package rgb.contest.semantic_search.search_service.dto;

import rgb.contest.semantic_search.search_service.model.Product;
import io.swagger.v3.oas.annotations.media.Schema;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;

@Data
@AllArgsConstructor
@Schema(description = "Search response object")
public class SearchResponse {
    @Schema(description = "List of search results")
    private List<Product> results;

    @Schema(description = "Total number of results found", example = "10")
    private Integer totalCount;
}