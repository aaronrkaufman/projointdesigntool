import { useEffect, useState } from "react";
import { useAttributes } from "../../context/attributes_context";
import styles from "./restrictions.module.css";
import CustomDropdown from "./dropdown";
import { Button } from "../button";
import { StatementProps } from "./restrictions";

interface IStatement {
  // part: "IF" | "THEN" | "AND";
  statement: StatementProps;
  index: number;
  addStatement?: () => void;
  changeStatement?: (
    index: number,
    attributeName?: any,
    levelName?: any,
    propositionName?: any,
    part?: any
  ) => void;
}

export const Statement: React.FC<IStatement> = ({
  statement,
  changeStatement,
  index,
  addStatement,
}) => {
  // Define the state with TypeScript type
  const [selectedAttr, setSelectedAttr] = useState<string>("select attribute");
  const [selectedLvl, setSelectedLvl] = useState<string>("select level");
  const [sign, setSign] = useState<string>(statement.equals);
  const [proposition, setProposition] = useState<string>(statement.part);

  const { attributes } = useAttributes();

  useEffect(() => {
    setSelectedLvl("select level");
  }, [selectedAttr]);

  useEffect(() => {
    if (changeStatement) {
      changeStatement(index, {
        attribute: selectedAttr,
        level: selectedLvl,
        equals: sign,
        part: proposition,
      });
    }
  }, [selectedAttr, selectedLvl, sign, proposition]);


  const getAttributeLevels = (attributeName: string) => {
    const index = attributes.findIndex((attr) => attr.name == attributeName);
    return attributes[index] ? attributes[index].levels : [];
  };
  return (
    <div className={styles.statement_container}>
      <div className={styles.statement}>
        {statement.part == "if" || statement.part == "then" ? (
          <p className={styles.part}>{statement.part.toUpperCase()}</p>
        ) : (
          <CustomDropdown
            value={proposition}
            type="small"
            sign={true}
            items={["&", "OR"]}
            setSelected={setProposition}
          />
        )}
        <CustomDropdown
          value={selectedAttr}
          items={attributes.map((attr) => attr.name)}
          setSelected={setSelectedAttr}
          color={selectedAttr == "select attribute" ? true : false}
        />
        {/* FOR NOW THIS */}
        {sign}
        {/* <CustomDropdown
          sign={true}
          value={sign}
          items={["=", "!="]}
          setSelected={setSign}
        /> */}
        <CustomDropdown
          value={selectedLvl}
          items={
            selectedAttr
              ? getAttributeLevels(selectedAttr).map((level) => level.name)
              : []
          }
          setSelected={setSelectedLvl}
          color={selectedLvl == "select level" ? true : false}
        />
        {addStatement ? <Button text="+" onClick={addStatement} /> : ""}
      </div>
    </div>
  );
};
