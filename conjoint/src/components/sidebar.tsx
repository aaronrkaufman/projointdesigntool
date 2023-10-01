import styles from "./sidebar.module.css";

export const Sidebar = () => {
  return (
    <div className={styles.sidebar}>
      <h2>Documents</h2>
      <ul className={styles.list}>
        <li>Immigrant Survey</li>
      </ul>
    </div>
  );
};
