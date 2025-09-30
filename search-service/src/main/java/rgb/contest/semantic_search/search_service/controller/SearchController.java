package rgb.contest.semantic_search.search_service.controller;

import rgb.contest.semantic_search.search_service.dto.SearchRequest;
import rgb.contest.semantic_search.search_service.dto.SearchResponse;
import rgb.contest.semantic_search.search_service.service.SearchService;
import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;

@RestController
@RequestMapping("/search")
@Tag(name = "Search", description = "Search API for semantic search operations")
public class SearchController {

    private final SearchService service;

    public SearchController(SearchService service) {
        this.service = service;
    }

    @PostMapping
    @Operation(
            summary = "Perform semantic search",
            description = "Executes a semantic search based on the provided search request"
    )
    @ApiResponses(value = {
            @ApiResponse(
                    responseCode = "200",
                    description = "Search completed successfully",
                    content = @Content(mediaType = "application/json", schema = @Schema(implementation = SearchResponse.class))
            ),
            @ApiResponse(responseCode = "400", description = "Invalid search request", content = @Content),
            @ApiResponse(responseCode = "500", description = "Internal server error", content = @Content)
    })
    public SearchResponse search(
            @Parameter(description = "Search request containing query parameters")
            @RequestBody SearchRequest request
    ) {
        return service.search(request);
    }
}
