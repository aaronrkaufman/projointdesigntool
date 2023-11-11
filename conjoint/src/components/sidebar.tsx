"use client";

import { Documents } from "./documents/documents";
import styles from "./sidebar.module.css";

export const Sidebar = ({ active }: { active: number }) => {
  return (
    <div className={styles.sidebar}>
      <h2>Documents</h2>
      <Documents />
    </div>
  );
};
