import styles from "./survey.module.css"

export const AddAttribute = () => {
    return <div className={styles.container}>
        <span className={styles.line}></span>
        <button className={styles.btn}>Add Attribute</button>
    </div>
}