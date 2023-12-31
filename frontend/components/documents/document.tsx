import styles from "./documents.module.css";
import Link from "next/link";
export interface IDocument {
  name: string;
  key: number | string;
}

interface IDoc extends IDocument {
  active: boolean;
  id: string;
}

export const Document = ({ name, active, id }: IDoc) => {
  const encodedName = encodeURIComponent(id);

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
              <li>Settings</li>{" "}
              <Link href={`/documents/${encodedName}/restrictions`}>
                <p>Restrictions</p>
              </Link>{" "}
            </ul>
          )}
        </div>
      </Link>
    </li>
  );
};
