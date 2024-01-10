import { useEffect, useState } from "react";
import styles from "../survey/survey.module.css";

interface IWeight {
  index: number;
  value: number;
  onWeightChange: (index: number, value: number) => void;
}

export const Weight = ({ index, value, onWeightChange }: IWeight) => {

  useEffect(() => {
    setWeight(value.toString());
  }, [value]);

  const [weight, setWeight] = useState<string>(value.toString());

  const changeHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = event.target.value;

    const match = inputValue.match(/^0\.(\d{0,3})$/);
    if (match) {
      setWeight(inputValue); // Update the state if the input value is valid
      onWeightChange(index, parseFloat(inputValue));
    }
  };
  return (
    <li className={styles.weight}>
      <input
        className={`${styles.input}`}
        value={weight}
        onChange={changeHandler}
        pattern="0\.[0-9]*"
      ></input>
    </li>
  );
};
