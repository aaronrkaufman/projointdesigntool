// CarSelection.tsx
import React, { useState } from "react";
import styles from "./preview.module.css"; // Make sure to create this CSS module
import { Button } from "../button";

export interface IPreview {
  attributes: string[];
  previews: string[][];
  setRefresh?: (refresh: boolean) => void;
}

const Preview = ({ attributes, previews, setRefresh }: IPreview) => {
  const [selectedCar, setSelectedCar] = useState(null);

  // const handleSelectCar = (index: any) => {
  //   setSelectedCar(index);
  // };
  console.log("attrs:", attributes, previews);

  return (
    <section className={styles.section}>
      <div className={styles.top}>
        <h2>Preview</h2>
        <Button text="Refresh" onClick={() => setRefresh && setRefresh(true)} />
      </div>
      <div className={styles.cardContainer}>
        <ul className={styles.attributes}>
          {attributes.map((attribute) => (
            <li key={attribute}>{attribute}:</li>
          ))}
        </ul>
        {previews.map((preview, index) => (
          <div
            key={index}
            className={
              selectedCar === index ? styles.cardSelected : styles.card
            }
          >
            <ul className={styles.cardContent}>
              {preview.map((choice) => (
                <li key={choice}>{choice}</li>
              ))}
            </ul>
            {/* <div className={styles.buttonContainer}>
            <button
              onClick={() => handleSelectCar(index)}
              className={styles.selectButton}
            >
              {selectedCar === index ? "Selected" : "Select"}
            </button>
          </div> */}
          </div>
        ))}
      </div>
    </section>
  );
};

export default Preview;
