import React, { FC, useState } from "react";

import styles from "./survey__outcome-types.module.css";
import CustomDropdown from "@/components/restrictions/dropdown";
import { SettingsExplanation } from "@/components/settings/__explanation/settings__explanation";

export interface SurveyOutcomeTypesProps {}

export const SurveyOutcomeTypes: FC<SurveyOutcomeTypesProps> = ({}) => {
  const [selected, setSelected] = useState<string>("Multiple Choice Question");

  return (
    <div className={styles.survey__outcome_types}>
      <div className={styles.survey__outcome_types__explanation}>
        <p> Select outcome type </p>
        <SettingsExplanation explanation="Select the type of outcome you want to use for your survey. You can choose between a single outcome, multiple outcomes, or a range of outcomes." />
      </div>

      <CustomDropdown
        items={["Multiple Choice Question", "Slider", "Ranking"]}
        value={selected}
        setSelected={setSelected}
      />
    </div>
  );
};
