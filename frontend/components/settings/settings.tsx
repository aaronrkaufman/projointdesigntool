import { useContext, useState, useRef, useEffect } from "react";
import styles from "./settings.module.css";
import { DocumentContext } from "../../context/document_context";
import { useAttributes } from "../../context/attributes_context";
import { SettingsCheckbox } from "./__checkbox/settings__checkbox";
import { SettingsRadioGroup } from "./__radio-group/settings__radio-group";
import { SettingsExplanation } from "./__explanation/settings__explanation";
import { SettingsLine } from "./__line/settings__line";
import { SettingsNumberRange } from "./__number-range/settings__number-range";

export const Settings = () => {
  const { currentDoc, lastEdited, setLastEdited, setCurrentDoc } =
    useContext(DocumentContext);

  const { setEdited } = useAttributes();

  const [repeatedTasks, setRepeatedTasks] = useState(true);
  const [repeatedTasksFlipped, setRepeatedTasksFlipped] = useState(false);

  const [numProfiles, setNumProfiles] = useState(2);
  const [numTasks, setNumTasks] = useState(2);

  const [isEditing, setIsEditing] = useState(false);
  const [docName, setDocName] = useState<string>(currentDoc);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (docName !== currentDoc) {
      setDocName(currentDoc);
    }
  }, [currentDoc]);

  useEffect(() => {
    if (isEditing) {
      inputRef.current?.focus();
    }
  }, [isEditing]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDocName(e.target.value);
  };

  const handleBlur = () => {
    setIsEditing(false);
    setLastEdited(new Date());
    setEdited(true);
    // Here you can call a function to save the docName
    // saveDocName(docName);
    setCurrentDoc(docName);
  };
  return (
    <section className={styles.section}>
      <div className={styles.sectionContainer}>
        <div className={styles.top}>
          <h2>Settings</h2>
        </div>
        <div className={styles.name}>
          <label>
            <h3>Name</h3>
          </label>
          <input
            ref={inputRef}
            value={docName}
            onChange={handleInputChange}
            onBlur={handleBlur}
            className={styles.editableInput}
            // additional styling or attributes
          />
          <SettingsExplanation
            explanation={<p>You can use any name you want. Keep it simple.</p>}
          />
        </div>
        <SettingsLine />
        <SettingsNumberRange
          value={numProfiles}
          onChange={(newValue) => setNumProfiles(newValue)}
          min={1}
          max={10}
          label="Number of profiles"
          explanation="Changes the number of profiles in preview section"
        />
        <SettingsNumberRange
          value={numTasks}
          onChange={(newValue) => setNumTasks(newValue)}
          min={1}
          max={10}
          label="Number of tasks"
          explanation="Set of choices presented to the respondent in a single screen (i.e. pair of candidates)"
        />
        <SettingsLine />
        <SettingsCheckbox
          checked={repeatedTasks}
          onChange={(e) => setRepeatedTasks(e.target.checked)}
          label="Repeated tasks"
          explanation="Option to repeat tasks"
        />
        {repeatedTasks && (
          <SettingsCheckbox
            checked={repeatedTasksFlipped}
            onChange={(e) => setRepeatedTasksFlipped(e.target.checked)}
            label="Flipped"
            explanation="Option to either flip columns same for repeated tasks"
          />
        )}
        <SettingsLine />
        <div className={styles.ordering}>
          <h3>Ordering of attributes</h3>

          <SettingsRadioGroup
            options={[
              "Non random",
              "Participant randomized",
              "Task randomized",
            ]}
            defaultValue="Non random"
          />
          <SettingsExplanation
            learnMoreLink
            explanation={<p>Learn about attribute ordering.</p>}
          />
          {/* This setting determines the order in which the attributes are presented to the user. The default is non-random, which means the attributes are presented in the order they are defined in the document. The other options randomize the order in different ways. */}
        </div>
        <SettingsLine />
      </div>
    </section>
  );
};
