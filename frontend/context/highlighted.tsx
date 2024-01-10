import { ReactNode, createContext, useEffect, useState } from "react";

interface IHighlightedContext {
  highlightedAttribute: number;
  setHighlightedAttribute: (name: number) => void;
  showWeights: boolean;
  setShowWeights: (bool: boolean) => void;
  currentWeights: number[];
  setCurrentWeights: React.Dispatch<React.SetStateAction<number[]>>;
}

export const HighlightedContext = createContext<IHighlightedContext>({
  highlightedAttribute: -1,
  setHighlightedAttribute: () => {},
  showWeights: false,
  setShowWeights: () => {},
  currentWeights: [],
  setCurrentWeights: () => {},
});

interface IHighlightedProvider {
  children: ReactNode;
}

export const HighlightedProvider: React.FC<IHighlightedProvider> = ({
  children,
}) => {
  const [highlightedAttribute, setHighlightedAttribute] = useState(-1);
  const [showWeights, setShowWeights] = useState(false);
  const [currentWeights, setCurrentWeights] = useState<number[]>([]);

  useEffect(() => {
    setShowWeights(false);
  }, [highlightedAttribute]);

  return (
    <HighlightedContext.Provider
      value={{
        highlightedAttribute,
        setHighlightedAttribute,
        showWeights,
        setShowWeights,
        currentWeights,
        setCurrentWeights,
      }}
    >
      {children}
    </HighlightedContext.Provider>
  );
};
