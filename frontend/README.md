# Frontend for Conjoint Survey Tool

Projoint is a Django-based project that provides a robust platform for managing projects and collaborations. This README file includes instructions on how to set up the project and see how the project would look like.

## Setup

Open the frontend folder and in the terminal install all dependencies
```
pnpm i
```

After that, you can run the project using this command
```
pnpm run dev
```

## View

The project could be viewed at localhost:3000/documents/document

## Functionalities

Currently implemented:

- Adding attributes locally
- Adding levels locally
- Changing the positions of attributes (Drag & Drop)
- Changing the name of the document

Needs to be implemented:

- Adding new documents locally
- Connect to backend
- Editing the attribute (delete, change name)
- Editing the levels (delete, change name)
- Exporting (Qualtrics, Python)
- Preview
- Settings
- Restrictions
- Update weights (works, but some tweaks for correct work)
