// CarSelection.tsx
import React, { useState } from "react";
import styles from "./preview.module.css"; // Make sure to create this CSS module

const cars = [
  { brand: "Ford", type: "SUV", engine: "V6, 3.6 liter", price: "$36,599" },
  { brand: "Chevy", type: "Truck", engine: "V8, 5.7 liter", price: "$42,999" },
  // ... add other car objects
];

export interface IPreview {
  attributes: string[];
  previews: string[][];
}

const Preview = ({ attributes, previews }: IPreview) => {
  const [selectedCar, setSelectedCar] = useState(null);

  const handleSelectCar = (index: any) => {
    setSelectedCar(index);
  };

  return (
    <div className={styles.cardContainer}>
      <ul className={styles.attributes}>
        {attributes.map((attribute) => (
          <li key={attribute}>{attribute}:</li>
        ))}
      </ul>
      {previews.map((preview, index) => (
        <div
          key={index}
          className={selectedCar === index ? styles.cardSelected : styles.card}
        >
          <ul className={styles.cardContent}>
            {preview.map((choice) => (
              <li key={choice}>{choice}</li>
            ))}
          </ul>
          <div className={styles.buttonContainer}>
            <button
              onClick={() => handleSelectCar(index)}
              className={styles.selectButton}
            >
              {selectedCar === index ? "Selected" : "Select"}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Preview;
