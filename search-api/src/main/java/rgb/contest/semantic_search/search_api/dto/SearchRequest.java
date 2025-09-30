package rgb.contest.semantic_search.search_api.dto;
import io.swagger.v3.oas.annotations.media.Schema;

import lombok.Data;

@Schema(description = "Search request object")
@Data
public class SearchRequest {
    @Schema(description = "Search query text", example = "car tires")
    private String query;

    @Schema(description = "Maximum number of results to return", example = "5")
    private int limit = 10;
}