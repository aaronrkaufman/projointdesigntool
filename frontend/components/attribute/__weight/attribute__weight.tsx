import React, { FC, useEffect, useState } from "react";

import styles from "./attribute__weight.module.css";

export interface AttributeWeightProps {
  index: number;
  value: number;
  onWeightChange: (index: number, value: number) => void;
}

export const AttributeWeight: FC<AttributeWeightProps> = ({
  index,
  value,
  onWeightChange,
}) => {
  useEffect(() => {
    setWeight(value.toString());
  }, [value]);

  const [weight, setWeight] = useState<string>(value.toString());

  const changeHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = event.target.value;
    if (inputValue === "") {
      setWeight("");
    } else {
      const match = inputValue.match(/^(?:[1-9]?[0-9])$/); // Matches numbers from 0 to 99
      if (match) {
        setWeight(inputValue); // Update the state if the input value is valid
        onWeightChange(index, parseInt(inputValue, 10));
      }
    }
  };

  const onBlurHandler = (event: React.FocusEvent<HTMLInputElement>) => {
    const inputValue = event.target.value;
    if (inputValue === "") {
      setWeight("0");
      onWeightChange(index, 0);
    }
  };

  return (
    <li className={styles.attribute__weight}>
      <input
        className={`${styles.input}`}
        value={weight}
        onChange={changeHandler}
        onBlur={onBlurHandler}
        pattern="[0-9]{1,2}" // Pattern to match numbers from 0 to 99
      ></input>
      <span>%</span>
    </li>
  );
};
