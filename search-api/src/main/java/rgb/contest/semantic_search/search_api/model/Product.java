package rgb.contest.semantic_search.search_api.model;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "products")
@Data
public class Product {
    /*
    asin  CHAR(10) PRIMARY KEY,
    title TEXT,
    department VARCHAR(255),
    description TEXT,
    embedding VECTOR(384)
    */

    @Id
    private String asin;
    private String title;
    private String department;
    private String description;

    // Store as JSON string or float[] depending on mapping strategy
    @Column(columnDefinition = "vector(384)")
    private float[] embedding;
}
