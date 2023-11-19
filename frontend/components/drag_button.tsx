import React from "react";
import styles from "./drag_button.module.css";
interface DragButtonProps {
  direction: "vertical" | "horizontal";
  //   visible: boolean;
  // ... include other props you might need, such as styling props
}

const DragButton: React.FC<
  DragButtonProps & React.HTMLAttributes<HTMLDivElement>
> = ({ direction, ...props }) => {
  return (
    <div {...props} className={styles.drag + " dragHandle"}>
      {/* You can add an icon or any visual element to represent the drag handle here */}
      {direction === "vertical" ? (
        // Icons or styles specific to vertical direction
        <span>:::</span>
      ) : (
        // Icons or styles specific to horizontal direction
        <span>⋮⋮</span>
      )}
      {/* <span className={styles.tooltiptext}>Drag to move</span> */}
    </div>
  );
};

export default DragButton;
