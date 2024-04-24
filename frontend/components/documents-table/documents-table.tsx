import React, { FC } from "react";

import styles from "./documents-table.module.css";

export interface DocumentsTableProps {}

export const DocumentsTable: FC<DocumentsTableProps> = ({}) => {
  return <div className={styles.documents_table}></div>;
};

