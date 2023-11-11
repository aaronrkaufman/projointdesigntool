// SurveyComponent.tsx
import React, { FC, useContext, useEffect } from "react";
import styles from "./survey.module.css";
import { AddAttribute } from "./add_attribute";
import { IAttribute } from "../attribute/attribute.container";
import { AttributeContainer } from "../attribute/attribute.container";
import { Button } from "../button";
import { HighlightedContext } from "@/context/highlighted";
import { useAttributes } from "@/context/attributes_context";

// interface Props {
//   attributes: IAttribute[];
//   isCreatingAttribute: boolean;
//   onAddAttribute: (name: string) => void;
//   onCancelNewAttribute: () => void;
//   onAddLevelToAttribute: (attributeName: string, newLevel: string) => void;
//   onCreateAttribute: () => void;
//   onUpdateWeight: (
//     attributeKey: number,
//     index: number,
//     newWeight: string
//   ) => void;
// }

export const Survey: FC = (
  {
    // attributes,
    // isCreatingAttribute,
    // onAddAttribute,
    // onCancelNewAttribute,
    // onAddLevelToAttribute,
    // onCreateAttribute,
    // onUpdateWeight
  }
) => {
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
  return (
    <section className={styles.survey}>
      <div className={styles.top}>
        <h2>Immigrant Survey</h2>
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
