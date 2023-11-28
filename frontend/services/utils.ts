import { Attribute } from "../context/attributes_context";

export const preproccessAttributes = (attributes: Attribute[]) => {
  const processedAttributes = attributes.map((attribute) => {
    // Combine the levels and weights into one array of objects
    const levels = attribute.levels.map((level, index) => ({
      name: level.name,
      weight: attribute.weights[index] || 0, // Use the weight or default to 0 if not available
    }));

    return {
      name: attribute.name,
      levels: levels,
    };
  });

  // Return the object in the desired format
  return {
    attributes: processedAttributes,
  };
};
