"use client";
import { ReactNode, createContext, useState } from "react";

interface IDocContext {
  currentDoc: string;
  setCurrentDoc: (doc: string) => void;
  currentDocID: string;
  setCurrentDocID: (docID: string) => void;
  lastEdited: Date;
  setLastEdited: (date: Date) => void;
  surveyFolderOpened: boolean;
  setSurveyFolderOpened: (open: boolean) => void;
  tutorialFolderOpened: boolean;
  setTutorialFolderOpened: (open: boolean) => void;
}

export const DocumentContext = createContext<IDocContext>({
  currentDoc: "",
  setCurrentDoc: () => {},
  currentDocID: "",
  setCurrentDocID: () => {},
  lastEdited: new Date(),
  setLastEdited: () => {},
  surveyFolderOpened: false,
  setSurveyFolderOpened: () => {},
  tutorialFolderOpened: false,
  setTutorialFolderOpened: () => {},
});

interface IDocProvider {
  children: ReactNode;
}

export const DocProvider: React.FC<IDocProvider> = ({ children }) => {
  const [currentDoc, setCurrentDoc] = useState<string>("");
  const [lastEdited, setLastEdited] = useState<Date>(new Date());
  const [currentDocID, setCurrentDocID] = useState<string>("");
  const [surveyFolderOpened, setSurveyFolderOpened] = useState<boolean>(false);
  const [tutorialFolderOpened, setTutorialFolderOpened] = useState<boolean>(false);
  return (
    <DocumentContext.Provider
      value={{
        currentDoc,
        setCurrentDoc,
        currentDocID,
        setCurrentDocID,
        lastEdited,
        setLastEdited,
        surveyFolderOpened,
        setSurveyFolderOpened,
        tutorialFolderOpened,
        setTutorialFolderOpened,
      }}
    >
      {children}
    </DocumentContext.Provider>
  );
};
