import React, { useState, useRef, useEffect, useContext } from "react";
import styles from "./export.module.css"; // Import your styles here
import { downloadSurvey } from "@/services/api";
import { useAttributes } from "@/context/attributes_context";
import { Button } from "@/components/ui/button";
import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import { CodeFileIcon, ExportIcon, XIcon } from "@/components/ui/icons";
import { DocumentContext } from "@/context/document_context";
import { ExportFormat } from "./__format/export__format";
import { SettingsNumberRange } from "../settings/__number-range/settings__number-range";

interface IExportDropdown {
  size: "big" | "small";
}

export interface IFormat {
  name: string;
  path: "create_qualtrics" | "export_js" | "export_csv" | "export_json";
  description: string;
  clickable: boolean;
}

const formats: IFormat[] = [
  {
    name: "Qualtrics",
    path: "create_qualtrics",
    clickable: false,
    description: "Export your survey to Qualtrics",
  },
  {
    name: "CSV",
    path: "export_csv",
    clickable: true,
    description: "Export your survey to a CSV file",
  },
  {
    name: "JS",
    path: "export_js",
    clickable: true,
    description: "Export your survey to a JavaScript file",
  },
  {
    name: "JSON",
    path: "export_json",
    clickable: true,
    description:
      "Export your survey to a JSON file that you can import in your own app",
  },
];

const ExportDropdown: React.FC<IExportDropdown> = ({ size }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeItem, setActiveItem] = useState<IFormat>(formats[1]);
  const { currentDoc } = useContext(DocumentContext);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const { attributes } = useAttributes();
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [docName, setDocName] = useState<string>(currentDoc);
  const inputRef = useRef<HTMLInputElement>(null);
  const [numRows, setNumRows] = useState<number>(500);

  const toggleOpen = () => setIsOpen(!isOpen);

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node)
    ) {
      setIsOpen(false);
    }
  };

  const handleItemClick = (item: IFormat) => setActiveItem(item);

  const handleDownload = async (path: IFormat["path"]) => {
    setIsLoading(true);
    await downloadSurvey(attributes, path, docName, numRows);
    setIsLoading(false);
  };

  const handleBlur = () => {
    if (docName.trim() === "") {
      setDocName("Untitled");
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDocName(e.target.value);
  };

  const handleNumRowsChange = (value: number) => {
    setNumRows(value);
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  useEffect(() => {
    setDocName(currentDoc);
  }, [currentDoc]);

  return (
    <>
      {size === "big" ? (
        <div className={styles.modalBefore} onClick={toggleOpen}>
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
          <div className={styles.modalContent}>
            <label>
              <p>File name</p>
            </label>
            <input
              ref={inputRef}
              value={docName}
              onChange={handleInputChange}
              onBlur={handleBlur}
              className={styles.editableInput}
              // additional styling or attributes
            />
            <p>Choose the format </p>
            <ExportFormat
              formats={formats}
              activeItem={activeItem}
              handleItemClick={handleItemClick}
            />
            {activeItem.name === "CSV" && (
              <>
                <SettingsNumberRange
                  value={numRows}
                  onChange={handleNumRowsChange}
                  min={1}
                  max={100000}
                  label="How many rows?"
                  explanation="Set the amount of rows to export in the CSV"
                />
              </>
            )}
            <div className={styles.modalButtonContainer}>
              <button
                onClick={() => handleDownload(activeItem.path)}
                className={styles.modalButton}
              >
                Export
              </button>
            </div>
          </div>
        </Box>
      </Modal>
    </>
  );
};

export default ExportDropdown;

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
