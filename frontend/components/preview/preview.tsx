// CarSelection.tsx
import React, { useState } from "react";
import styles from "./preview.module.css"; // Make sure to create this CSS module
import { Button } from "../ui/button";
import { IInstructions } from "../../context/attributes_context";

export interface IPreview {
  attributes: string[];
  previews: string[][];
  instructions: IInstructions;
  setRefresh?: (refresh: boolean) => void;
}

const Preview = ({
  attributes,
  previews,
  instructions,
  setRefresh,
}: IPreview) => {
  const [selectedCar, setSelectedCar] = useState(null);

  return (
    <section className={styles.section}>
      <div className={styles.sectionContainer}>
        <div className={styles.top}>
          <h2>Preview</h2>
          <Button
            text="Refresh"
            onClick={() => setRefresh && setRefresh(true)}
          />
        </div>
        <div className={styles.instructions}>
          {instructions && instructions.description}
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
                <li className={styles.profile_name}>Profile {index + 1}</li>
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
        <div className={styles.instructions}>
          {instructions && instructions.instructions}
        </div>
      </div>
    </section>
  );
};

export default Preview;
