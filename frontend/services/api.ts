// services/api.ts
import axios from "axios";
import { Attribute } from "../context/attributes_context";
import { preproccessAttributes, preprocessRestrictions } from "./utils";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
});

export default api;

export const downloadSurvey = async (
  attributes: Attribute[],
  path: "qualtrics" | "export" | "preview_csv"
): Promise<void> => {
  try {
    const processedAttributes = preproccessAttributes(attributes);
    // console.log(processedAttributes);
    const response = await api.post(`/surveys/${path}/`, processedAttributes, {
      responseType: "blob",
    });

    // console.log(response);

    const filename =
      path === "qualtrics"
        ? "default-filename.qsf"
        : path === "export"
        ? "survey.js"
        : path === "preview_csv"
        ? "survey.csv"
        : "survey.js";

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename); // Choose the correct file name and extension
    document.body.appendChild(link);
    link.click();
    window.URL.revokeObjectURL(url);
    link.remove();
  } catch (error) {
    console.error("Error during file download", error);
  }
};

export const getPreview = async (
  attributes: Attribute[]
  // retstrictions: string[][][]
): Promise<string[][]> => {
  console.log("HERE TRIED", api.defaults.baseURL);
  try {
    const processedAttributes = preproccessAttributes(attributes);
    const processedRestrictions = preprocessRestrictions([]);

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
