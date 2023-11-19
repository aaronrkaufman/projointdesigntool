import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { DocumentContext } from "./document_context";

interface Level {
  name: string;
}

interface Attribute {
  name: string;
  levels: Level[];
  key: number;
  weights: number[];
}

interface AttributeContextType {
  attributes: Attribute[];
  setAttributes: React.Dispatch<React.SetStateAction<Attribute[]>>;
  isCreatingAttribute: boolean;
  setIsCreatingAttribute: React.Dispatch<React.SetStateAction<boolean>>;
  addNewAttribute: (name: string) => void;
  addLevelToAttribute: (attributeName: string, newLevel: string) => void;
  updateWeight: (
    attributeKey: number,
    index: number,
    newWeight: string
  ) => void;
  cancelNewAttribute: () => void;
  handleCreateAttribute: () => void;
  // Include other function signatures as needed
}

// Initialize context with undefined as it will be set in the provider
const AttributeContext = createContext<AttributeContextType | undefined>(
  undefined
);

// Custom hook to use the attribute context
export const useAttributes = () => {
  const context = useContext(AttributeContext);
  if (!context) {
    throw new Error("useAttributes must be used within an AttributeProvider");
  }
  return context;
};

// The component that provides the context
export const AttributeProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [attributes, setAttributes] = useState<Attribute[]>([]);

  const { currentDoc } = useContext(DocumentContext);
  const [prevDoc, setPrevDoc] = useState<string>("");

  useEffect(() => {
    if (currentDoc && currentDoc != prevDoc) {
      setPrevDoc(currentDoc);
      // console.log("here it is:", currentDoc, "ande here:", prevDoc);
      const localData = localStorage.getItem(`attributes-${currentDoc}`);
      if (localData) {
        setAttributes(JSON.parse(localData));
      }
    }
  }, [currentDoc]);

  const [isCreatingAttribute, setIsCreatingAttribute] = useState(false);

  useEffect(() => {
    // console.log("but here it is:", currentDoc);
    if (currentDoc && attributes.length > 0 && currentDoc == prevDoc) {
      localStorage.setItem(
        `attributes-${currentDoc}`,
        JSON.stringify(attributes)
      );
    }
  }, [attributes, currentDoc]);

  const addNewAttribute = (name: string) => {
    const newAttribute: Attribute = {
      name,
      levels: [],
      key: attributes.length,
      weights: [],
    };
    setAttributes([...attributes, newAttribute]);
    setIsCreatingAttribute(false);
  };

  const handleCreateAttribute = () => setIsCreatingAttribute(true);

  const addLevelToAttribute = (attributeName: string, newLevel: string) => {
    setAttributes((prevAttributes) =>
      prevAttributes.map((attribute) => {
        if (attribute.name === attributeName) {
          const newNumberOfLevels = attribute.levels.length + 1;
          const newWeight = parseFloat((1 / newNumberOfLevels).toFixed(2));
          const newWeights = Array(newNumberOfLevels).fill(newWeight);
          return {
            ...attribute,
            weights: newWeights,
            levels: [...attribute.levels, { name: newLevel }],
          };
        }
        return attribute;
      })
    );
  };

  const cancelNewAttribute = () => setIsCreatingAttribute(false);

  const updateWeight = (
    attributeKey: number,
    index: number,
    newWeight: string
  ) => {
    setAttributes((prevAttributes) =>
      prevAttributes.map((attribute) => {
        if (attribute.key === attributeKey) {
          const updatedWeights = [...attribute.weights];
          const weightFloat = parseFloat(newWeight);
          updatedWeights[index] = isNaN(weightFloat) ? 0 : weightFloat;

          // This logic assumes you want to distribute the remaining weight equally
          // It will need to be adjusted if you want a different distribution logic
          const remainingWeight = 1 - weightFloat;
          const sumOtherWeights = updatedWeights.reduce(
            (sum, _, idx) => (idx !== index ? sum + updatedWeights[idx] : sum),
            0
          );
          if (sumOtherWeights > 0) {
            updatedWeights.forEach((_, idx) => {
              if (idx !== index) {
                updatedWeights[idx] = parseFloat(
                  (
                    (remainingWeight * updatedWeights[idx]) /
                    sumOtherWeights
                  ).toFixed(2)
                );
              }
            });
          }

          return {
            ...attribute,
            weights: updatedWeights,
          };
        }
        return attribute;
      })
    );
  };

  const value: AttributeContextType = {
    attributes,
    setAttributes,
    isCreatingAttribute,
    setIsCreatingAttribute,
    addNewAttribute,
    addLevelToAttribute,
    updateWeight,
    cancelNewAttribute,
    handleCreateAttribute,
    // Add other functions here
  };

  return (
    <AttributeContext.Provider value={value}>
      {children}
    </AttributeContext.Provider>
  );
};

export default AttributeProvider;
