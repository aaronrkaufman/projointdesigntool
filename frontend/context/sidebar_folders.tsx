import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SidebarFoldersState {
  surveyFolderOpened: boolean;
  setSurveyFolderOpened: () => void;
  tutorialFolderOpened: boolean;
  setTutorialFolderOpened: () => void;
}

export const useSidebarFoldersStore = create(
  persist<SidebarFoldersState>(
    (set) => ({
      surveyFolderOpened: false,
      setSurveyFolderOpened: () =>
        set((state) => ({ surveyFolderOpened: !state.surveyFolderOpened })),
      tutorialFolderOpened: false,
      setTutorialFolderOpened: () =>
        set((state) => ({ tutorialFolderOpened: !state.tutorialFolderOpened })),
    }),
    {
      name: "sidebar-folders-storage", // unique name of the storage (required)
    }
  )
);
