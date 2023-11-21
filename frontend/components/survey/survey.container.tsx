"use client";
import React, { FC, useEffect } from "react";
import { Survey } from "./survey";
import { useState } from "react";
import { IAttribute } from "../attribute/attribute.container";
import { HighlightedProvider } from "../../context/highlighted";
import AttributeProvider, {
  useAttributes,
} from "../../context/attributes_context";
import { DragDropContext } from "react-beautiful-dnd";

const reorder = (
  list: IAttribute[],
  startIndex: number,
  endIndex: number
): IAttribute[] => {
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);
  return result;
};

export const SurveyContainer: FC = () => {
  const { attributes, setAttributes } = useAttributes();

  const onDragEnd = (result: any) => {
    const { source, destination, type } = result;
    // Dropped outside the list
    if (!destination || source.droppableId !== destination.droppableId) {
      return;
    }

    // If the source and destination droppables are the same

    if (source.droppableId.startsWith("droppable-attributes")) {
      const reorderedItems = reorder(
        attributes,
        result.source.index,
        result.destination.index
      );
      setAttributes(reorderedItems);
    } else {
      const newAttributes = [...attributes];
      // Find the attribute by droppableId, which should match the attribute's key
      const attributeIndex = newAttributes.findIndex(
        (attr) => `droppable-levels-${attr.key}` === source.droppableId
      );
      if (attributeIndex !== -1) {
        // Reorder levels within the attribute
        const [movedLevel] = newAttributes[attributeIndex].levels.splice(
          source.index,
          1
        );
        newAttributes[attributeIndex].levels.splice(
          destination.index,
          0,
          movedLevel
        );
      }

      // Update the state with the new attributes array

      setAttributes(newAttributes);
    }
  };

  // const [attributes, setAttributes] = useState<IAttribute[]>([
  //   {
  //     name: "Age",
  //     levels: [{ name: "10-20" }, { name: "20-30" }, { name: "30-40" }],
  //     key: 0,
  //     weights: [0.33, 0.33, 0.33],
  //   },
  //   {
  //     name: "Education",
  //     levels: [
  //       { name: "No Formal" },
  //       { name: "4th Grade" },
  //       { name: "8th Grade" },
  //       { name: "High School" },
  //       { name: "Two-Year College" },
  //     ],
  //     key: 1,
  //     weights: [0.2, 0.2, 0.2, 0.2, 0.2],
  //   },
  // ]);

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <HighlightedProvider>
        <Survey />
      </HighlightedProvider>
    </DragDropContext>
  );
};
