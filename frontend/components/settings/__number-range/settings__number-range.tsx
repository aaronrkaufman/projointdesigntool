import React, { FC } from "react";

import styles from "./settings__number-range.module.css";
import { SettingsExplanation } from "../__explanation/settings__explanation";

export interface SettingsNumberRangeProps {
  value: number;
  onChange: (newValue: number) => void;
  min: number;
  max: number;
  label: string;
  explanation: string;
}

export const SettingsNumberRange: FC<SettingsNumberRangeProps> = ({
  value,
  onChange,
  min,
  max,
  label,
  explanation,
}) => {
  const handleIncrement = () => {
    if (value < max) {
      onChange(value + 1);
    }
  };

  const handleDecrement = () => {
    if (value > min) {
      onChange(value - 1);
    }
  };

  return (
    <div className={styles.settings__number_range}>
      <div className={styles.label}>
        <h3>{label}</h3>
        <SettingsExplanation explanation={explanation} />
      </div>
      <div className={styles.controls}>
        <input
          type="number"
          id="profile-number"
          min={min}
          max={max}
          value={value}
          readOnly
        />
        <button onClick={handleIncrement} className={styles.arrow}>
          <svg
            width="14"
            height="8"
            viewBox="0 0 14 8"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M1 7L7 1L13 7"
              stroke="#778C9F"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
        <button onClick={handleDecrement} className={styles.arrow}>
          <svg
            width="14"
            height="8"
            viewBox="0 0 14 8"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M13 1L7 7L1 1"
              stroke="#778C9F"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
      </div>
    </div>
  );
};
