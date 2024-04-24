import { RestrictionProps } from "@/components/restrictions/restriction";
import { Attribute } from "../context/attributes_context";
import { StatementProps } from "@/components/restrictions/restrictions";

export const preproccessAttributes = (attributes: Attribute[]) => {
  const processedAttributes = attributes.map((attribute) => {
    // Combine the levels and weights into one array of objects
    const levels = attribute.levels.map((level, index) => ({
      name: level.name,
      weight: level.weight || 0, // Use the weight or default to 0 if not available
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

export const preprocessRestrictions = (restrictions: RestrictionProps[]) => {
  const processedRestrictions = restrictions.map((restriction) => {
    const formatStatement = (
      statement: StatementProps,
      index: number,
      array: StatementProps[]
    ) => {
      const operand = statement.equals ? "==" : "!=";
      const joiner =
        index != 0 ? `;${statement.part == "and" ? "&&" : "||"};` : "";
      return `${joiner}${statement.attribute};${operand};${statement.level}`;
    };

    const ifPart = restriction.ifStates.map(formatStatement).join("");
    const thenPart = restriction.elseStates.map(formatStatement).join("");
    const logicalOperator = restriction.elseStates.length > 0 ? ";then;" : "";

    return ifPart + logicalOperator + thenPart;
  });

  return {
    restrictions: processedRestrictions,
  };
};
