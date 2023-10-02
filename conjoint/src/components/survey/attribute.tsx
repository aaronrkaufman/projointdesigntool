import { useState } from "react";
import styles from "./survey.module.css";

export interface ILevel {
  name: string;
  weight?: number;
}

export interface IAttribute {
  name: string;
  levels: ILevel[];
}

export const Attribute = ({ attribute }: { attribute: IAttribute }) => {
  const [show, setShow] = useState<Boolean>(false);
  return (
    <li className={styles.attribute}>
      <div className={styles.attribute_left}>
        <svg
          onClick={() => setShow(!show)}
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
          <ul className={`${styles.levels} ${show ? styles.open : ""}`}>
            {attribute.levels.map((level) => (
              <li>
                <span className={styles.circle}></span>
                {level.name}
              </li>
            ))}
          </ul>
        ) : (
          <p>{attribute.levels.length} levels</p>
        )}
      </div>
    </li>
  );
};
