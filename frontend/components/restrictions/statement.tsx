import { useState } from "react";
import { useAttributes } from "../../context/attributes_context";
import styles from "./restrictions.module.css";
import CustomDropdown from "./dropdown";

export const Statement = () => {
  // Define the state with TypeScript type
  const [selectedValue, setSelectedValue] = useState<string>("");
  const [selectedLvl, setSelectedLvl] = useState<string>("");

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
        <CustomDropdown
          items={attributes.map((attr) => attr.name)}
          setSelected={setSelectedValue}
        />
        <p>=</p>
        <CustomDropdown
          items={
            selectedValue
              ? getAttributeLevels(selectedValue).map((level) => level.name)
              : []
          }
          setSelected={setSelectedLvl}
        />
      </div>
    </div>
  );
};
