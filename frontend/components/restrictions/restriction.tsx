import { useEffect, useState } from "react";
import { DeleteTip, PlusIcon } from "../ui/icons";
import { StatementProps } from "./restrictions";
import { Statement } from "./statement";
import { v4 as uuidv4 } from "uuid";
import styles from "./restrictions.module.css";
import { useAttributes } from "../../context/attributes_context";
import naming from "@/naming/english.json";

export interface RestrictionProps {
  ifStates: StatementProps[];
  elseStates: StatementProps[];
  id: string;
}

export const Restriction: React.FC<
  RestrictionProps & {
    saveRestriction: (restriction: RestrictionProps) => void;
    handleUpdate: (change: boolean) => void;
    handleRestrictions: (id: string) => void;
  }
> = ({
  ifStates,
  elseStates,
  id,
  saveRestriction,
  handleUpdate,
  handleRestrictions,
}) => {
  const [ifStatements, setIfStatements] = useState<StatementProps[]>(ifStates);
  const [elseStatements, setElseStatements] =
    useState<StatementProps[]>(elseStates);

  const addIfStatement = () => {
    setIfStatements((prev) => [
      ...prev,
      {
        part: "and",
        attribute: "select attribute",
        level: "select level",
        equals: false,
        id: uuidv4(),
      },
    ]);
  };

  const deleteIfStatement = (attributeIndex: number) => {
    setIfStatements((prev) =>
      prev.filter((_, index) => index !== attributeIndex)
    );
  };

  const addElseStatement = () => {
    setElseStatements((prev) => [
      ...prev,
      {
        part: "and",
        attribute: "select attribute",
        level: "select level",
        equals: true,
        id: uuidv4(),
      },
    ]);
  };

  const deleteElseStatement = (attributeIndex: number) => {
    setElseStatements((prev) =>
      prev.filter((_, index) => index !== attributeIndex)
    );
  };

  const changeIfStatement = (
    index: number,
    { attribute, level, equals, part }: Partial<StatementProps>
  ) => {
    setIfStatements((prev) =>
      prev.map((st, ind) => {
        if (ind === index) {
          return {
            ...st,
            attribute: attribute ?? st.attribute,
            level: level ?? st.level,
            equals: equals ?? st.equals,
            part: part ?? st.part,
          };
        }
        return st;
      })
    );
  };

  const changeElseStatement = (
    index: number,
    { attribute, level, equals, part }: Partial<StatementProps>
  ) => {
    setElseStatements((prev) =>
      prev.map((st, ind) => {
        if (ind === index) {
          return {
            ...st,
            attribute: attribute ?? st.attribute,
            level: level ?? st.level,
            equals: equals ?? st.equals,
            part: part ?? st.part,
          };
        }
        return st;
      })
    );
  };

  const isRestrictionDone = () => {
    const notDone = ({ attribute, level }: any) => {
      return attribute == "select attribute" || level == "select level";
    };
    return ifStatements.some(notDone) || elseStatements.some(notDone);
  };

  useEffect(() => {
    handleUpdate(!isRestrictionDone());
    if (!isRestrictionDone()) {
      saveRestriction({
        ifStates: ifStatements,
        elseStates: elseStatements,
        id,
      });
    }
  }, [ifStatements, elseStatements]);

  const { deleteRestriction } = useAttributes();

  const handleDeleteRestriction = () => {
    if (!isRestrictionDone()) {
      handleRestrictions(id);
      deleteRestriction(id);
    } else {
      handleRestrictions(id);
      handleUpdate(true);
    }
  };

  return (
    <div className={styles.restrictionContainer}>
      <div className={styles.statements}>
        <div className={styles.ifStatements}>
          <Statement
            statement={ifStatements[0]}
            index={0}
            changeStatement={changeIfStatement}
          />
          {ifStatements.map((item, index) => {
            if (index === 0) return "";
            return (
              <Statement
                key={item.id}
                statement={item}
                index={index}
                changeStatement={changeIfStatement}
                deleteStatement={deleteIfStatement}
              />
            );
          })}
          <div className={styles.addCondition} onClick={addIfStatement}>
            <PlusIcon stroke={`var(--blue)`} />{" "}
            {naming.restrictionsPage.addCondition.value}
          </div>
        </div>
        <div className={styles.elseStatements}>
          <Statement
            statement={elseStatements[0]}
            index={0}
            changeStatement={changeElseStatement}
          />
          {elseStatements.map((item, index) => {
            if (index === 0) return "";
            return (
              <Statement
                changeStatement={changeElseStatement}
                key={index}
                statement={item}
                index={index}
                deleteStatement={deleteElseStatement}
              />
            );
          })}
          {/* <div className={styles.addCondition} onClick={addElseStatement}>
            <PlusIcon stroke={`var(--blue)`} /> Add condition
          </div> */}
        </div>
      </div>
      <div className={styles.svg} onClick={handleDeleteRestriction}>
        <DeleteTip />
      </div>
    </div>
  );
};
