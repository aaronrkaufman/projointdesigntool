import styles from "../../../styles/page.module.css";
import { Sidebar } from "@/components/sidebar/sidebar";
import { GetStaticPaths, GetStaticProps } from "next";
import { getTutorial, getTutorials } from "@/services/api";
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

export const getStaticPaths: GetStaticPaths = async () => {
  // Assuming getTutorials is available and fetches all tutorial slugs
  const tutorials = await getTutorials(); // This function should be implemented to fetch all tutorial identifiers
  const paths = tutorials.map((tutorial: string) => ({
    params: { tutorial },
  }));

  return { paths, fallback: false };
};

export const getStaticProps: GetStaticProps = async (context) => {
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
    revalidate: 3600, // Revalidate at most once per hour
  };
};

export default TutorialPage;
