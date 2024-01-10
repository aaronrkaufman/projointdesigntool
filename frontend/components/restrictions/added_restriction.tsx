import { useAttributes } from "../../context/attributes_context";
import styles from "./restrictions.module.css";

interface IAddedRestriction {
  restriction: string[][];
  index: number;
}

const showRestrictions = (restriction: string[][]) => {
  return (
    <>
      {"if"} <span className={styles.state}>{restriction[0].join(" ")}</span>
      <br></br> {"then "}
      <span className={styles.state}>{restriction[1].join(" ")}</span>
    </>
  );
};

export const AddedRestriction = ({ restriction, index }: IAddedRestriction) => {
  const { deleteRestrictionFromAttribute } = useAttributes();

  return (
    <li className={styles.restriction}>
      <div>{showRestrictions(restriction)} </div>
      <p
        onClick={() => {
          deleteRestrictionFromAttribute(index);
        }}
        className={styles.deleteRestriction}
      >
        x
      </p>
    </li>
  );
};
