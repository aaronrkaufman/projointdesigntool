import classNames from "classnames";

interface BEMOptions {
  e?: string; // Element
  m?: Record<string, boolean>; // Modifiers
}

export const cn = (block: string) => {
  return ({ e, m }: BEMOptions = {}) => {
    const element = e ? `${block}__${e}` : block;
    const modifiers = m
      ? Object.keys(m).reduce((acc, key) => {
          if (m[key]) {
            acc[`${element}_${key}`] = m[key];
          }
          return acc;
        }, {} as Record<string, boolean>)
      : {};
    return classNames(element, modifiers);
  };
};
