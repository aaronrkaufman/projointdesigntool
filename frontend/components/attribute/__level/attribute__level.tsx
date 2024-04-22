import styles from "./attribute__level.module.css";

import { ILevel } from "../attribute.container";
import { Draggable } from "react-beautiful-dnd";
import DragButton from "../../ui/drag_button";
import { useState, useRef, useEffect } from "react";
import { useAttributes } from "../../../context/attributes_context";
import { RemoveMinus } from "../../ui/icons";

interface ILevelComponent extends ILevel {
  index: number;
  attributeKey: number;
}

export const Level = ({ name, index, id, attributeKey }: ILevelComponent) => {
  const [isEditing, setIsEditing] = useState(false);
  const [levelName, setLevelName] = useState<string>(name);
  const inputRef = useRef<HTMLInputElement>(null);

  const { deleteLevelFromAttribute, handleLevelNameChange } = useAttributes();

  useEffect(() => {
    if (isEditing) {
      inputRef.current?.focus();
    }
  }, [isEditing]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLevelName(e.target.value);
  };

  const handleBlur = () => {
    setIsEditing(false);

    if (levelName.trim() === "") {
      deleteLevelFromAttribute(attributeKey, id);
    } else {
      handleLevelNameChange(attributeKey, levelName, id);
    }
  };

  return (
    <Draggable
      key={id}
      draggableId={`draggable-level-${attributeKey}-${id}`}
      index={index}
    >
      {(providedHere) => (
        <li
          ref={providedHere.innerRef}
          {...providedHere.draggableProps}
          className={styles.level}
        >
          <div className={`${styles.dragHandle} ${styles.dragLevel}`}>
            <DragButton
              direction={"horizontal"}
              {...providedHere.dragHandleProps}
            />
          </div>
          <div
            className={styles.levelInfo}
            onClick={() => {
              setIsEditing(true);
            }}
          >
            {isEditing ? (
              <input
                ref={inputRef}
                value={levelName}
                onChange={handleInputChange}
                onBlur={handleBlur}
                className={styles.input}
                // additional styling or attributes
              />
            ) : (
              <p className={styles.levelName}>{levelName}</p>
            )}
            <div
              onClick={() => {
                deleteLevelFromAttribute(attributeKey, id);
              }}
              className={styles.deleteLevel}
            >
              <RemoveMinus />
              <RemoveMinus />
            </div>
          </div>
        </li>
      )}
    </Draggable>
  );
};
