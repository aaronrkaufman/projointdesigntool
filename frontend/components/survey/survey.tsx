// SurveyComponent.tsx
import React, { FC, useContext, useEffect, useRef, useState } from "react";
import styles from "./survey.module.css";
import { AddAttribute } from "./add_attribute";
import { IAttribute } from "../attribute/attribute.container";
import { AttributeContainer } from "../attribute/attribute.container";
import { Button } from "../button";
import { HighlightedContext } from "../../context/highlighted";
import { useAttributes } from "../../context/attributes_context";
import { DocumentContext } from "../../context/document_context";

import { Droppable } from "react-beautiful-dnd";
import { downloadSurvey } from "../../services/api";

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
  const { highlightedAttribute, setShowWeights, showWeights } =
    useContext(HighlightedContext);
  const {
    setEdited,
    attributes,
    addLevelToAttribute,
    isCreatingAttribute,
    addNewAttribute,
    cancelNewAttribute,
    handleCreateAttribute,
  } = useAttributes();

  const { currentDoc, lastEdited, setLastEdited, setCurrentDoc } =
    useContext(DocumentContext);

  // Handle download of a file through export
  const [isLoading, setisLoading] = useState<boolean>(false);

  const handleDownload = async (path: "qualtrics" | "export" | "preview_csv") => {
    setisLoading(true);
    await downloadSurvey(attributes, path);
    setisLoading(false);
  };

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

  return (
    <section className={styles.survey}>
      {isLoading && (
        <div className={styles.loaderOverlay}>
          <div className={styles.loadingText}>Loading...</div>
        </div>
      )}
      <div className={styles.top}>
        {isEditing ? (
          <input
            ref={inputRef}
            value={docName}
            style={{ width: `${(docName.length + 1) * 14}px` }}
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
        {highlightedAttribute === -1 ? (
          ""
        ) : (
          <Button
            text={showWeights ? "Save weights" : "Edit weights"}
            onClick={() => setShowWeights(!showWeights)}
          ></Button>
        )}
        <Button
          text="Export to Qualtrics"
          onClick={() => handleDownload("qualtrics")}
        ></Button>
        <Button
          text="Export to JS"
          onClick={() => handleDownload("export")}
        ></Button>
        <Button
          text="Export to CSV"
          onClick={() => handleDownload("preview_csv")}
        ></Button>
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
                key={index}
                attribute={attribute}
                index={index}
                addLevel={addLevelToAttribute}
              />
            ))}
            {provided.placeholder}
            {isCreatingAttribute && (
              <AttributeContainer
                isCreator
                addNewAttribute={addNewAttribute}
                cancelNewAttribute={cancelNewAttribute}
              />
            )}
          </ul>
        )}
      </Droppable>
      <AddAttribute onCreate={handleCreateAttribute} />
    </section>
  );
};
