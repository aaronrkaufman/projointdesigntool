"use client";

import { useState } from "react";
import { Documents } from "./documents/documents";
import styles from "./sidebar.module.css";
import { IDocument } from "./documents/document";
import { useRouter } from "next/router";

export const Sidebar = ({ active }: { active: string }) => {
  const [documents, setDocuments] = useState<IDocument[]>([
    { name: "document", key: 0 },
    { name: "immigrant survey", key: 1 },
    { name: "3", key: 2 },
  ]);

  const router = useRouter();

  const handleAddDoc = () => {
    const hasUntitled = documents.some(
      (element) => element.name === "Untitled"
    );

    if (!hasUntitled) {
      setDocuments((prev) => {
        const newDoc = { name: "Untitled", key: prev.length + 1 };
        // Now navigate to the new document page
        return [...prev, newDoc];
      });
      router.push(`/documents/${encodeURIComponent("Untitled")}`);
    }
  };

  return (
    <div className={styles.sidebar}>
      <div className={styles.top}>
        <h2>Documents</h2>
        <button onClick={handleAddDoc}>+</button>
      </div>
      <Documents documents={documents} active={active} />
    </div>
  );
};
