import { useState } from "react";
import { DocumentItem, IDocument } from "./__item/documents__item";
import styles from "./documents.module.css";

export const Documents = ({
  active,
  documents,
}: {
  active: string;
  documents: IDocument[];
}) => {
  return (
    <ul className={styles.list}>
      {documents.map((document) => (
        <DocumentItem
          name={document.name}
          active={active == document.key}
          key={document.key}
          id={document.key as string}
        />
      ))}
    </ul>
  );
};
