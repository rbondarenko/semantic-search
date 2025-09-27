package rgb.contest.semantic_search.search_api.controller;

import rgb.contest.semantic_search.search_api.dto.SearchRequest;
import rgb.contest.semantic_search.search_api.dto.SearchResponse;
import rgb.contest.semantic_search.search_api.service.SearchService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/search")
public class SearchController {

    private final SearchService service;

    public SearchController(SearchService service) {
        this.service = service;
    }

    @PostMapping
    public SearchResponse search(@RequestBody SearchRequest request) {
        return service.search(request);
    }
}
