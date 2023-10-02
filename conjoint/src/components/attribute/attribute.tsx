// AttributeComponent.tsx
import React, { FC, KeyboardEvent, ChangeEvent } from "react";
import styles from "../survey/survey.module.css";
import { IAttribute } from "./attribute.container";

interface PropsAttributeComponent {
  attribute: IAttribute;
  show: boolean;
  newLevel: string;
  onShow: () => void;
  onKeyPress: (event: KeyboardEvent) => void;
  onBlur: () => void;
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
}

export const Attribute: FC<PropsAttributeComponent> = ({
  attribute,
  show,
  newLevel,
  onShow,
  onKeyPress,
  onBlur,
  onChange,
}) => (
  <li className={styles.attribute}>
    <div className={styles.attribute_left}>
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
          {attribute.levels.map((level) => (
            <li>
              <span className={styles.circle}></span>
              {level.name}
            </li>
          ))}
          <li>
            <span className={styles.circle}></span>
            <input
              className={styles.input}
              placeholder={"Add level"}
              value={newLevel}
              onChange={onChange}
              onKeyDown={onKeyPress}
              onBlur={onBlur}
            ></input>
          </li>
        </ul>
      ) : (
        <p>{attribute.levels.length} levels</p>
      )}
    </div>
  </li>
);
