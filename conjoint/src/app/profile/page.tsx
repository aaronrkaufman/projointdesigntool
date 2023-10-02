import { Header } from "@/components/header";
import styles from "./page.module.css";
import { Sidebar } from "@/components/sidebar";
import { Survey } from "@/components/survey/survey";

const Profile = () => {
  return (
    <>
      <Header></Header>
      <main className={styles.main}>
        <Sidebar />
        <Survey />
      </main>
    </>
  );
};

export default Profile;
