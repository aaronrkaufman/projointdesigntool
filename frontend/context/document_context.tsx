"use client";
import { ReactNode, createContext, useState } from "react";

interface IDocContext {
  currentDoc: string;
  setCurrentDoc: (doc: string) => void;
  lastEdited: Date;
  setLastEdited: (date: Date) => void;
}

export const DocumentContext = createContext<IDocContext>({
  currentDoc: "",
  setCurrentDoc: () => {},
  lastEdited: new Date(),
  setLastEdited: () => {},
});

interface IDocProvider {
  children: ReactNode;
}

export const DocProvider: React.FC<IDocProvider> = ({ children }) => {
  const [currentDoc, setCurrentDoc] = useState<string>("");
  const [lastEdited, setLastEdited] = useState<Date>(new Date());
  return (
    <DocumentContext.Provider
      value={{
        currentDoc,
        setCurrentDoc,
        lastEdited,
        setLastEdited,
      }}
    >
      {children}
    </DocumentContext.Provider>
  );
};
