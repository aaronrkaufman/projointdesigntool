import React, {
  FC,
  KeyboardEvent,
  ChangeEvent,
  useState,
  useRef,
  useEffect,
  Dispatch,
  SetStateAction,
  useContext,
} from "react";
import styles from "../survey/survey.module.css";
import { IAttribute } from "./attribute.container";
import { HighlightedContext } from "../../context/highlighted";
import { Draggable, Droppable } from "react-beautiful-dnd";
import DragButton from "../drag_button";
import { Level } from "../level/level";
import { useAttributes } from "../../context/attributes_context";
import { Weight } from "../level/weight";

interface PropsAttributeComponent {
  attribute: IAttribute;
  show: boolean;
  newLevel: string;
  onShow: () => void;
  onKeyPress: (event: KeyboardEvent) => void;
  onBlur: () => void;
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
  index: number;
}

export const Attribute: FC<PropsAttributeComponent> = ({
  attribute,
  show,
  newLevel,
  onShow,
  onKeyPress,
  onBlur,
  onChange,
  index,
}) => {
  // console.log(attribute, index);

  const {
    highlightedAttribute,
    setHighlightedAttribute,
    showWeights,
    currentWeights,
    setCurrentWeights,
  } = useContext(HighlightedContext);

  const { deleteAttribute, handleAttributeNameChange } = useAttributes();

  const [isEditing, setIsEditing] = useState(false);
  const [attributeName, setAttributeName] = useState<string>(attribute.name);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    !show && setHighlightedAttribute(-1);
  }, [show]);

  useEffect(() => {
    highlightedAttribute === attribute.key &&
      setCurrentWeights(attribute.levels.map((lvl) => lvl.weight));
  }, [highlightedAttribute]);

  useEffect(() => {
    if (isEditing) {
      inputRef.current?.focus();
    }
  }, [isEditing]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAttributeName(e.target.value);
  };

  const handleBlur = () => {
    setIsEditing(false);

    if (attributeName.trim() === "") {
      deleteAttribute(index);
    } else {
      handleAttributeNameChange(attributeName, index);
    }
  };

  const handleWeightChange = (index: number, newWeight: number) => {
    setCurrentWeights((prevWeights) => {
      const newWeights = [...prevWeights];
      newWeights[index] = newWeight;
      return newWeights;
    });
  };

  return (
    <Draggable
      key={attribute.key}
      draggableId={`draggable-${attribute.key}`}
      index={index}
    >
      {(provided) => (
        <li
          ref={provided.innerRef}
          {...provided.draggableProps}
          // {...provided.dragHandleProps}
          className={`${styles.attribute} ${
            highlightedAttribute === attribute.key ? styles.stroke : ""
          }`}
          onClick={() => {
            show && setHighlightedAttribute(attribute.key);
          }}
        >
          <div className={styles.deleteHandle}>
            <button
              onClick={() => {
                deleteAttribute(index);
              }}
              className={styles.deleteAttribute}
            >
              x
            </button>
          </div>
          <div className={styles.attribute_left}>
            <div className={`${styles.dragHandle} ${styles.dragAttribute}`}>
              <DragButton
                direction={"horizontal"}
                {...provided.dragHandleProps}
              />
            </div>
            <svg
              onClick={onShow}
              width="18"
              height="11"
              viewBox="0 0 18 11"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              style={{ transform: show ? "rotate(-180deg)" : "rotate(0deg)" }}
            >
              <path
                d="M1 1.5C1 1.5 7.31579 9.5 9 9.5C10.6842 9.5 17 1.5 17 1.5"
                stroke="#415A77"
                strokeWidth="2"
              />
            </svg>
            <div
              className={styles.atrributeInfo}
              onClick={() => {
                setIsEditing(true);
              }}
            >
              {isEditing ? (
                <input
                  ref={inputRef}
                  value={attributeName}
                  onChange={handleInputChange}
                  onBlur={handleBlur}
                  className={styles.input}
                  // additional styling or attributes
                />
              ) : (
                <p className={styles.levelName}>{attributeName}</p>
              )}
            </div>
          </div>
          <div className={styles.attribute_right}>
            {show ? (
              <Droppable
                droppableId={`droppable-levels-${attribute.key}`}
                type="levels"
              >
                {(provided) => (
                  <ul
                    className={`${styles.levels}`}
                    {...provided.droppableProps}
                    ref={provided.innerRef}
                  >
                    {attribute.levels.map((level, index) => (
                      <Level
                        key={level.id}
                        {...level}
                        index={index}
                        attributeName={attribute.name}
                      ></Level>
                    ))}
                    {provided.placeholder}
                    <li>
                      {/* <span className={styles.circle}></span> */}
                      <input
                        type="text"
                        className={styles.input}
                        placeholder={"Add level"}
                        value={newLevel}
                        onChange={onChange}
                        onKeyDown={onKeyPress}
                        onBlur={onBlur}
                      />
                    </li>
                  </ul>
                )}
              </Droppable>
            ) : (
              <p>{attribute.levels.length} levels</p>
            )}
          </div>
          <div
            className={`${styles.attribute_weights} ${
              showWeights && show ? "" : styles.notvisible
            }`}
          >
            {show && highlightedAttribute === attribute.key ? (
              <ul className={`${styles.weights}`}>
                {attribute.levels.map((lvl, index) => (
                  <Weight
                    key={index}
                    index={index}
                    value={lvl.weight}
                    onWeightChange={handleWeightChange}
                  />
                ))}
                <li>
                  {currentWeights
                    .reduce((acc, weight) => acc + weight, 0)
                    .toFixed(1)}
                </li>
              </ul>
            ) : (
              ""
            )}
          </div>
        </li>
      )}
    </Draggable>
  );
};
