import React, { FC, useEffect, useState } from "react";

import styles from "./survey__outcome-types.module.css";
import CustomDropdown from "@/components/restrictions/dropdown";
import { SettingsExplanation } from "@/components/settings/__explanation/settings__explanation";
import { useAttributes } from "@/context/attributes_context";

export interface SurveyOutcomeTypesProps {}

const mapping = {
  mcq: "Multiple Choice Question",
  slider: "Slider",
  ranking: "Ranking",
};

export const SurveyOutcomeTypes: FC<SurveyOutcomeTypesProps> = ({}) => {
  const { instructions, handleInstructions } = useAttributes();
  const [selected, setSelected] = useState<"mcq" | "slider" | "ranking">(
    instructions?.outcomeType || "mcq"
  );

  useEffect(() => {
    // Correctly pass the outcomeType to handleInstructions
    handleInstructions(selected, "outcomeType");
  }, [selected]);

  useEffect(() => {
    setSelected(instructions?.outcomeType || "mcq");
  }, [instructions]);

  return (
    <div className={styles.survey__outcome_types}>
      <div className={styles.survey__outcome_types__explanation}>
        <p>Select outcome type</p>
        <SettingsExplanation explanation="Select the type of outcome you want to use for your survey. You can choose between a single outcome, multiple outcomes, or a range of outcomes." />
      </div>

      <CustomDropdown
        items={["Multiple Choice Question", "Slider", "Ranking"]}
        value={mapping[selected]}
        setSelected={(item) => {
          switch (item) {
            case "Multiple Choice Question":
              setSelected("mcq");
              break;
            case "Slider":
              setSelected("slider");
              break;
            case "Ranking":
              setSelected("ranking");
              break;
          }
        }}
      />
    </div>
  );
};
