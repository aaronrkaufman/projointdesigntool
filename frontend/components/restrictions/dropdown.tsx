import React, { useState, useRef, useEffect } from "react";
import styles from "./dropdown.module.css"; // Import your styles here

interface IDropdown {
  items: string[];
  setSelected: (item: string) => void;
}

const CustomDropdown: React.FC<IDropdown> = ({ items, setSelected }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState<string | number>(
    "select attributes"
  );
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

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const selectOption = (value: string) => {
    setSelectedValue(value);
    setSelected(value);
    setIsOpen(false);
  };

  return (
    <div className={styles.dropdown} ref={dropdownRef}>
      <button className={styles.dropdownButton} onClick={toggleOpen}>
        {selectedValue}
      </button>
      {isOpen && (
        <ul className={styles.dropdownContent}>
          {items.map((number) => (
            <li
              key={number}
              onClick={() => selectOption(number)}
              className={styles.dropdownItem}
            >
              {number}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CustomDropdown;
