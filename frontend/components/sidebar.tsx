"use client";

import { useContext, useEffect, useState } from "react";
import { Documents } from "./documents/documents";
import styles from "./sidebar.module.css";
import { IDocument } from "./documents/document";
import { useRouter } from "next/router";
import { v4 as uuidv4 } from "uuid";
import { useAttributes } from "../context/attributes_context";
import { FileAdd, LightTooltip } from "./ui/icons";

export const Sidebar = ({ active }: { active: string }) => {
  const [documents, setDocuments] = useState<IDocument[]>([]);
  const { storageChanged, setStorageChanged } = useAttributes();

  useEffect(() => {
    // Function to load documents from localStorage
    const loadDocuments = (): IDocument[] => {
      const docs: IDocument[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith("attributes-")) {
          const item = localStorage.getItem(key);
          if (item) {
            const data = JSON.parse(item);
            docs.push({
              name: data.name,
              key: key.substring(11), // assuming the key is in the format 'attributes-uniqueid'
              // Include other document properties as needed
            });
          }
        }
      }
      return docs;
    };

    setDocuments(loadDocuments());
  }, [storageChanged]);

  const router = useRouter();

  const handleAddDoc = () => {
    const uniqueId = uuidv4();
    const dataToSave = {
      attributes: [],
      lastEdited: new Date(), // Update last edited time
      name: "Untitled",
    };
    localStorage.setItem(`attributes-${uniqueId}`, JSON.stringify(dataToSave));
    setStorageChanged(1);
    router.push(`/documents/${encodeURIComponent(uniqueId)}`);
  };

  return (
    <div className={styles.sidebar}>
      <div className={styles.top} onClick={handleAddDoc}>
        <h3>Projoint</h3>
        {/* <button onClick={handleAddDoc}>+</button> */}
        <LightTooltip
          disableInteractive
          title="New file"
          arrow
          placement="right"
        >
          <FileAdd />
        </LightTooltip>
      </div>
      <span className={styles.line}></span>
      <Documents documents={documents} active={active} />
    </div>
  );
};
