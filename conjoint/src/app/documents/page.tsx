import { Header } from "@/components/header";
import styles from "../profile/page.module.css";
import { Sidebar } from "@/components/sidebar";
import { SurveyContainer } from "@/components/survey/survey.container";

const Profile = () => {
  return (
    <>
      <Header></Header>
      <main className={styles.main}>
        <Sidebar active={"1"} />
        <SurveyContainer />
      </main>
    </>
  );
};

export default Profile;
