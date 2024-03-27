import { useState } from "react";
import styles from "../survey/survey.module.css"; // Adjust the styles accordingly
import { ExpandIcon } from "../ui/icons";

interface Props {
  addNewAttribute: (name: string) => void;
  cancelNewAttribute: () => void;
  onBlur: () => void;
  onKeyDown: (event: React.KeyboardEvent) => void;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export const AttributeCreator: React.FC<Props> = ({
  addNewAttribute,
  cancelNewAttribute,
  onBlur,
  onKeyDown,
  onChange,
}) => {
  const [name, setName] = useState("");

  // Bind setName to onChange event
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setName(event.target.value);
    if (onChange) onChange(event); // propagate event upward
  };

  // Bind onBlur and onKeyDown events
  const handleBlur = () => {
    onBlur && onBlur();
    if (name.trim() === "") cancelNewAttribute();
    else addNewAttribute(name);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    onKeyDown && onKeyDown(event); // propagate event upward
    if (event.key === "Enter" && name.trim() !== "") addNewAttribute(name);
  };

  return (
    <li className={styles.attribute}>
      <div className={styles.attribute_left}>
        <ExpandIcon expand={true} size={1.25} />
        <input
          autoFocus
          placeholder="Attribute Name"
          value={name}
          onChange={handleChange}
          onBlur={handleBlur}
          onKeyDown={handleKeyPress}
          className={styles.input}
        />
      </div>
      <div className={styles.attribute_right}>
        <p>0 levels</p>
      </div>
    </li>
  );
};
