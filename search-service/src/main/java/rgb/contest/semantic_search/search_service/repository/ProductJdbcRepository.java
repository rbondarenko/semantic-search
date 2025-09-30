package rgb.contest.semantic_search.search_service.repository;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;
import rgb.contest.semantic_search.search_service.model.Product;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

@Repository
public class ProductJdbcRepository {

    private final JdbcTemplate jdbcTemplate;

    public ProductJdbcRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public List<Product> searchByEmbedding(String embedding, int limit) {
        String sql = """
            SELECT asin, title, department, description, embedding::text
            FROM products
            ORDER BY embedding <-> CAST(? AS vector)
            LIMIT ?
            """;

        return jdbcTemplate.query(sql, new Object[]{embedding, limit}, new ProductRowMapper());
    }

    private static class ProductRowMapper implements RowMapper<Product> {
        @Override
        public Product mapRow(ResultSet rs, int rowNum) throws SQLException {
            Product p = new Product();
            p.setAsin(rs.getString("asin"));
            p.setTitle(rs.getString("title"));
            p.setDepartment(rs.getString("department"));
            p.setDescription(rs.getString("description"));
            String vectorText = rs.getString("embedding");
            if (vectorText != null) {
                p.setEmbedding(new PgVectorConverter().convertToEntityAttribute(vectorText));
            }
            return p;
        }
    }
}
