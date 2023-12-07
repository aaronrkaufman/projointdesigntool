import React, { useState, useRef, useEffect } from "react";
import styles from "../restrictions//dropdown.module.css"; // Import your styles here
import { downloadSurvey } from "../../services/api";
import { useAttributes } from "../../context/attributes_context";
import { Button } from "../button";

// interface IDropdown {
//   items: string[];
//   setSelected: (item: string) => void;
// }

const ExportDropdown: React.FC = () => {
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
    path: "qualtrics" | "export" | "preview_csv"
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
    <div className={styles.dropdown} ref={dropdownRef}>
      <button className={styles.dropdownButton} onClick={toggleOpen}>
        Export
      </button>
      {isOpen && (
        <ul className={`${styles.dropdownContent} ${styles.active}`}>
          <li onClick={() => handleDownload("qualtrics")}>
            Export to Qualtrics
          </li>
          <li onClick={() => handleDownload("export")}>Export to JS</li>
          <li onClick={() => handleDownload("preview_csv")}>Export to CSV</li>
        </ul>
      )}
    </div>
  );
};

export default ExportDropdown;
