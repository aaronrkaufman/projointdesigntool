// services/api.ts
import axios from "axios";
import { Attribute } from "../context/attributes_context";
import { preproccessAttributes, preprocessRestrictions } from "./utils";
import { RestrictionProps } from "@/components/restrictions/restriction";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
});

export default api;

export const downloadSurvey = async (
  attributes: Attribute[],
  path: "qualtrics" | "export" | "export_csv" | "markdown",
  filename: string,
  csv_lines?: number,
  settings?: number
): Promise<void> => {
  try {
    const processedAttributes = preproccessAttributes(attributes);
    // console.log(processedAttributes);
    const response = await api.post(
      `/surveys/${path}/`,
      { ...processedAttributes, csv_lines, settings },
      {
        responseType: "blob",
      }
    );

    // console.log(response);
    const fileExtension = (filename: string) => {
      switch (path) {
        case "qualtrics":
          return filename + ".qsf";
        case "export":
          return filename + ".js";
        case "export_csv":
          return filename + ".csv";
        case "markdown":
          return filename + ".md";
        default:
          return filename;
      }
    };

    const file = fileExtension(filename);

    console.log("filename", file);

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", file); // Choose the correct file name and extension
    document.body.appendChild(link);
    link.click();
    window.URL.revokeObjectURL(url);
    link.remove();
  } catch (error) {
    console.error("Error during file download", error);
  }
};

export const getPreview = async (
  attributes: Attribute[],
  restrictions: RestrictionProps[]
): Promise<string[][]> => {
  try {
    const processedAttributes = preproccessAttributes(attributes);
    const processedRestrictions = preprocessRestrictions(restrictions);

    const response = await api.post("/surveys/preview/", {
      ...processedRestrictions,
      ...processedAttributes,
    });

    // console.log(response);
    return response.data.previews;
  } catch (error) {
    console.error("Error during file download", error);
  }
  return [];
};

export const getTutorials = async () => {
  const response = await api.get("/common/docs/list/");
  return response.data;
};

export const getTutorial = async (tutorial: string) => {
  const tutorialWithoutMd = tutorial.replace(".md", "");

  const response = await api.get(`/common/docs/${tutorialWithoutMd}/`);
  return response.data;
};
