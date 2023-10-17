import styles from "./button.module.css";

interface IButton {
  text: string;
  onClick: () => void;
}

export const Button = (props: IButton) => {
  return (
    <button className={styles.btn} onClick={props.onClick}>
      {props.text}
    </button>
  );
};
