package rgb.contest.semantic_search.search_service.repository;

import rgb.contest.semantic_search.search_service.model.Product;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ProductRepository extends JpaRepository<Product, Long> {

    // Custom query using pgvector similarity operator (<->)
    // asin, title, department, description, embedding
    @Query(value = """
        SELECT p.*
        FROM products p
        ORDER BY p.embedding <-> CAST(?1 AS vector)
        LIMIT ?2
        """, nativeQuery = true)
    List<Product> searchByEmbedding(@Param("embedding") String embedding,
                                    @Param("limit") int limit);
}
