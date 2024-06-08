// CarSelection.tsx
import React, { useMemo, useState } from "react";
import styles from "./preview.module.css"; // Make sure to create this CSS module
import { Button } from "../ui/button";
import { IInstructions, useAttributes } from "../../context/attributes_context";
import ExportDropdown from "../export/export";
import naming from "@/naming/english.json";
import { PreviewMcq } from "./__mcq/preview__mcq";
import { PreviewRanking } from "./__ranking/preview__ranking";
import { PreviewSlider } from "./__slider/preview__slider";

export interface IPreview {
  attributes: string[];
  previews: string[][];
  instructions: IInstructions;
  setRefresh?: (refresh: boolean) => void;
  refresh?: boolean;
}

export interface IProfile {
  value: string;
  id: string;
}

const Preview = ({
  attributes,
  previews,
  instructions,
  setRefresh,
  refresh,
}: IPreview) => {
  const profiles: IProfile[] = useMemo(
    () =>
      previews.map((_, index) => ({
        value: `Profile ${index + 1}`,
        id: `${index + 1}`,
      })),
    [previews]
  );

  const renderOutcome = () => {
    switch (instructions?.outcomeType) {
      case "mcq":
        return (
          <PreviewMcq refresh={refresh ? refresh : false} options={profiles} />
        );
      case "ranking":
        return (
          <PreviewRanking
            refresh={refresh ? refresh : false}
            profiles={profiles}
          />
        );
      case "slider":
        return <PreviewSlider profiles={profiles} />;
    }
  };

  return (
    <section className={styles.section}>
      <div className={styles.sectionContainer}>
        <div className={styles.top}>
          <h2>Preview</h2>
          <div className={styles.buttons}>
            <Button
              text={naming.previewPage.refreshButton.value}
              onClick={() => setRefresh && setRefresh(true)}
            />
            <ExportDropdown size="small" />
          </div>
        </div>
        <div className={styles.instructions}>
          {instructions && instructions.description}
        </div>
        <div className={styles.cardContainer}>
          <ul className={styles.attributes}>
            {attributes.map((attribute, index) => (
              <li key={attribute + index}>{attribute}:</li>
            ))}
          </ul>
          {previews.map((preview, index) => (
            <div key={index} className={styles.card}>
              <ul className={styles.cardContent}>
                <li className={styles.profile_name}>Profile {index + 1}</li>
                {preview.map((choice, index) => (
                  <li key={choice + index}>{choice}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className={styles.instructions}>
          {instructions && instructions.instructions}
        </div>
        {renderOutcome()}
      </div>
    </section>
  );
};

export default Preview;
