import { v4 as uuidv4 } from "uuid";
import { NextRouter } from "next/router";

// Abstracted function with customization options via parameters
export const addSurvey = ({
  router,
  value,
  onStorageChange,
}: {
  router: NextRouter;
  value?: any;
  onStorageChange: (updateFunc: (prev: number) => number) => void;
}) => {
  const uniqueId = uuidv4();
  const dataToSave = {
    attributes: value ? value.attributes : [],
    lastEdited: new Date(),
    name: "Untitled",
    instructions: {
      description: "",
      instructions: "",
      outcomeType: "mcq",
    },
    restrictions: value ? value.restrictions : [],
    crossRestrictions: value ? value.cross_restrictions : [],
    settings: {
      numProfiles: value ? value.profiles : 2,
      numTasks: value ? value.tasks : 2,
      repeatedTasks: value ? value.repeat_task : true,
      repeatedTasksFlipped: value ? value.noFlip : false,
      taskToRepeat: value ? value.duplicate_first : 1,
      whereToRepeat: value ? value.duplicate_second : 1,
      randomize: value ? value.randomize : false,
      noFlip: value ? value.noFlip : false,
    },
  };
  localStorage.setItem(`attributes-${uniqueId}`, JSON.stringify(dataToSave));
  if (onStorageChange) {
    onStorageChange((prev: number) => prev + 1);
  }
  router.push(`/${encodeURIComponent(uniqueId)}`);
};
