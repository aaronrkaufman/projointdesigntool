import { Attribute } from "../attributes_context";

export const LevelNameChange = (
  attributeKey: number,
  newName: string,
  levelId: number, // Changed levelIndex to levelId
  setAttributes: React.Dispatch<React.SetStateAction<Attribute[]>>
) => {
  setAttributes((prevAttributes) =>
    prevAttributes.map((attribute) => {
      if (attribute.key === attributeKey) {
        const newLevels = attribute.levels.map((lvl) => {
          if (lvl.id === levelId) {
            // Use levelId for comparison
            return { ...lvl, name: newName };
          }
          return lvl;
        });

        // Return the updated attribute
        return { ...attribute, levels: newLevels };
      }

      // For other attributes, return them as is
      return attribute;
    })
  );
};

export const AddLevelToAttribute = (
  attributeKey: number,
  newLevel: string,
  setAttributes: React.Dispatch<React.SetStateAction<Attribute[]>>
) => {
  setAttributes((prevAttributes) =>
    prevAttributes.map((attribute) => {
      if (attribute.key === attributeKey) {
        const newLevelId =
          attribute.levels.reduce((maxId, lvl) => Math.max(maxId, lvl.id), 0) +
          1; // Calculate new levelId
        const newNumberOfLevels = attribute.levels.length + 1;
        const newWeight = parseFloat((1 / newNumberOfLevels).toFixed(2)) * 100;
        console.log(newWeight);
        const newLevels = attribute.levels.map((lvl) => {
          return { ...lvl, weight: newWeight };
        });
        return {
          ...attribute,
          levels: [
            ...newLevels,
            {
              name: newLevel,
              id: newLevelId, // Use newLevelId instead of length + 1
              weight: newWeight,
            },
          ],
        };
      }
      return attribute;
    })
  );
};

export const DeleteLevelFromAttribute = (
  attributeKey: number,
  levelId: number, // Changed levelIndex to levelId
  setAttributes: React.Dispatch<React.SetStateAction<Attribute[]>>
) => {
  setAttributes((prevAttributes) =>
    prevAttributes.map((attribute) => {
      if (attribute.key === attributeKey) {
        let newLevels = attribute.levels.filter(
          (lvl) => lvl.id !== levelId // Use levelId for comparison
        );

        const newNumberOfLevels = newLevels.length;
        const newWeight =
          newNumberOfLevels > 0
            ? parseFloat((1 / newNumberOfLevels).toFixed(2)) * 100
            : 0;

        newLevels = newLevels.map((lvl) => {
          return { ...lvl, weight: newWeight, id: lvl.id }; // Keep original id
        });

        return {
          ...attribute,
          levels: newLevels,
        };
      }
      return attribute;
    })
  );
};
