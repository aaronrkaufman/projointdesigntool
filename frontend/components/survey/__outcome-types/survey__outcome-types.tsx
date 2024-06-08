import React, { FC, useEffect, useState } from "react";

import styles from "./survey__outcome-types.module.css";
import CustomDropdown from "@/components/restrictions/dropdown";
import { SettingsExplanation } from "@/components/settings/__explanation/settings__explanation";
import { useAttributes } from "@/context/attributes_context";
import naming from "@/naming/english.json";

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
        <p>{naming.surveyPage.outcomeType.value}</p>
        <SettingsExplanation
          explanation={naming.surveyPage.outcomeType.subtitle}
        />
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
