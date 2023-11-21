import styles from "../survey/survey.module.css";

import { ILevel } from "../attribute/attribute.container";
import { Draggable } from "react-beautiful-dnd";

interface ILevelComponent extends ILevel {
  index: number;
}

export const Level = ({ name, index, id }: ILevelComponent) => {
  return (
    <Draggable key={id} draggableId={`draggable-level-${name}`} index={index}>
      {(providedHere) => (
        <li
          ref={providedHere.innerRef}
          {...providedHere.draggableProps}
          {...providedHere.dragHandleProps}
        >
          <span className={styles.circle}></span>
          {name}
        </li>
      )}
    </Draggable>
  );
};
