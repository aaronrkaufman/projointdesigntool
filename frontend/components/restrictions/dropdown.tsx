import React, { useState, useRef, useEffect } from "react";
import styles from "./dropdown.module.css"; // Import your styles here

interface IDropdown {
  items: string[];
  value: string;
  setSelected: (item: string) => void;

  sign?: boolean;
}

const CustomDropdown: React.FC<IDropdown> = ({
  items,
  setSelected,

  sign,
  value,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  //   const [selectedValue, setSelectedValue] = useState<string | number>(text);
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
    setSelected(value);
    setIsOpen(false);
  };

  return (
    <div className={styles.dropdown} ref={dropdownRef}>
      <button
        className={`${styles.dropdownButton} ${sign && styles.smaller}`}
        onClick={toggleOpen}
      >
        {value}
      </button>
      {isOpen && (
        <ul className={`${styles.dropdownContent} ${styles.active}`}>
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
