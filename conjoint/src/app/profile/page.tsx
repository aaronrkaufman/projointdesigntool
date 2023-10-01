import { Header } from "@/components/header";
import styles from "./page.module.css";
import { Sidebar } from "@/components/sidebar";

const Profile = () => {
  return (
    <>
      <Header></Header>
      <main className={styles.main}>
        <Sidebar />
      </main>
    </>
  );
};

export default Profile;
