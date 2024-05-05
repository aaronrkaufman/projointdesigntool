import React, { FC, ReactNode } from "react";

import styles from "./settings__explanation.module.css";

export interface SettingsExplanationProps {
  explanation: ReactNode;
}

export const SettingsExplanation: FC<SettingsExplanationProps> = ({
  explanation,
}) => <div className={styles.settings__explanation}>{explanation}</div>;
