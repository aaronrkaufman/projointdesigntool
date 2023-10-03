// AttributeContainer.tsx
import React, { FC, useState } from "react";
import { Attribute } from "./attribute";
import { AttributeCreator } from "./attribute_creator";

export interface ILevel {
  name: string;
  weight?: number;
}

export interface IAttribute {
  name: string;
  levels: ILevel[];
}

interface PropsAttributeContainer {
  attribute?: IAttribute;
  addLevel?: (attributeName: string, newLevel: string) => void;
  addNewAttribute?: (name: string) => void;
  cancelNewAttribute?: () => void;
  isCreator?: boolean; // To determine whether to render AttributeCreator or AttributeComponent
}

export const AttributeContainer: FC<PropsAttributeContainer> = ({
  attribute,
  addLevel,
  addNewAttribute,
  cancelNewAttribute,
  isCreator = false,
}) => {
  const [show, setShow] = useState<boolean>(false);
  const [newLevel, setNewLevel] = useState<string>("");
  const [name, setName] = useState<string>("");

  // Handle key press for AttributeComponent
  const handleKeyPressAttribute = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && newLevel.trim() !== "" && addLevel) {
      if (attribute) addLevel(attribute.name, newLevel);
      setNewLevel("");
    }
  };

  // Handle blur for AttributeCreator
  const handleBlurCreator = () => {
    if (name.trim() === "" && cancelNewAttribute) {
      cancelNewAttribute();
    } else if (addNewAttribute) {
      addNewAttribute(name);
    }
  };

  // Handle key press for AttributeCreator
  const handleKeyPressCreator = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && name.trim() !== "" && addNewAttribute) {
      addNewAttribute(name);
    }
  };

  const handleShow = () => setShow(!show);

  return isCreator ? (
    <AttributeCreator
      addNewAttribute={addNewAttribute!}
      cancelNewAttribute={cancelNewAttribute!}
      onBlur={handleBlurCreator}
      onKeyDown={handleKeyPressCreator}
      onChange={(e) => setName(e.target.value)}
    />
  ) : (
    <Attribute
      show={show}
      newLevel={newLevel}
      onShow={handleShow}
      onKeyPress={handleKeyPressAttribute}
      onBlur={() => setNewLevel("")}
      onChange={(e) => setNewLevel(e.target.value)}
      attribute={attribute!}
    />
  );
};