import { Button } from "../button";
import styles from "./restrictions.module.css";
import { Statement } from "./statement";

export const Restrictions = () => {
  return (
    <section className={styles.section}>
      <div className={styles.top}>
        <h2>Restrictions</h2>
        <p>List of attribute-level pairs that can’t be together in a profile</p>
      </div>
      <div className={styles.container}>
        <div className={styles.left}>
          <ul className={styles.restrictions}></ul>
          <Button
            text="Add a restriction statement"
            onClick={() => {
              console.log("");
            }}
          />
        </div>
        <div className={styles.right}>
          <Statement part="IF" />
          <Statement part="THEN" />
        </div>
      </div>
    </section>
  );
};
