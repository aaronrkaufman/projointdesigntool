import { useState } from "react";
import { Document, IDocument } from "./document";
import styles from "./documents.module.css";
import { Button } from "../button";

export const Documents = ({ active }: { active: string }) => {
  const [documents, setDocuments] = useState<IDocument[]>([
    { name: "document", key: 0 },
    { name: "immigrant survey", key: 1 },
    { name: "3", key: 2 },
  ]);
  return (
    <ul className={styles.list}>
      {documents.map((document) => (
        <Document
          name={document.name}
          active={active == document.name}
          key={document.key}
        />
      ))}
      {/* <li>
        <Button text="New document" onClick={() => {}} />
      </li> */}
    </ul>
  );
};
