// services/api.ts
import axios from "axios";
import { Attribute } from "../context/attributes_context";
import { preproccessAttributes } from "./utils";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

export default api;

export const downloadSurvey = async (
  attributes: Attribute[]
): Promise<void> => {
  try {
    const processedAttributes = preproccessAttributes(attributes);
    console.log(processedAttributes);
    const response = await api.post(
      "/surveys/qualtrics/",
      processedAttributes,
      {
        responseType: "blob",
      }
    );

    console.log(response);

    // Extract the filename from the Content-Disposition header
    // const contentDispositionHeader = response.headers["content-disposition"];
    // const matches = contentDispositionHeader.match(/filename="(.+)"/);
    // const filename = (matches && matches[1]) || "default-filename.qsf";
    const filename = "default-filename.qsf";

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
): Promise<string[][]> => {
  try {
    const processedAttributes = preproccessAttributes(attributes);
    console.log(processedAttributes);
    const response = await api.post("/surveys/preview/", processedAttributes);

    console.log(response);
    return response.data.previews;
  } catch (error) {
    console.error("Error during file download", error);
  }
  return [];
};
