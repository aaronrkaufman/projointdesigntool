import { useEffect, useState } from "react";
import { Button } from "../ui/button";
import styles from "./restrictions.module.css";
import { useAttributes } from "../../context/attributes_context";
import { PlusIcon } from "../ui/icons";
import { Restriction, RestrictionProps } from "./restriction";
import { v4 as uuidv4 } from "uuid";

export interface StatementProps {
  part: "if" | "then" | "and" | "or";
  attribute: string;
  level: string;
  equals: boolean;
  id: string;
}

export const Restrictions = () => {
  const { restrictions, saveRestriction } = useAttributes();

  const isRestrictionDone = (restriction: RestrictionProps) => {
    const notDone = ({ attribute, level }: any) => {
      return attribute == "select attribute" || level == "select level";
    };
    return (
      restriction.ifStates.some(notDone) || restriction.elseStates.some(notDone)
    );
  };

  const [newRestrictions, setNewRestrictions] = useState<RestrictionProps[]>(
    restrictions ? restrictions : []
  );

  const handleUpdate = (change: boolean) => {
    setCanAddNewRestriction(change);
  };

  const [canAddNewRestriction, setCanAddNewRestriction] =
    useState<boolean>(true);

  useEffect(() => {
    setNewRestrictions(restrictions ? restrictions : []);
  }, [restrictions]);

  const handleSave = (restriction: RestrictionProps) => {
    saveRestriction(restriction);
  };

  const handleAddRestriction = () => {
    if (canAddNewRestriction) {
      setNewRestrictions((prev) => [
        ...prev,
        {
          ifStates: [
            {
              part: "if",
              attribute: "select attribute",
              level: "select level",
              equals: true,
              id: uuidv4(),
            },
          ],
          elseStates: [
            {
              part: "then",
              attribute: "select attribute",
              level: "select level",
              equals: false,
              id: uuidv4(),
            },
          ],
          id: uuidv4(),
        },
      ]);
    }
  };

  const handleRestrictions = (id: string) => {
    setNewRestrictions((prev) => prev.filter((r) => r.id !== id));
  };

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
              {newRestrictions &&
                newRestrictions.map((restr, index) => (
                  <Restriction
                    key={restr.id}
                    {...restr}
                    handleUpdate={handleUpdate}
                    saveRestriction={handleSave}
                    handleRestrictions={handleRestrictions}
                  />
                ))}
            </ul>
          </div>
          <div className={styles.right}>
            <div>
              <Button
                icon={<PlusIcon stroke="white" />}
                text="Add a restriction statement"
                disabled={!canAddNewRestriction}
                onClick={handleAddRestriction}
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
