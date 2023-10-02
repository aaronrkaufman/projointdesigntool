// SurveyComponent.tsx
import React, { FC } from "react";
import styles from "./survey.module.css";
import { AddAttribute } from "./add_attribute";
import { IAttribute } from "../attribute/attribute.container";
import { AttributeContainer } from "../attribute/attribute.container";

interface Props {
  attributes: IAttribute[];
  isCreatingAttribute: boolean;
  onAddAttribute: (name: string) => void;
  onCancelNewAttribute: () => void;
  onAddLevelToAttribute: (attributeName: string, newLevel: string) => void;
  onCreateAttribute: () => void;
}

export const Survey: FC<Props> = ({
  attributes,
  isCreatingAttribute,
  onAddAttribute,
  onCancelNewAttribute,
  onAddLevelToAttribute,
  onCreateAttribute,
}) => (
  <section className={styles.survey}>
    <h2>Immigrant Survey</h2>
    <ul className={styles.attributes}>
      {attributes.map((attribute, index) => (
        <AttributeContainer
          key={index}
          attribute={attribute}
          addLevel={onAddLevelToAttribute}
        />
      ))}
      {isCreatingAttribute && (
        <AttributeContainer
          isCreator
          addNewAttribute={onAddAttribute}
          cancelNewAttribute={onCancelNewAttribute}
        />
      )}
    </ul>
    <AddAttribute onCreate={onCreateAttribute} />
  </section>
);
