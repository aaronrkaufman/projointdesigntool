import React, { useState, useRef, useEffect } from "react";
import styles from "./survey.module.css"; // Import your styles here
import { downloadSurvey } from "../../services/api";
import { useAttributes } from "../../context/attributes_context";
import { Button } from "../ui/button";
import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import { CodeFileIcon, ExportIcon, XIcon } from "../ui/icons";

// interface IDropdown {
//   items: string[];
//   setSelected: (item: string) => void;
// }

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

interface IExportDropdown {
  size: "big" | "small";
}

const ExportDropdown: React.FC<IExportDropdown> = ({ size }) => {
  const [isOpen, setIsOpen] = useState(false);

  const dropdownRef = useRef<HTMLDivElement>(null);

  const toggleOpen = () => setIsOpen(!isOpen);

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node)
    ) {
      setIsOpen(false);
    }
  };

  // Handle download of a file through export
  const [isLoading, setisLoading] = useState<boolean>(false);
  const { attributes } = useAttributes();

  const handleDownload = async (
    path: "qualtrics" | "export" | "export_csv"
  ) => {
    setisLoading(true);
    await downloadSurvey(attributes, path);
    setisLoading(false);
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <>
      {size === "big" ? (
        <div
          style={{
            width: "100%",
            display: "flex",
            alignItems: "center",
            gap: "0.75rem",
          }}
          onClick={toggleOpen}
        >
          <ExportIcon /> <p>Export</p>{" "}
        </div>
      ) : (
        <Button
          text="Export"
          icon={<ExportIcon stroke="white" />}
          onClick={toggleOpen}
        ></Button>
      )}
      <Modal
        open={isOpen}
        onClose={() => setIsOpen(false)}
        aria-labelledby="export-modal-title"
        aria-describedby="export-modal-description"
      >
        <Box sx={modalStyle}>
          <div className={styles.modalHeader}>
            <h2 id="export-modal-title">Export this survey</h2>
            <XIcon onClick={() => setIsOpen(false)} />
          </div>
          <ul className={styles.modalList}>
            <li>
              <div className={styles.modalListItem}>
                <CodeFileIcon stroke="var(--blue)" />
                <p> Export to Qualtrics</p>
              </div>
              <button
                onClick={() => handleDownload("qualtrics")}
                className={styles.modalListItemButton}
              >
                Export
              </button>
            </li>
            <li>
              <div className={styles.modalListItem}>
                <CodeFileIcon stroke="var(--blue)" />
                <p>Export to JS</p>
              </div>
              <button
                onClick={() => handleDownload("export")}
                className={styles.modalListItemButton}
              >
                Export
              </button>
            </li>
            <li>
              <div className={styles.modalListItem}>
                <CodeFileIcon stroke="var(--blue)" />
                <p>Export to CSV</p>
              </div>
              <button
                onClick={() => handleDownload("export_csv")}
                className={styles.modalListItemButton}
              >
                Export
              </button>
            </li>
          </ul>
        </Box>
      </Modal>
    </>
  );
};

export default ExportDropdown;
