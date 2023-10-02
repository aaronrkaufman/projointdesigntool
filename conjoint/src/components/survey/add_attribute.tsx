import styles from "./survey.module.css";

interface AddAttributeProps {
  onCreate: () => void;
}

export const AddAttribute = ({ onCreate }: AddAttributeProps) => {
  return (
    <div className={styles.container}>
      <span className={styles.line}></span>
      <button className={styles.btn} onClick={onCreate}>
        Add Attribute
      </button>
    </div>
  );
};
