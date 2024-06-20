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
import { addSurvey } from "@/components/utils/add-survey";

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

  const router = useRouter();

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
    addSurvey({ router, value: response, onStorageChange: setStorageChanged });
    setIsLoading(false);
    setIsOpen(false);
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
          icon={<ImportIcon stroke="var(--white)" />}
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
