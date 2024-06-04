"use client";

import styles from "../../../styles/page.module.css";
import { Sidebar } from "@/components/sidebar/sidebar";
import { GetServerSideProps } from "next";
import { getTutorial } from "@/services/api";
import { Tutorial } from "@/components/tutorial/tutorial";
import { useEffect, useState } from "react";

interface IServerProps {
  params: {
    tutorial: string;
  };
}

function TutorialPage({ params }: IServerProps) {
  const [tutorialData, setTutorialData] = useState("");
  const tutorial = params.tutorial;

  useEffect(() => {
    if (tutorial) {
      getTutorial(tutorial)
        .then((data) => {
          setTutorialData(data);
        })
        .catch((error) => {
          console.error("Failed to fetch tutorial data:", error);
        });
    }
  }, [tutorial]);

  return (
    <>
      <main className={styles.main}>
        <Sidebar active={tutorial} />
        <Tutorial tutorialData={tutorialData} />
      </main>
    </>
  );
}


//TODO: maybe use static paths and props next time
export const getServerSideProps: GetServerSideProps = async (context) => {
  const tutorial = context.params?.tutorial;

  // Check if 'tutorial' is a string (or an array of strings if you allow that)
  if (typeof tutorial !== "string") {
    // Handle the case where 'tutorial' is not provided or is not a string
    // return { notFound: true }; // Or redirect to another page
  }

  // You can perform server-side operations here, like fetching data based on the tutorial name
  // ...

  // Then return the props
  return {
    props: {
      params: {
        tutorial: tutorial || "",
      },
    },
  };
};

export default TutorialPage;
