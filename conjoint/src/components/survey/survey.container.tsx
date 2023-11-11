"use client";
import React, { FC, useEffect } from "react";
import { Survey } from "./survey";
import { useState } from "react";
import { IAttribute } from "../attribute/attribute.container";
import { HighlightedProvider } from "@/context/highlighted";
import AttributeProvider from "@/context/attributes_context";

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

  return (
    <AttributeProvider>
      <HighlightedProvider>
        <Survey />
      </HighlightedProvider>
    </AttributeProvider>
  );
};
