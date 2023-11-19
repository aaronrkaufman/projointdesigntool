// SurveyComponent.tsx
import React, { FC, useContext, useEffect } from "react";
import styles from "./survey.module.css";
import { AddAttribute } from "./add_attribute";
import { IAttribute } from "../attribute/attribute.container";
import { AttributeContainer } from "../attribute/attribute.container";
import { Button } from "../button";
import { HighlightedContext } from "../../context/highlighted";
import { useAttributes } from "../../context/attributes_context";
import { DocumentContext } from "../../context/document_context";

import { Droppable } from "react-beautiful-dnd";

export const Survey: FC = () => {
  const { highlightedAttribute, setShowWeights, showWeights } =
    useContext(HighlightedContext);
  const {
    attributes,
    addLevelToAttribute,
    isCreatingAttribute,
    addNewAttribute,
    cancelNewAttribute,
    handleCreateAttribute,
  } = useAttributes();

  const { currentDoc } = useContext(DocumentContext);
  console.log("waht is this:", currentDoc)
  return (
    <section className={styles.survey}>
      <div className={styles.top}>
        <h2>{currentDoc}</h2>
        {highlightedAttribute === -1 ? (
          ""
        ) : (
          <Button
            text={showWeights ? "Save weights" : "Edit weights"}
            onClick={() => setShowWeights(!showWeights)}
          ></Button>
        )}
      </div>
      <ul className={styles.attributes}>
        {attributes.map((attribute, index) => (
          <AttributeContainer
            key={index}
            attribute={attribute}
            addLevel={addLevelToAttribute}
          />
        ))}
        {isCreatingAttribute && (
          <AttributeContainer
            isCreator
            addNewAttribute={addNewAttribute}
            cancelNewAttribute={cancelNewAttribute}
          />
        )}
      </ul>
      <AddAttribute onCreate={handleCreateAttribute} />
    </section>
  );
};
