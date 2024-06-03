import React, { FC } from "react";

import styles from "./sidebar__tutorials.module.css";
import Link from "next/link";

export interface SidebarTutorialsProps {
  tutorials: string[];
  active: string;
}

export const SidebarTutorials: FC<SidebarTutorialsProps> = ({
  tutorials,
  active,
}) => (
  <ul className={styles.sidebar__tutorials}>
    {tutorials.map((tutorial) => (
      <li
        key={tutorial}
        className={active.includes(tutorial) ? styles.active : ""}
      >
        <Link href={`/tutorials/${tutorial}`}>
          <p className={styles.sidebar__tutorials__link}>{tutorial}</p>
        </Link>
      </li>
    ))}
  </ul>
);
