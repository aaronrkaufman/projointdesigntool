"use client";

import { Documents } from "./documents/documents";
import styles from "./sidebar.module.css";

export const Sidebar = ({ active }: { active: string }) => {
  return (
    <div className={styles.sidebar}>
      <div className={styles.top}>
        <h2>Documents</h2>
        <button>+</button>
      </div>
      <Documents active={active} />
    </div>
  );
};
