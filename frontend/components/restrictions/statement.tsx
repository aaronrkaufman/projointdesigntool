import { useEffect, useState } from "react";
import { useAttributes } from "../../context/attributes_context";
import styles from "./restrictions.module.css";
import CustomDropdown from "./dropdown";

interface IStatement {
  part: "IF" | "THEN";
}

export const Statement: React.FC<IStatement> = ({ part }) => {
  // Define the state with TypeScript type
  const [selectedAttr, setSelectedAttr] = useState<string>("select attribute");
  const [selectedLvl, setSelectedLvl] = useState<string>("selece level");
  const [sign, setSign] = useState<string>("=");

  const { attributes } = useAttributes();

  useEffect(() => {
    setSelectedLvl("select level");
  }, [selectedAttr]);

  const getAttributeLevels = (attributeName: string) => {
    const index = attributes.findIndex((attr) => attr.name == attributeName);
    return attributes[index] ? attributes[index].levels : [];
  };
  return (
    <div className={styles.statement_container}>
      <div className={styles.statement}>
        <p>{part}</p>
        <CustomDropdown
          value={selectedAttr}
          items={attributes.map((attr) => attr.name)}
          setSelected={setSelectedAttr}
        />
        <CustomDropdown
          sign={true}
          value={sign}
          items={["=", "!="]}
          setSelected={setSign}
        />
        <CustomDropdown
          value={selectedLvl}
          items={
            selectedAttr
              ? getAttributeLevels(selectedAttr).map((level) => level.name)
              : []
          }
          setSelected={setSelectedLvl}
        />
      </div>
    </div>
  );
};
