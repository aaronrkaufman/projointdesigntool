"use client";

import { useContext, useEffect, useState } from "react";
import { Documents } from "../documents/documents";
import styles from "./sidebar.module.css";
import { IDocument } from "../documents/__item/documents__item";
import { useRouter } from "next/router";
import { v4 as uuidv4 } from "uuid";
import { useAttributes } from "../../context/attributes_context";
import { FileAdd, LightTooltip } from "../ui/icons";
import { SidebarFolder } from "./__folder/sidebar__folder";
import { getTutorials } from "@/services/api";
import { SidebarTutorials } from "./__tutorials/sidebar__tutorials";

export const Sidebar = ({ active }: { active: string }) => {
  const [documents, setDocuments] = useState<IDocument[]>([]);
  const { storageChanged, setStorageChanged } = useAttributes();
  const [tutorials, setTutorials] = useState([]);

  useEffect(() => {
    const fetchTutorials = async () => {
      const tutorialData = await getTutorials();
      setTutorials(tutorialData);
    };

    fetchTutorials();
  }, []);

  useEffect(() => {
    // Function to load documents from localStorage
    const loadDocuments = (): IDocument[] => {
      const docs: IDocument[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith("attributes-")) {
          const item = localStorage.getItem(key);
          if (item) {
            const data = JSON.parse(item);
            docs.push({
              name: data.name,
              key: key.substring(11), // assuming the key is in the format 'attributes-uniqueid'
            });
          }
        }
      }
      return docs;
    };

    setDocuments(loadDocuments());
  }, [storageChanged]);

  const router = useRouter();

  const handleAddDoc = () => {
    const uniqueId = uuidv4();
    const dataToSave = {
      attributes: [],
      lastEdited: new Date(), // Update last edited time
      name: "Untitled",
      instructions: {
        description: "",
        instructions: "",
        outcomeType: "mcq",
      },
      restrictions: [],
      settings: {
        numProfiles: 2,
        numTasks: 2,
        repeatedTasks: true,
        repeatedTasksFlipped: false,
        taskToRepeat: 1,
        whereToRepeat: 1,
        randomize: false,
        noFlip: false,
      },
    };
    localStorage.setItem(`attributes-${uniqueId}`, JSON.stringify(dataToSave));
    setStorageChanged((prev) => prev + 1);
    router.push(`/${encodeURIComponent(uniqueId)}`);
  };

  const handleHome = () => {
    router.push("/");
  };

  return (
    <div className={styles.sidebar}>
      <div className={styles.top}>
        <h3 onClick={handleHome}>Projoint</h3>
        <div className={styles.addDoc} onClick={handleAddDoc}>
          <LightTooltip
            disableInteractive
            title="New survey"
            arrow
            placement="right"
          >
            <FileAdd />
          </LightTooltip>
        </div>
      </div>
      <span className={styles.line}></span>
      <SidebarFolder
        name="My surveys"
        active={!active.includes("tutorial") && !active.includes("index")}
        element={<Documents documents={documents} active={active} />}
      />
      <SidebarFolder
        active={active.includes("tutorial")}
        name="Tutorials"
        element={<SidebarTutorials tutorials={tutorials} active={active} />}
      />
    </div>
  );
};
