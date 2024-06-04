import { ReactNode } from "react";
import styles from "./button.module.css";

interface IButton {
  text: string;
  onClick: () => void;
  disabled?: boolean;
  icon?: ReactNode;
  size?: string;
  bg?: string;
  effect?: boolean;
}

export const Button = (props: IButton) => {
  return (
    <button
      disabled={props.disabled ? props.disabled : false}
      className={props.effect ? styles.btnEffect : styles.btn}
      onClick={props.onClick}
      style={{
        fontSize: props.size ? props.size : "1rem",
        backgroundColor: props.bg
          ? props.bg
          : props.effect
          ? ""
          : "var(--blue)",
      }}
    >
      {props.icon} {props.text}
    </button>
  );
};
