import { ReactNode, createContext, useState } from "react";

interface IHighlightedContext {
  highlightedAttribute: number;
  setHighlightedAttribute: (name: number) => void;
  showWeights: boolean;
  setShowWeights: (bool: boolean) => void;
}

export const HighlightedContext = createContext<IHighlightedContext>({
  highlightedAttribute: -1,
  setHighlightedAttribute: () => {},
  showWeights: false,
  setShowWeights: () => {},
});

interface IHighlightedProvider {
  children: ReactNode;
}

export const HighlightedProvider: React.FC<IHighlightedProvider> = ({
  children,
}) => {
  const [highlightedAttribute, setHighlightedAttribute] = useState(-1);
  const [showWeights, setShowWeights] = useState(false);

  return (
    <HighlightedContext.Provider
      value={{
        highlightedAttribute,
        setHighlightedAttribute,
        showWeights,
        setShowWeights,
      }}
    >
      {children}
    </HighlightedContext.Provider>
  );
};
