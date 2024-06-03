"use client";

import styles from "../../../styles/page.module.css";
import { Sidebar } from "@/components/sidebar/sidebar";
import { GetServerSideProps } from "next";
import { getTutorial } from "@/services/api";
import { Tutorial } from "@/components/tutorial/tutorial";

interface ITutorialProps {
  tutorialData: string;
  tutorial: string;
}

function TutorialPage({ tutorialData, tutorial }: ITutorialProps) {
  return (
    <>
      <main className={styles.main}>
        <Sidebar active={tutorial} />
        <Tutorial tutorialData={tutorialData} />
      </main>
    </>
  );
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const tutorial = context.params?.tutorial as string;

  if (!tutorial) {
    return { notFound: true };
  }

  const tutorialData = await getTutorial(tutorial);

  return {
    props: {
      tutorialData: tutorialData || "",
      tutorial,
    },
  };
};

export default TutorialPage;
