package rgb.contest.semantic_search.search_api.repository;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;

import java.util.Arrays;
import java.util.stream.Collectors;

@Converter(autoApply = false) // use only where explicitly annotated
public class PgVectorConverter implements AttributeConverter<float[], String> {

    @Override
    public String convertToDatabaseColumn(float[] attribute) {
        if (attribute == null) {
            return null;
        }

        String[] strArr = new String[attribute.length];
        for (int i = 0; i < attribute.length; i++) {
            strArr[i] = Float.toString(attribute[i]);
        }

        return "[" + String.join(",", strArr) + "]";
    }

    @Override
    public float[] convertToEntityAttribute(String dbData) {
        if (dbData == null || dbData.isBlank()) return new float[0];

        // Strip leading/trailing [ ]
        String cleaned = dbData.trim()
                .replaceFirst("^\\[", "")
                .replaceFirst("]$", "");

        if (cleaned.isBlank()) return new float[0];

        String[] parts = cleaned.split(",");
        float[] result = new float[parts.length];
        for (int i = 0; i < parts.length; i++) {
            result[i] = Float.parseFloat(parts[i].trim());
        }
        return result;
    }
}