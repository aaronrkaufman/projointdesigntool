import React, { FC, useState } from "react";

import styles from "./preview__ranking.module.css";
import {
  DragDropContext,
  Draggable,
  DropResult,
  Droppable,
} from "react-beautiful-dnd";
import { IProfile } from "../preview";

export interface PreviewRankingProps {
  refresh: boolean;
  profiles: IProfile[];
}

const reorder = (
  list: IProfile[],
  startIndex: number,
  endIndex: number
): IProfile[] => {
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);
  return result;
};

export const PreviewRanking: FC<PreviewRankingProps> = ({
  profiles,
  refresh,
}) => {
  const [profilesData, setProfilesData] = useState<IProfile[]>(profiles);

  const onDragEnd = (result: DropResult) => {
    // dropped outside the list
    if (!result.destination) {
      return;
    }
    console.log(result.source.index, result.destination!.index);
    const reorderedItems = reorder(
      profilesData,
      result.source.index,
      result.destination!.index
    );

    setProfilesData(reorderedItems);
  };
  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className={styles.preview__ranking}>
        <ul className={styles.ranking__index}>
          {profilesData.map((_, index) => (
            <li key={index}>{index + 1}</li>
          ))}
        </ul>
        <Droppable droppableId={`droppable--ranking`} type="ranking">
          {(provided) => (
            <ul
              className={`${styles.profiles}`}
              {...provided.droppableProps}
              ref={provided.innerRef}
            >
              {profilesData.map((profile, index) => (
                <Draggable
                  key={profile.id}
                  draggableId={`draggable-profile-${profile.id}`}
                  index={index}
                >
                  {(providedHere) => (
                    <li
                      ref={providedHere.innerRef}
                      {...providedHere.draggableProps}
                      className={styles.profile}
                      {...providedHere.dragHandleProps}
                    >
                      {profile.value}
                    </li>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </ul>
          )}
        </Droppable>
      </div>
    </DragDropContext>
  );
};
