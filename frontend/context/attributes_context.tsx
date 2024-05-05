import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { DocumentContext } from "./document_context";
import {
  AddLevelToAttribute,
  DeleteLevelFromAttribute,
  LevelNameChange,
} from "./utils/level";

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
  addLevelToAttribute: (attributeKey: number, newLevel: string) => void;
  deleteLevelFromAttribute: (attributeKey: number, levelId: number) => void; // Changed levelIndex to levelId
  deleteAttribute: (key: number) => void;
  updateWeight: (attributeKey: number, newWeights: number[]) => void;
  cancelNewAttribute: () => void;
  handleCreateAttribute: () => void;
  handleInstructions: (
    value: string,
    setting: "instructions" | "description"
  ) => void;
  handleLevelNameChange: (
    attributeKey: number,
    newName: string,
    levelId: number // Changed levelIndex to levelId
  ) => void;
  handleAttributeNameChange: (newName: string, key: number) => void;
  setEdited: (edited: boolean) => void;
  storageChanged: number;
  setStorageChanged: React.Dispatch<React.SetStateAction<number>>;
  restrictions: RestrictionProps[];
  saveRestriction: (restriction: RestrictionProps) => void;
  deleteRestriction: (restrictionId: string) => void;
  instructions: IInstructions;
}

const AttributeContext = createContext<AttributeContextType | undefined>(
  undefined
);

export const useAttributes = () => {
  const context = useContext(AttributeContext);
  if (!context) {
    throw new Error("useAttributes must be used within an AttributeProvider");
  }
  return context;
};

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
      } else {
        setAttributes([]);
      }
    }
  }, [currentDocID]);

  const [isCreatingAttribute, setIsCreatingAttribute] = useState(false);

  useEffect(() => {
    if (currentDocID && currentDocID === prevDocID && edited) {
      setLastEdited(new Date());
      const dataToSave = {
        attributes: attributes,
        lastEdited: new Date(),
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
      key: Date.now(), // Using Date.now() to ensure a unique key
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

  const deleteAttribute = (key: number) => {
    setAttributes((prevAttributes) => {
      const newAttributes = prevAttributes.filter(
        (attribute) => attribute.key !== key
      );
      return newAttributes;
    });
    setEdited(true);
  };

  const handleCreateAttribute = () => setIsCreatingAttribute(true);

  const addLevelToAttribute = (attributeKey: number, newLevel: string) => {
    AddLevelToAttribute(attributeKey, newLevel, setAttributes);
    setEdited(true);
  };

  const deleteLevelFromAttribute = (
    attributeKey: number,
    levelId: number // Changed levelIndex to levelId
  ) => {
    DeleteLevelFromAttribute(attributeKey, levelId, setAttributes);
    setEdited(true);
  };

  const cancelNewAttribute = () => setIsCreatingAttribute(false);

  const handleLevelNameChange = (
    attributeKey: number,
    newName: string,
    levelId: number // Changed levelIndex to levelId
  ) => {
    LevelNameChange(attributeKey, newName, levelId, setAttributes);
    setEdited(true);
  };

  const handleAttributeNameChange = (newName: string, key: number) => {
    setAttributes((prevAttributes) => {
      return prevAttributes.map((attribute) => {
        if (attribute.key === key) {
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
    handleLevelNameChange,
    updateWeight,
    cancelNewAttribute,
    handleCreateAttribute,
    setEdited,
    handleAttributeNameChange,
    handleInstructions,
    storageChanged,
    setStorageChanged,
    deleteAttribute,
    restrictions,
    saveRestriction,
    deleteRestriction,
    instructions,
  };

  return (
    <AttributeContext.Provider value={value}>
      {children}
    </AttributeContext.Provider>
  );
};

export default AttributeProvider;
