import { useState } from "react";
import { Document, IDocument } from "./document";
import styles from "./documents.module.css"

export const Documents = () => {
  const [documents, setDocuments] = useState<IDocument[]>([
    { name: "1", key: 0 },
  ]);
  return (
    <ul className={styles.list}>
      {documents.map((document) => (
        <Document name={document.name} key={document.key} />
      ))}
    </ul>
  );
};
