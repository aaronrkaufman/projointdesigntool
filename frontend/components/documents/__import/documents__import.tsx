import React, { FC, useState, useRef, useEffect, useContext } from "react";
import { importDocument } from "@/services/api";
import { useRouter } from "next/router";
import { v4 as uuidv4 } from "uuid";
import { Button } from "@/components/ui/button";
import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import { XIcon } from "@/components/ui/icons";

import styles from "./documents__import.module.css";
import { LinearProgress, TextField } from "@mui/material";
import { ImportIcon } from "@/components/ui/file-add";
import { useAttributes } from "@/context/attributes_context";

export interface DocumentsImportProps {
  size: "big" | "small";
}

export const DocumentsImport: FC<DocumentsImportProps> = ({ size }) => {
  const [isOpen, setIsOpen] = useState(false);

  const dropdownRef = useRef<HTMLDivElement>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const { setStorageChanged } = useAttributes();

  const toggleOpen = () => setIsOpen(!isOpen);

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node)
    ) {
      setIsOpen(false);
    }
  };

  const handleImport = async (event: React.FormEvent<HTMLFormElement>) => {
    setIsLoading(true);
    event.preventDefault();
    const target = event.target as HTMLFormElement;
    const fileInput = target.querySelector(
      'input[type="file"]'
    ) as HTMLInputElement;

    const file = fileInput.files?.[0];

    if (!file) {
      setIsLoading(false);
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    const response = await importDocument(formData, (progress: number) => {
      setUploadProgress(progress);
    });
    handleAddDoc(response);
    setIsOpen(false);

    setIsLoading(false);
  };

  const router = useRouter();

  const handleAddDoc = (value: any) => {
    const uniqueId = uuidv4();
    const dataToSave = {
      attributes: value.attributes,
      lastEdited: new Date(), // Update last edited time
      name: "Untitled",
      instructions: {
        description: "",
        instructions: "",
        outcomeType: "mcq",
      },
      restrictions: [],
      settings: {
        numProfiles: value.profiles,
        numTasks: value.tasks,
        repeatedTasks: value.repeat_task,
        repeatedTasksFlipped: value.noFlip,
        taskToRepeat: value.duplicate_first,
        whereToRepeat: value.duplicate_second,
        randomize: value.randomize,
        noFlip: value.noFlip,
      },
    };
    localStorage.setItem(`attributes-${uniqueId}`, JSON.stringify(dataToSave));
    setStorageChanged((prev) => prev + 1);
    router.push(`/${encodeURIComponent(uniqueId)}`);
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <>
      {size === "big" ? (
        <div className={styles.modalBefore} onClick={toggleOpen}>
          <ImportIcon /> <p>Import from JSON</p>{" "}
        </div>
      ) : (
        <Button
          text="Import from JSON"
          icon={<ImportIcon />}
          onClick={toggleOpen}
        ></Button>
      )}
      <Modal
        open={isOpen}
        onClose={() => setIsOpen(false)}
        aria-labelledby="import-modal-title"
        aria-describedby="import-modal-description"
      >
        <Box sx={modalStyle}>
          <div className={styles.modalHeader}>
            <h2 id="import-modal-title">Import a JSON file</h2>
            <XIcon onClick={() => setIsOpen(false)} />
          </div>
          <div className={styles.modalContent}>
            <form onSubmit={handleImport}>
              <TextField type="file" />
              <LinearProgress variant="determinate" value={uploadProgress} />
              <div className={styles.modalButtonContainer}>
                <button type="submit" className={styles.modalButton}>
                  Import
                </button>
              </div>
            </form>
          </div>
        </Box>
      </Modal>
    </>
  );
};

const modalStyle = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 450,
  bgcolor: "var(--light-blue)",
  borderRadius: "1rem",
  // p: 2,
};
