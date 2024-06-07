import React, { FC } from "react";

import styles from "./tutorial.module.css";
import parse from "html-react-parser";

export interface TutorialProps {
  tutorialData: string;
}

export const Tutorial: FC<TutorialProps> = ({ tutorialData }) => {
  return (
    <section className={styles.tutorial}>
      <div className={styles.tutorial__content}>{parse(tutorialData)}</div>
    </section>
  );
};
