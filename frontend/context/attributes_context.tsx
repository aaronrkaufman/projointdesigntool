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
  weight: number;
}

interface StatementProps {
  part: "if" | "then" | "and" | "or";
  attribute: string;
  level: string;
  equals: boolean;
  id: string;
}

interface RestrictionProps {
  ifStates: StatementProps[];
  elseStates: StatementProps[];
  id: string;
}

export interface IInstructions {
  description: string;
  instructions: string;
}

export interface Attribute {
  name: string;
  levels: Level[];
  key: number;
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
  updateWeight: (attributeKey: number, newWeights: number[]) => void;
  cancelNewAttribute: () => void;
  handleCreateAttribute: () => void;
  handleInstructions: (
    value: string,
    setting: "instructions" | "description"
  ) => void;
  handleLevelNameChange: (
    attributeName: string,
    newName: string,
    levelIndex: number
  ) => void;
  handleAttributeNameChange: (newName: string, index: number) => void;
  setEdited: (edited: boolean) => void;
  storageChanged: number;
  setStorageChanged: React.Dispatch<React.SetStateAction<number>>;
  // restrictions: string[];
  restrictions: RestrictionProps[];
  saveRestriction: (restriction: RestrictionProps) => void;
  // addRestrictionToAttribute: (newRestriction: RestrictionProps) => void;
  deleteRestriction: (restrictionId: string) => void;
  // editRestrictionInAttribute: (
  //   restrictionIndex: number,
  //   newRestriction: RestrictionProps
  // ) => void;
  instructions: IInstructions;
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

  const [restrictions, setRestrictions] = useState<RestrictionProps[]>([]);

  const [instructions, setInstructions] = useState<IInstructions>({
    description: "",
    instructions: "",
  });

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
        setRestrictions(parsedData.restrictions ? parsedData.restrictions : []);
        setInstructions(parsedData.instructions);
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
        restrictions: restrictions,
        instructions: instructions,
      };
      localStorage.setItem(
        `attributes-${currentDocID}`,
        JSON.stringify(dataToSave)
      );
      setStorageChanged((prev) => prev + 1);
      setEdited(false);

      console.log("maybe now?");
      console.log(attributes[0].levels);
    }
  }, [
    attributes,
    currentDocID,
    lastEdited,
    edited,
    currentDoc,
    restrictions,
    instructions,
  ]);

  // TODO: Change keys so there is no possiblity of duplicate keys
  const addNewAttribute = (name: string) => {
    const newAttribute: Attribute = {
      name,
      levels: [],
      key: attributes.length + 1,
    };
    setAttributes([...attributes, newAttribute]);
    setIsCreatingAttribute(false);
    setEdited(true);
  };

  const handleInstructions = (
    value: string,
    setting: "instructions" | "description"
  ) => {
    setting == "instructions"
      ? setInstructions({
          instructions: value,
          description: instructions?.description || "",
        })
      : setInstructions({
          instructions: instructions?.instructions || "",
          description: value,
        });
    setEdited(true);
  };

  // TODO: Change keys so there is no possiblity of duplicate keys
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
          const newLevels = attribute.levels.map((lvl) => {
            return { ...lvl, weight: newWeight };
          });
          return {
            ...attribute,

            levels: [
              ...newLevels,
              {
                name: newLevel,
                id: newLevels.length + 1,
                weight: newWeight,
              },
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
          let newLevels = attribute.levels.filter(
            (_, index) => index !== levelIndex
          );

          const newNumberOfLevels = newLevels.length;
          const newWeight =
            newNumberOfLevels > 0
              ? parseFloat((1 / newNumberOfLevels).toFixed(2))
              : 0;

          newLevels = newLevels.map((lvl, index) => {
            return { ...lvl, weight: newWeight, id: index + 1 };
          });

          return {
            ...attribute,
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

  const saveRestriction = (restriction: RestrictionProps) => {
    // Assuming we have a function to save the entire array of restrictions to local storage
    setRestrictions((prevRestrictions) => {
      const index = prevRestrictions.findIndex((r) => r.id === restriction.id);
      if (index !== -1) {
        // Update existing restriction
        return prevRestrictions.map((r) =>
          r.id === restriction.id ? restriction : r
        );
      } else {
        // Add new restriction
        return [...prevRestrictions, restriction];
      }
    });
    setEdited(true);
  };

  // // Function to delete a restriction from an attribute
  const deleteRestriction = (restrictionID: string) => {
    setRestrictions((prev) => {
      const index = prev.findIndex((r) => r.id === restrictionID);
      if (index !== -1) {
        // Update existing restriction
        return prev.filter((r) => r.id !== restrictionID);
      } else {
        return [...prev];
      }
    });

    setEdited(true);
  };

  const updateWeight = (attributeKey: number, newWeights: number[]) => {
    setAttributes((prevAttributes) =>
      prevAttributes.map((attribute) => {
        if (attribute.key === attributeKey) {
          // Map over levels and update their weights
          const updatedLevels = attribute.levels.map((lvl, index) => ({
            ...lvl,
            weight: newWeights[index],
          }));

          return {
            ...attribute,
            levels: updatedLevels,
          };
        }
        return attribute; // Return the attribute unchanged if it's not the one being updated
      })
    );
    setEdited(true);
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
    handleInstructions,
    storageChanged,
    setStorageChanged,
    deleteAttribute,
    restrictions,
    saveRestriction,
    deleteRestriction,
    // addRestrictionToAttribute,

    // editRestrictionInAttribute,
    instructions,
    // Add other functions here
  };

  return (
    <AttributeContext.Provider value={value}>
      {children}
    </AttributeContext.Provider>
  );
};

export default AttributeProvider;
