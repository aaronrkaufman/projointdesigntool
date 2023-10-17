"use client";
import React, { FC, useEffect } from "react";
import { Survey } from "./survey";
import { useState } from "react";
import { IAttribute } from "../attribute/attribute.container";
import { HighlightedProvider } from "@/context/highlighted";

export const SurveyContainer: FC = () => {
  const [attributes, setAttributes] = useState<IAttribute[]>([
    {
      name: "Age",
      levels: [{ name: "10-20" }, { name: "20-30" }, { name: "30-40" }],
      key: 0,
      weights: [0.33, 0.33, 0.33],
    },
    {
      name: "Education",
      levels: [
        { name: "No Formal" },
        { name: "4th Grade" },
        { name: "8th Grade" },
        { name: "High School" },
        { name: "Two-Year College" },
      ],
      key: 1,
      weights: [0.2, 0.2, 0.2, 0.2, 0.2],
    },
  ]);

  const [isCreatingAttribute, setIsCreatingAttribute] = useState(false);

  const handleCreateAttribute = () => setIsCreatingAttribute(true);

  const addNewAttribute = (name: string) => {
    setAttributes([
      ...attributes,
      { name, levels: [], key: attributes.length + 1, weights: [] },
    ]);
    setIsCreatingAttribute(false);
  };

  const cancelNewAttribute = () => setIsCreatingAttribute(false);

  const addLevelToAttribute = (attributeName: string, newLevel: string) => {
    setAttributes((prevAttributes) =>
      prevAttributes.map((attribute) =>
        attribute.name === attributeName
          ? { ...attribute, levels: [...attribute.levels, { name: newLevel }] }
          : attribute
      )
    );
  };

  return (
    <HighlightedProvider>
      <Survey
        attributes={attributes}
        isCreatingAttribute={isCreatingAttribute}
        onAddAttribute={addNewAttribute}
        onCancelNewAttribute={cancelNewAttribute}
        onAddLevelToAttribute={addLevelToAttribute}
        onCreateAttribute={handleCreateAttribute}
      />
    </HighlightedProvider>
  );
};
