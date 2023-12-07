import { useState } from "react";
import { useAttributes } from "../../context/attributes_context";
import styles from "./restrictions.module.css";

export const Statement = () => {
  // Define the state with TypeScript type
  const [selectedValue, setSelectedValue] = useState<string>("");

  const { attributes } = useAttributes();

  // Handler function with TypeScript type for the event
  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedValue(event.target.value);
  };

  const getAttributeLevels = (attributeName: string) => {
    const index = attributes.findIndex((attr) => attr.name == attributeName);
    return attributes[index].levels;
  };
  return (
    <div className={styles.statement_container}>
      <div className={styles.statement}>
        <p>IF</p>
        <select
          className={styles.select}
          value={selectedValue}
          onChange={handleChange}
        >
          {attributes.map((attr) => (
            <option value={attr.name}>{attr.name}</option>
          ))}
        </select>
        <p>=</p>
        <select className={styles.select}>
          {selectedValue
            ? getAttributeLevels(selectedValue).map((level) => (
                <option value={level.name}>{level.name}</option>
              ))
            : ""}
        </select>
      </div>
    </div>
  );
};
