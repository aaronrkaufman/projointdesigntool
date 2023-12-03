import { useState } from "react";
import { Document, IDocument } from "./document";
import styles from "./documents.module.css";
import { Button } from "../button";

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
        <Document
          name={document.name}
          active={active == document.key}
          key={document.key}
          id={document.key as string}
        />
      ))}
      {/* <li>
        <Button text="New document" onClick={() => {}} />
      </li> */}
    </ul>
  );
};
