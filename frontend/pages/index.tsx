"use client";

import styles from "../styles/page.module.css";
import { Sidebar } from "../components/sidebar/sidebar";
import { DocumentsTable } from "@/components/documents-table/documents-table";

function DocumentsPage() {
  return (
    <>
      <main className={styles.main}>
        <Sidebar active={"documentName"} />
        {/* <SurveyContainer /> */}
        <DocumentsTable />
      </main>
    </>
  );
}

export default DocumentsPage;
