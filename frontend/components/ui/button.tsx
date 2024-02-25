import styles from "./button.module.css";

interface IButton {
  text: string;
  onClick: () => void;
  disabled?: boolean;
}

export const Button = (props: IButton) => {
  return (
    <button
      disabled={props.disabled ? props.disabled : false}
      className={styles.btn}
      onClick={props.onClick}
    >
      {props.text}
    </button>
  );
};
