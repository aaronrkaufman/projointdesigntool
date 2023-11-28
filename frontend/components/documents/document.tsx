import styles from "./documents.module.css";
import Link from "next/link";
export interface IDocument {
  name: string;
  key: number;
}

interface IDoc extends IDocument {
  active: boolean;
}

export const Document = ({ name, active }: IDoc) => {
  const encodedName = encodeURIComponent(name);

  return (
    <li>
      <Link href={`/documents/${encodedName}`}>
        <div className={`${active ? styles.active : ""} ${styles.container}`}>
          <p>{name}</p>
          {active && (
            <ul className={styles.helpers}>
              <Link href={`/documents/${encodedName}/preview`}>
                <p>Preview</p>
              </Link>{" "}
              <li>Settings</li> <li>Restrictions</li>
            </ul>
          )}
        </div>
      </Link>
    </li>
  );
};
