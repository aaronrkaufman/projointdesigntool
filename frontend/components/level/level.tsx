import styles from "../survey/survey.module.css";

import { ILevel } from "../attribute/attribute.container";
import { Draggable } from "react-beautiful-dnd";
import DragButton from "../drag_button";
import { useState, useRef, useEffect } from "react";

interface ILevelComponent extends ILevel {
  index: number;
}

export const Level = ({ name, index, id }: ILevelComponent) => {
  const [isEditing, setIsEditing] = useState(false);
  const [levelName, setLevelName] = useState<string>(name);
  const inputRef = useRef<HTMLInputElement>(null);

  //   useEffect(() => {
  //     if (levelName !== currentDoc) {
  //         setLevelName(currentDoc);
  //     }
  //   }, [currentDoc]);

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
    // Here you can call a function to save the docName
    // saveDocName(docName);
  };

  return (
    <Draggable key={id} draggableId={`draggable-level-${name}`} index={index}>
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
            <p>X</p>
          </div>
        </li>
      )}
    </Draggable>
  );
};
