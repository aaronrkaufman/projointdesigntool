import { useState } from "react";
import { Button } from "../ui/button";
import styles from "./restrictions.module.css";
import { Statement } from "./statement";
import { useAttributes } from "../../context/attributes_context";
import { AddedRestriction } from "./added_restriction";
import { PlusIcon } from "../ui/icons";

export interface StatementProps {
  part: "if" | "then" | "&" | "OR";
  attribute: string;
  level: string;
  equals: "=" | "!=";
}

export const Restrictions = () => {
  const [ifStatements, setIfStatements] = useState<StatementProps[]>([
    {
      part: "if",
      attribute: "select attribute",
      level: "select level",
      equals: "=",
    },
  ]);
  const [elseStatements, setElseStatements] = useState<StatementProps[]>([
    {
      part: "then",
      attribute: "select attribute",
      level: "select level",
      equals: "!=",
    },
  ]);

  const addIfStatement = () => {
    setIfStatements((prev) => [
      ...prev,
      {
        part: "&",
        attribute: "select attribute",
        level: "select level",
        equals: "!=",
      },
    ]);
  };

  const addElseStatement = () => {
    setElseStatements((prev) => [
      ...prev,
      {
        part: "&",
        attribute: "select attribute",
        level: "select level",
        equals: "!=",
      },
    ]);
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

  const createRestrictionString = () => {
    // Helper function to format a single statement
    const formatStatement = ({ attribute, level, equals }: any) => {
      const operator = equals === "=" ? "equals" : "does not equal";
      return `${attribute} ${operator} ${level}`;
    };

    const formatAgain = ({ attribute, level, equals }: any) => {
      return [attribute, equals, level];
    };

    // Process the 'if' statements
    // const ifPart = ifStatements.map(formatStatement).join(" or ");
    const ifPart = ifStatements.map(formatAgain);
    const thenPart = elseStatements.map(formatAgain);
    // // Process the 'then' statements
    // const thenPart = elseStatements.map(formatStatement).join(" or ");

    // Combine both parts
    // return `if ${ifPart}, then ${thenPart}`;
    return [...ifPart, ...thenPart];
  };

  const handleAddRestriction = () => {
    // const statements = [ifStatements, elseStatements];
    // console.log(statements);
    const newRestriction: string[][] = createRestrictionString();
    console.log(newRestriction);
    addRestrictionToAttribute(newRestriction);
  };

  const { restrictions, addRestrictionToAttribute } = useAttributes();

  return (
    <section className={styles.section}>
      <div className={styles.sectionContainer}>
        <div className={styles.top}>
          <h2>Restrictions</h2>
        </div>
        <p>List of attribute-level pairs that can’t be together in a profile</p>
        <div className={styles.container}>
          <div className={styles.left}>
            <ul className={styles.restrictions}>
              {restrictions &&
                restrictions.map((restr, index) => (
                  <AddedRestriction
                    restriction={restr}
                    index={index}
                    key={restr[0][index]}
                  />
                ))}
            </ul>
          </div>
          <div className={styles.right}>
            <p>Enter New Restriction Statement</p>
            <div className={styles.statements}>
              <Statement
                statement={ifStatements[0]}
                index={0}
                changeStatement={changeIfStatement}
                addStatement={addIfStatement}
              />
              {ifStatements.map((item, index) => {
                if (index === 0) return "";
                return (
                  <Statement
                    key={index}
                    statement={item}
                    index={index}
                    changeStatement={changeIfStatement}
                  />
                );
              })}
              <Statement
                statement={elseStatements[0]}
                index={0}
                changeStatement={changeElseStatement}
                addStatement={addElseStatement}
              />
              {elseStatements.map((item, index) => {
                if (index === 0) return "";
                return (
                  <Statement
                    changeStatement={changeElseStatement}
                    key={index}
                    statement={item}
                    index={index}
                  />
                );
              })}
            </div>
            <div>
              <Button
                icon={<PlusIcon stroke="white" />}
                text="Add a restriction statement"
                disabled={isRestrictionDone()}
                onClick={handleAddRestriction}
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
