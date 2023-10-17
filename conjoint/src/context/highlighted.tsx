import { ReactNode, createContext, useState } from "react";

interface IHighlightedContext {
  highlightedAttribute: number;
  setHighlightedAttribute: (name: number) => void;
}

export const HighlightedContext = createContext<IHighlightedContext>({
  highlightedAttribute: -1,
  setHighlightedAttribute: () => {},
});

interface IHighlightedProvider {
  children: ReactNode;
}

export const HighlightedProvider: React.FC<IHighlightedProvider> = ({
  children,
}) => {
  const [highlightedAttribute, setHighlightedAttribute] = useState(-1);

  return (
    <HighlightedContext.Provider
      value={{ highlightedAttribute, setHighlightedAttribute }}
    >
      {children}
    </HighlightedContext.Provider>
  );
};
