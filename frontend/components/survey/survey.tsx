// SurveyComponent.tsx
import React, { FC, useContext, useEffect, useRef, useState } from "react";
import styles from "./survey.module.css";
import { AddAttribute } from "./add_attribute";
import { AttributeContainer } from "../attribute/attribute.container";
import { Button } from "../ui/button";
import { HighlightedContext } from "../../context/highlighted";
import { useAttributes } from "../../context/attributes_context";
import { DocumentContext } from "../../context/document_context";

import { Droppable } from "react-beautiful-dnd";
import ExportDropdown from "./export";

const getTimeElapsed = (lastEdited: Date) => {
  const now = new Date();
  const elapsed = now.getTime() - lastEdited.getTime(); // time in milliseconds

  if (elapsed < 60000) return "last edited now";
  if (elapsed < 3600000) return `${Math.round(elapsed / 60000)} minutes ago`;
  if (elapsed < 86400000) return `${Math.round(elapsed / 3600000)} hours ago`;
  // Add more conditions for days, months, years as needed
  if (elapsed < 2629800000) return `${Math.round(elapsed / 86400000)} days ago`; // 30.44 days in milliseconds
  if (elapsed < 31557600000)
    return `${Math.round(elapsed / 2629800000)} months ago`; // Average month in milliseconds (30.44 days)
  return `${Math.round(elapsed / 31557600000)} years ago`; // Average year in milliseconds (365.25 days)
};

export const Survey: FC = () => {
  const { highlightedAttribute, setShowWeights, showWeights, currentWeights } =
    useContext(HighlightedContext);

  const {
    setEdited,
    attributes,
    addLevelToAttribute,
    isCreatingAttribute,
    addNewAttribute,
    cancelNewAttribute,
    handleCreateAttribute,
    updateWeight,
  } = useAttributes();

  const { currentDoc, lastEdited, setLastEdited, setCurrentDoc } =
    useContext(DocumentContext);

  // Handle name change
  const [isEditing, setIsEditing] = useState(false);
  const [docName, setDocName] = useState<string>(currentDoc);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (docName !== currentDoc) {
      setDocName(currentDoc);
    }
  }, [currentDoc]);

  useEffect(() => {
    if (isEditing) {
      inputRef.current?.focus();
    }
  }, [isEditing]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDocName(e.target.value);
  };

  const handleBlur = () => {
    setIsEditing(false);
    setLastEdited(new Date());
    setEdited(true);
    // Here you can call a function to save the docName
    // saveDocName(docName);
    setCurrentDoc(docName);
  };

  const saveWeights = () => {
    const totalWeight = currentWeights.reduce((acc, weight) => acc + weight, 0);

    if (totalWeight >= 0.9 && totalWeight <= 1.1) {
      // Save logic here
      console.log("Weights are valid and saved.");
      updateWeight(highlightedAttribute, currentWeights);
    } else {
      // TODO make something else
      alert("Total weight must be close to 1.");
    }
  };

  return (
    <section className={styles.survey}>
      <div className={styles.surveyContainer}>
        <div className={styles.top}>
          {isEditing ? (
            <input
              ref={inputRef}
              value={docName}
              style={{ width: `${(docName.length + 1) * 9.75}px` }}
              onChange={handleInputChange}
              onBlur={handleBlur}
              className={styles.editableInput}
              // additional styling or attributes
            />
          ) : (
            <h2
              onClick={() => {
                setIsEditing(true);
              }}
            >
              {docName}
            </h2>
          )}
          {/* {highlightedAttribute === -1 ? (
            ""
          ) : (
            <Button
              text={showWeights ? "Save weights" : "Edit weights"}
              onClick={
                showWeights
                  ? () => saveWeights()
                  : () => setShowWeights(!showWeights)
              }
            ></Button>
          )} */}
          {/* <ExportDropdown /> */}
          {/* <CustomDropdown /> */}
          <div>Last edited: {getTimeElapsed(lastEdited)}</div>
        </div>
        <Droppable droppableId="droppable-attributes" type="group">
          {(provided) => (
            <ul
              className={styles.attributes}
              {...provided.droppableProps}
              ref={provided.innerRef}
            >
              {attributes.map((attribute, index) => (
                <AttributeContainer
                  key={attribute.key}
                  attribute={attribute}
                  index={index}
                  addLevel={addLevelToAttribute}
                />
              ))}
              {provided.placeholder}
              {/* {isCreatingAttribute && (
                <AttributeContainer
                  isCreator
                  addNewAttribute={addNewAttribute}
                  cancelNewAttribute={cancelNewAttribute}
                />
              )} */}
            </ul>
          )}
        </Droppable>
        <AddAttribute onCreate={handleCreateAttribute} />
      </div>
    </section>
  );
};
