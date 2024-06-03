import React, { FC } from "react";

import styles from "./tutorial.module.css";
import parse from "html-react-parser";

export interface TutorialProps {
  tutorialData: string;
}

export const Tutorial: FC<TutorialProps> = ({ tutorialData }) => {
  return <section className={styles.tutorial}>{parse(tutorialData)}</section>;
};
