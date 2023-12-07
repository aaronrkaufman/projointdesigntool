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
  id: number;
}

export interface Attribute {
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
  deleteLevelFromAttribute: (attributeName: string, levelIndex: number) => void;
  deleteAttribute: (index: number) => void;
  updateWeight: (
    attributeKey: number,
    index: number,
    newWeight: string
  ) => void;
  cancelNewAttribute: () => void;
  handleCreateAttribute: () => void;
  handleLevelNameChange: (
    attributeName: string,
    newName: string,
    levelIndex: number
  ) => void;
  handleAttributeNameChange: (newName: string, index: number) => void;
  setEdited: (edited: boolean) => void;
  storageChanged: number;
  setStorageChanged: (storageChanged: number) => void;
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

  const { currentDoc, lastEdited, setLastEdited, currentDocID, setCurrentDoc } =
    useContext(DocumentContext);
  const [prevDocID, setPrevDocID] = useState<string>("");
  const [edited, setEdited] = useState<boolean>(false);
  const [storageChanged, setStorageChanged] = useState<number>(0);

  useEffect(() => {
    if (currentDocID && currentDocID !== prevDocID) {
      setEdited(false);
      setPrevDocID(currentDocID);
      const localData = localStorage.getItem(`attributes-${currentDocID}`);
      if (localData) {
        const parsedData = JSON.parse(localData);
        setAttributes(parsedData.attributes);
        setLastEdited(new Date(parsedData.lastEdited));
        setCurrentDoc(parsedData.name);
        // Use parsedData.lastEdited as needed
      } else {
        setAttributes([]);
      }
    }
  }, [currentDocID]);

  const [isCreatingAttribute, setIsCreatingAttribute] = useState(false);

  useEffect(() => {
    // console.log("but here it is:", currentDoc);
    if (
      currentDocID &&
      // attributes.length > 0 &&
      currentDocID === prevDocID &&
      edited
    ) {
      setLastEdited(new Date());
      const dataToSave = {
        attributes: attributes,
        lastEdited: new Date(), // Update last edited time
        name: currentDoc,
      };
      localStorage.setItem(
        `attributes-${currentDocID}`,
        JSON.stringify(dataToSave)
      );
      setStorageChanged((prev) => prev + 1);
      setEdited(false);

      console.log("maybe now?");
    }
  }, [attributes, currentDocID, lastEdited, edited, currentDoc]);

  const addNewAttribute = (name: string) => {
    const newAttribute: Attribute = {
      name,
      levels: [],
      key: attributes.length,
      weights: [],
    };
    setAttributes([...attributes, newAttribute]);
    setIsCreatingAttribute(false);
    setEdited(true);
  };

  const deleteAttribute = (index: number) => {
    setAttributes((prevAttributes) => {
      const newAttributes = prevAttributes.filter((_, ind) => ind !== index);
      return newAttributes;
    });
    setEdited(true);
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
            levels: [
              ...attribute.levels,
              { name: newLevel, id: attribute.levels.length + 1 },
            ],
          };
        }
        return attribute;
      })
    );
    setEdited(true);
  };

  const deleteLevelFromAttribute = (
    attributeName: string,
    levelIndex: number
  ) => {
    setAttributes((prevAttributes) =>
      prevAttributes.map((attribute) => {
        if (attribute.name === attributeName) {
          // Remove the level at the specified index
          const newLevels = attribute.levels.filter(
            (_, index) => index !== levelIndex
          );
          const newNumberOfLevels = newLevels.length;
          const newWeight =
            newNumberOfLevels > 0
              ? parseFloat((1 / newNumberOfLevels).toFixed(2))
              : 0;
          const newWeights = Array(newNumberOfLevels).fill(newWeight);

          return {
            ...attribute,
            weights: newWeights,
            levels: newLevels,
          };
        }
        return attribute;
      })
    );
    setEdited(true);
  };

  const cancelNewAttribute = () => setIsCreatingAttribute(false);

  const handleLevelNameChange = (
    attributeName: string,
    newName: string,
    levelIndex: number
  ) => {
    // console.log("yes here.", attributeName, newName, levelIndex)
    setAttributes((prevAttributes) =>
      prevAttributes.map((attribute) => {
        // Check if this is the attribute to update
        if (attribute.name === attributeName) {
          // Copy the levels array
          const newLevels = [...attribute.levels];

          // Check if the level index is valid
          if (levelIndex >= 0 && levelIndex < newLevels.length) {
            // Update the level name
            newLevels[levelIndex] = { ...newLevels[levelIndex], name: newName };
          }

          // Return the updated attribute
          return { ...attribute, levels: newLevels };
        }

        // For other attributes, return them as is
        return attribute;
      })
    );
    setEdited(true);
  };

  const handleAttributeNameChange = (newName: string, index: number) => {
    setAttributes((prevAttributes) => {
      return prevAttributes.map((attribute, ind) => {
        if (ind === index) {
          return { ...attribute, name: newName };
        }
        return attribute;
      });
    });
    setEdited(true);
  };

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
    deleteLevelFromAttribute,
    updateWeight,
    cancelNewAttribute,
    handleCreateAttribute,
    handleLevelNameChange,
    setEdited,
    handleAttributeNameChange,
    storageChanged,
    setStorageChanged,
    deleteAttribute,
    // Add other functions here
  };

  return (
    <AttributeContext.Provider value={value}>
      {children}
    </AttributeContext.Provider>
  );
};

export default AttributeProvider;
