import styles from "./survey.module.css";
import naming from "@/naming/english.json";
interface AddAttributeProps {
  onCreate: () => void;
}

export const AddAttribute = ({ onCreate }: AddAttributeProps) => {
  return (
    <div className={styles.container}>
      <span className={styles.line}></span>
      <button className={styles.btn} onClick={onCreate}>
        {naming.surveyPage.attribute.addAttribute.value}
      </button>
    </div>
  );
};
