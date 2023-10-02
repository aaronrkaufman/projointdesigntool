"use client";
import styles from "./survey.module.css";
import { AddAttribute } from "./add_attribute";
import { useState } from "react";
import { Attribute, IAttribute } from "./attribute";

export const Survey = () => {
  const [attributes, setAttributes] = useState<IAttribute[]>([
    {
      name: "Age",
      levels: [{ name: "10-20" }, { name: "20-30" }, { name: "30-40" }],
    },
    {
      name: "Education",
      levels: [
        { name: "No Formal" },
        { name: "4th Grade" },
        { name: "8th Grade" },
        { name: "High School" },
        { name: "Two-Year College" },
      ],
    },
  ]);

  return (
    <section className={styles.survey}>
      <h2>Immigrant Survey</h2>
      <ul className={styles.attributes}>
        {attributes.map((attribute, index) => (
          <Attribute key={index} attribute={attribute} />
        ))}
      </ul>
      <AddAttribute />
    </section>
  );
};
