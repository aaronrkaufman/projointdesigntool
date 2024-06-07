### Managing Text Elements in the Application Interface

This instructions are designed to help you understand and manage the static text elements that appear on the application's frontend. All modifiable text elements are stored in a JSON format in the file `/english.json`.

#### Example structure

```json
"surveyPage": {
    "description": {
      "value": "Enter your description here! Example: 'Here are two profiles A and B.'"
    },
    "instructions": {
      "value": "Enter your instructions here! Example: 'Do you prefer A or B?'"
    },
    "attribute": {
      "editWeights": {
        "value": "Edit Weights"
      },
      "saveWeights": {
        "value": "Save Weights"
      },
      "deleteAttribute": {
        "value": "Delete Attribute"
      },
      "addLevel": {
        "value": "Add Level"
      },
      "addAttribute": {
        "value": "Add Attribute"
      }
    }
}
```

#### Editing Text Values

To modify the text that appears on the frontend, locate the corresponding key in the `english.json` file and change the text within the "value" or "subtitle" field. !Changes to other parts of the structure may cause the application to behave unexpectedly! After making changes, the server may need to be restarted for the changes to take effect.

#### Future Enhancements

- Adding Links: I plan to include the ability to add hyperlinks to text elements, allowing for more interactive and connected content.
- Clickable Elements: I plan to make text elements clickable when necessary, for navigation.
