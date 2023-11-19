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
import { Draggable } from "react-beautiful-dnd";
import DragButton from "../drag_button";

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
  const attributeRef = useRef<HTMLLIElement | null>(null);

  useEffect(() => {
    !show && setHighlightedAttribute(-1);
  }, [show]);

  const { highlightedAttribute, setHighlightedAttribute, showWeights } =
    useContext(HighlightedContext);

  return (
    <Draggable
      key={attribute.key}
      draggableId={`draggable-${attribute.name}`}
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
          <div className={styles.attribute_left}>
            <div className={styles.dragHandle}>
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
            <p>{attribute.name}</p>
          </div>
          <div className={styles.attribute_right}>
            {show ? (
              <ul className={`${styles.levels}`}>
                {attribute.levels.map((level, index) => (
                  <li key={index}>
                    <span className={styles.circle}></span>
                    {level.name}
                  </li>
                ))}
                <li>
                  <span className={styles.circle}></span>
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
                {attribute.weights.map((weight, index) => (
                  <input
                    className={styles.input}
                    key={index}
                    value={weight}
                  ></input>
                ))}
                <li>{1.0}</li>
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
