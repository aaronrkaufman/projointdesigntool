"use client";

import styles from "../styles/page.module.css";
import { Sidebar } from "../components/sidebar/sidebar";
import { SurveyContainer } from "../components/survey/survey.container";
import ColumnGroupingTable from "@/components/documents-table/test-table";

function DocumentsPage() {
  return (
    <>
      <main className={styles.main}>
        <Sidebar active={"documentName"} />
        {/* <SurveyContainer /> */}
        <ColumnGroupingTable />
      </main>
    </>
  );
}

export default DocumentsPage;
