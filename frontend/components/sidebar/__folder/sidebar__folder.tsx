import React, { FC, useState } from "react";

import styles from "./sidebar__folder.module.css";
import { ExpandIcon } from "@/components/ui/icons";

export interface SidebarFolderProps {
  name: string;
  element: React.ReactNode;
  active?: boolean;
}

export const SidebarFolder: FC<SidebarFolderProps> = ({
  name,
  element,
  active,
}) => {
  const [isOpen, setIsOpen] = useState(active ? active : false);

  const toggleFolder = () => setIsOpen(!isOpen);

  return (
    <div className={styles.sidebar__folder}>
      <div
        className={`${styles.sidebar__folder__header} ${
          isOpen ? styles.active : ""
        }`}
        onClick={toggleFolder}
      >
        <p>{name}</p>
        <ExpandIcon
          fill={isOpen ? "var(--blue)" : "#778C9F"}
          onClick={toggleFolder}
          expand={!isOpen}
          size={1.25}
        />
      </div>
      {isOpen && (
        <div className={styles.sidebar__folder__content}>{element}</div>
      )}
    </div>
  );
};
