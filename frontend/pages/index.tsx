"use client";

import styles from "../styles/page.module.css";
import { Sidebar } from "../components/sidebar/sidebar";
import { SurveyContainer } from "../components/survey/survey.container";

function DocumentsPage() {
  return (
    <>
      <main className={styles.main}>
        <Sidebar active={"documentName"} />
        <SurveyContainer />
      </main>
    </>
  );
}

export default DocumentsPage;
