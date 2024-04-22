import { useRouter } from "next/router";
import { useAttributes } from "../../../context/attributes_context";
import { FileIcon, LightTooltip, ThreeDots } from "../../ui/icons";
import styles from "../documents.module.css";
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

  const { setStorageChanged } = useAttributes();
  const router = useRouter();

  const isPath = (path: string) => {
    return router.asPath.includes(path);
  };

  const handleDelete = () => {
    localStorage.removeItem(`attributes-${id}`);
    setStorageChanged((prev) => prev + 1);
    router.push(`/document}`);
  };
  return (
    <li>
      <Link href={`/${encodedName}`}>
        <div className={`${active ? styles.active : ""} ${styles.container}`}>
          <div className={styles.file_top}>
            <div className={styles.file}>
              <FileIcon
                stroke={`${active ? "var(--dark-blue-h)" : "var(--blue-p)"}`}
              />
              <p>{name}</p>
            </div>
            <div className={`${active ? "" : styles.noshow} ${styles.dots}`}>
              <LightTooltip
                disableInteractive
                title="More"
                arrow
                placement="top"
              >
                <ThreeDots onDelete={handleDelete} />
              </LightTooltip>
            </div>
          </div>
          {active && (
            <ul className={styles.helpers}>
              <Link href={`/${encodedName}/preview`}>
                <p className={isPath("/preview") ? styles.activeLink : ""}>
                  Preview
                </p>
              </Link>
              <Link href={`/${encodedName}/settings`}>
                <p className={isPath("/settings") ? styles.activeLink : ""}>
                  Settings
                </p>
              </Link>
              <Link href={`/${encodedName}/restrictions`}>
                <p className={isPath("/restrictions") ? styles.activeLink : ""}>
                  Restrictions
                </p>
              </Link>
            </ul>
          )}
        </div>
      </Link>
    </li>
  );
};
