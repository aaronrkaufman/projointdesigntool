"use client";
import React, { FC, useEffect } from "react";
import { Survey } from "./survey";
import { useState } from "react";
import { IAttribute } from "../attribute/attribute.container";
import { HighlightedProvider } from "../../context/highlighted";
import AttributeProvider, { useAttributes } from "../../context/attributes_context";
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
    if (!result.destination) {
      return;
    }
    const reorderedItems = reorder(
      attributes,
      result.source.index,
      result.destination.index
    );
    setAttributes(reorderedItems);
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
