"use client";
import { ReactNode, createContext, useState } from "react";

interface IDocContext {
  currentDoc: string;
  setCurrentDoc: (doc: string) => void;
}

export const DocumentContext = createContext<IDocContext>({
  currentDoc: "",
  setCurrentDoc: () => {},
});

interface IDocProvider {
  children: ReactNode;
}

export const DocProvider: React.FC<IDocProvider> = ({ children }) => {
  const [currentDoc, setCurrentDoc] = useState<string>("");
  return (
    <DocumentContext.Provider
      value={{
        currentDoc,
        setCurrentDoc,
      }}
    >
      {children}
    </DocumentContext.Provider>
  );
};
