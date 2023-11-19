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
    setAttributes,
  } = useAttributes();

  const { currentDoc } = useContext(DocumentContext);

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
      <Droppable droppableId="droppable-attributes">
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
