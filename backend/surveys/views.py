from rest_framework.decorators import api_view, permission_classes
from django.http import FileResponse, HttpResponse
from rest_framework import status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from .models import Survey
from .serializers import SurveySerializer, ShortSurveySerializer
import requests, os, random, json, csv


# Create your views here.

temp_1 = """// Code to randomly generate conjoint profiles in a Qualtrics survey

// Terminology clarification: 
// Task = Set of choices presented to respondent in a single screen (i.e. pair of candidates)
// Profile = Single list of attributes in a given task (i.e. candidate)
// Attribute = Category characterized by a set of levels (i.e. education level)
// Level = Value that an attribute can take in a particular choice task (i.e. "no formal education")

// Attributes and Levels stored in a 2-dimensional Array 

/* Randomize array in-place using Durstenfeld shuffle algorithm */
function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return(array);
}

// Function to generate weighted random numbers
function weighted_randomize(prob_array, at_key)
{
	var prob_list = prob_array[at_key];
	
	// Create an array containing cutpoints for randomization
	var cumul_prob = new Array(prob_list.length);
	var cumulative = 0.0;
	for (var i=0;  i < prob_list.length; i++){
		cumul_prob[i] = cumulative;
		cumulative = cumulative + parseFloat(prob_list[i]);
	}

	// Generate a uniform random floating point value between 0.0 and 1.0
	var unif_rand = Math.random();

	// Figure out which integer should be returned
	var outInt = 0;
	for (var k = 0; k < cumul_prob.length; k++){
		if (cumul_prob[k] <= unif_rand){
			outInt = k + 1;
		}
	}

	return(outInt);

}
                    """

temp_2_star = """// Place the featurearray keys into a new array
var featureArrayKeys = Object.keys(featurearray);"""

temp_2 = """// Re-randomize the featurearray

// Place the featurearray keys into a new array
var featureArrayKeys = Object.keys(featurearray);

// If order randomization constraints exist, drop all of the non-free attributes
if (attrconstraintarray.length != 0){
	for (const constraints of attrconstraintarray){
		if (constraints.length > 1){
			for (var p = 1; p < constraints.length; p++){
				if (featureArrayKeys.includes(constraints[p])){
					var remkey = featureArrayKeys.indexOf(constraints[p]);
                    featureArrayKeys.splice(remkey, 1);
				}
			}
		}
	}
} 

// Re-randomize the featurearray keys
featureArrayKeys = shuffleArray(featureArrayKeys);

// Re-insert the non-free attributes constrained by attrconstraintarray
if (attrconstraintarray.length != 0){
	for (const constraints of attrconstraintarray){
		if (constraints.length > 1){
			var insertloc = constraints[0];
			if (featureArrayKeys.includes(insertloc)){
				var insert_block = [];
				for (var p = 1; p < constraints.length; p++){
          insert_block.push(constraints[p]);
				}
				var begin_index = featureArrayKeys.indexOf(insertloc);
				featureArrayKeys.splice(begin_index+1, 0, ...insert_block);
			}
		}
	}
}


// Re-generate the new featurearray - label it featureArrayNew
var featureArrayNew = {};
for (var h = 0; h < featureArrayKeys.length; h++){
    featureArrayNew[featureArrayKeys[h]] = featurearray[featureArrayKeys[h]];        
}

"""

temp_3 = """
// Initialize the array returned to the user
// Naming Convention
// Level Name: F-[task number]-[profile number]-[attribute number]
// Attribute Name: F-[task number]-[attribute number]
// Example: F-1-3-2, Returns the level corresponding to Task 1, Profile 3, Attribute 2 
// F-3-3, Returns the attribute name corresponding to Task 3, Attribute 3

var returnarray = {};

// For each task p
for(var p = 1; p <= K; p++){

	// For each profile i
	for(var i = 1; i <= N; i++){

		// Repeat until non-restricted profile generated
		var complete = false;

		while (complete == false){

			// Create a count for attributes to be incremented in the next loop
			var attr = 0;
			
			// Create a dictionary to hold profile's attributes
			var profile_dict = {};

			// For each attribute attribute and level array levels in task p
			for(var q = 0; q < featureArrayKeys.length; q++){
				// Get Attribute name
				var attr_name = featureArrayKeys[q];
					
				// Increment attribute count
				attr = attr + 1;
	
				// Create key for attribute name
				var attr_key = "F-" + p + "-" + attr;
	
                // Store attribute name in returnarray
                returnarray[attr_key] = attr_name;

				// Get length of levels array
				var num_levels = featureArrayNew[attr_name].length;

				// Randomly select one of the level indices
				if (weighted == 1){
					var level_index = weighted_randomize(probabilityarray, attr_name) - 1;

				}else{
					var level_index = Math.floor(Math.random() * num_levels);
				}	

				// Pull out the selected level
				var chosen_level = featureArrayNew[attr_name][level_index];
				
				// Store selected level in profileDict
				profile_dict[attr_name] = chosen_level;
	
				// Create key for level in returnarray
				var level_key = "F-" + p + "-" + i + "-" + attr;
	
				// Store selected level in returnarray
				returnarray[level_key] = chosen_level;

			}

            var clear = true;
            
            // Cycle through restrictions to confirm/reject profile
            if (restrictionarray.length != 0){
                for (var v = 0; v < restrictionarray.length; v++){
                    var falsevar = 1;
                    for (var mp = 0; mp < restrictionarray[v].length; mp++){
                        if (profile_dict[restrictionarray[v][mp][0]] == restrictionarray[v][mp][1]){
                            falsevar = falsevar*1;
                        }else{
                            falsevar = falsevar*0;
                        }							
                    }
                    if (falsevar == 1){
                        clear = false;
                    }
                }
            }
                            
            // If we're throwing out duplicates
            if (noDuplicateProfiles == true){
                // Cycle through all previous profiles to confirm no identical profiles
                if (i > 1){    
                    // For each previous profile
                    for(var z = 1; z < i; z++){
    					
                        // Start by assuming it's the same
                        var identical = true;
    					
                        // Create a count for attributes to be incremented in the next loop
                        var attrTemp = 0;
    					
                        // For each attribute attribute and level array levels in task p
                        for(var qz = 0; qz < featureArrayKeys.length; qz++){
    						
                            // Increment attribute count
                            attrTemp = attrTemp + 1;
    
                            // Create keys 
                            var level_key_profile = "F-" + p + "-" + i + "-" + attrTemp;
                            var level_key_check = "F-" + p + "-" + z + "-" + attrTemp;
    						
                            // If attributes are different, declare not identical
                            if (returnarray[level_key_profile] != returnarray[level_key_check]){
                                identical = false;
                            }
                        }
                        // If we detect an identical profile, reject
                        if (identical == true){
                            clear = false;
                        }
                    }                
                }
            }
            complete = clear;
        }
    }
}
                            
// Write returnarray to Qualtrics

var returnarrayKeys = Object.keys(returnarray);

for (var pr = 0; pr < returnarrayKeys.length; pr++){
       Qualtrics.SurveyEngine.setEmbeddedData(returnarrayKeys[pr], returnarray[returnarrayKeys[pr]]); 
}
"""

"""
def _cleanAttributes(attributes, level_dict):
    # Drop attributes that don't have any levels
    attrout = []
    contin = True
    for i in range(len(attributes)):
        if len(level_dict[attributes[i]]) > 0:
            attrout.append(attributes[i])
        else:
            contin = False
            print("Error: Attribute " + attributes[i] + " has no associated levels")
    if contin == False:
        messagebox.showerror(
            title="Error",
            message="Error: Cannot export to JavaScript. Some attributes have no levels.",
        )
        return
    return attrout
"""

"""
def _cleanConstraints(constraints):
    # Drop any Null constraints
    constrai = []
    for c in constraints:
        if c != []:
            constrai.append(c)
    return constrai
"""


def _createArrayString(attributes, level_dict):
    arrayString = "var featurearray = {"
    for i in range(len(attributes)):
        attr = attributes[i]

        arrayString = arrayString + '"' + attr + '" : ['

        for k in range(len(level_dict[attr])):
            level = level_dict[attr][k]
            arrayString = arrayString + '"' + level + '"'
            if k != len(level_dict[attr]) - 1:
                arrayString = arrayString + ","

        if i != len(attributes) - 1:
            arrayString = arrayString + "],"
        else:
            arrayString = arrayString + "]"

    arrayString = arrayString + "};\n\n"

    return arrayString


def _createRestrictionString(restrictions):
    if len(restrictions) > 0:
        restrictionString = "var restrictionarray = ["
        for m in range(len(restrictions)):
            restrict = restrictions[m]
            restrictionString = restrictionString + "["
            for i in range(len(restrict)):
                entry = restrict[i]
                restrictionString = restrictionString + "["
                restrictionString = restrictionString + '"' + entry[0] + '"'
                restrictionString = restrictionString + ","
                restrictionString = restrictionString + '"' + entry[1] + '"'
                if i != len(restrict) - 1:
                    restrictionString = restrictionString + "],"
                else:
                    restrictionString = restrictionString + "]"
            if m != len(restrictions) - 1:
                restrictionString = restrictionString + "],"
            else:
                restrictionString = restrictionString + "]"

        restrictionString = restrictionString + "];\n\n"
    else:
        restrictionString = "var restrictionarray = [];\n\n"
    return restrictionString


def _createProbString(attributes, probabilities):
    probString = "var probabilityarray = {"
    for i in range(len(attributes)):
        attr = attributes[i]

        probString = probString + '"' + attr + '" : ['
        for k in range(len(probabilities[attr])):
            prob = probabilities[attr][k]
            probString = probString + str(prob)
            if k != len(probabilities[attr]) - 1:
                probString = probString + ","

        if i != len(attributes) - 1:
            probString = probString + "],"
        else:
            probString = probString + "]"

    probString = probString + "};\n\n"
    return probString


def _clearProbabilities(level_dict):
    probabilities = {}

    for k in level_dict:
        probabilities[k] = []
        length = len(level_dict[k])
        for _ in range(length):
            probabilities[k].append(1 / float(length))
    return probabilities


def _refactorAttributes(attributes_list_dict):
    """(TEMPORARY) Refactored to old design"""
    attributes = []
    level_dict = {}
    probabilites = {}
    for attribute in attributes_list_dict:
        attributes.append(attribute["name"])

        level_dict[attribute["name"]] = []
        probabilites[attribute["name"]] = []
        for level in attribute["levels"]:
            level_dict[attribute["name"]].append(level["name"])
            probabilites[attribute["name"]].append(level["weight"])
    return attributes, level_dict, probabilites


def _sendFileResponse(file_path):
    file_js = open(file_path, "rb")
    response = FileResponse(
        file_js,
        content_type="application/javascript",
        status=status.HTTP_201_CREATED,
        as_attachment=True,
        filename=file_path,
    )
    response.closed = file_js.close
    # Delete the file
    os.remove(file_path)
    return response


def _createFile(request):
    # Convert parameters to types
    attributes_list_dict = request.data.get("attributes", [])

    # Optional
    constraints = request.data.get("constraints", [])
    restrictions = request.data.get("restrictions", [])
    filename = request.data.get("filename", "survey.js")
    profiles = request.data.get("profiles", 2)
    tasks = request.data.get("tasks", 5)
    randomize = request.data.get("randomize", 1)
    noDuplicates = request.data.get("noDuplicates", 0)
    random = request.data.get("random", 0)

    # Split attributes(NEW DESIGN) to attributes and level_dict(OLD DESIGN)
    attributes, level_dict, probabilities = _refactorAttributes(attributes_list_dict)

    # attributes = _cleanAttributes(attributes, level_dict)
    # constraints = _cleanConstraints(constraints)
    if probabilities == {}:
        probabilities = _clearProbabilities(level_dict)

    """ Write into file """
    with open(filename, "w", encoding="utf-8") as file_js:
        file_js.write(temp_1)
        file_js.write("\n\n")

        file_js.write(_createArrayString(attributes, level_dict))
        file_js.write(_createRestrictionString(restrictions))

        if random == 1:
            file_js.write(_createProbString(attributes, probabilities))
        else:
            file_js.write("var probabilityarray = {};\n\n")

        file_js.write(
            "// Indicator for whether weighted randomization should be enabled or not\n"
        )
        file_js.write("var weighted = " + str(random) + ";\n\n")
        file_js.write("// K = Number of tasks displayed to the respondent\n")
        file_js.write("var K = " + str(tasks) + ";\n\n")
        file_js.write("// N = Number of profiles displayed in each task\n")
        file_js.write("var N = " + str(profiles) + ";\n\n")
        file_js.write("// num_attributes = Number of Attributes in the Array\n")
        file_js.write("var num_attributes = featurearray.length;\n\n")
        file_js.write("// Should duplicate profiles be rejected?\n")

        file_js.write(
            f"var noDuplicateProfiles = {'true' if noDuplicates else 'false'};\n"
        )

        if randomize == 1:
            file_js.write("\n")

            if len(constraints) > 0:
                constString = "var attrconstraintarray = ["
                for m in range(len(constraints)):
                    const = constraints[m]
                    constString = constString + "["
                    for i in range(len(const)):
                        entry = const[i]
                        constString = constString + '"' + entry + '"'
                        if i != len(const) - 1:
                            constString = constString + ","
                    if m != len(constraints) - 1:
                        constString = constString + "],"
                    else:
                        constString = constString + "]"
                constString = constString + "];\n\n"
            else:
                constString = "var attrconstraintarray = [];\n"

            file_js.write(constString)
            file_js.write("\n")
            file_js.write(temp_2)
        else:
            file_js.write("\n")
            file_js.write(temp_2_star)
            file_js.write("\n")
            file_js.write("var featureArrayNew = featurearray;\n\n")

        file_js.write(temp_3)

        file_js.close()
    return filename


@extend_schema(
    request=SurveySerializer,
    responses={
        201: OpenApiResponse(
            response="application/javascript",
            description="A JavaScript file containing the exported survey data.",
            examples=[
                OpenApiExample(
                    "SurveyJSFileExample",
                    summary="Exported Survey JS File",
                    description="A JavaScript file stream named survey.js containing the exported survey data.",
                    value={
                        "content_type": "application/javascript",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="{filename}"'
                        },
                    },
                )
            ],
        ),
        400: OpenApiResponse(
            response="application/json",
            description="An error response indicating that the request was invalid.",
            examples=[
                OpenApiExample(
                    "Error Example",
                    summary="Bad Request Response",
                    description="This response is returned when the request data is invalid.",
                    value={
                        "error": "Invalid data provided.",
                        "details": "The attributes field is required.",
                    },
                )
            ],
        ),
    },
    description="Export survey to JS. Creates a file on the server and returns it to the user",
)
@api_view(["POST"])
def export_js(request):
    return _sendFileResponse(_createFile(request))


@extend_schema(
    request=ShortSurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="Saves the survey to user's profile",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveySaveSuccess",
                    description="The survey has been successfully saved to the user's profile.",
                    value={"message": "Survey has been saved."},
                    response_only=True,
                    status_codes=[str(status.HTTP_201_CREATED)],
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Bad Request",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveySaveFail",
                    description="The survey data provided is invalid.",
                    value={"error": "Invalid data provided."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                )
            ],
        ),
    },
    description="Saves the survey to user's profile",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_user_survey(request):
    serializer = ShortSurveySerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Survey has been saved."}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="List of user's surveys",
            response=ShortSurveySerializer,
            examples=[
                OpenApiExample(
                    name="SurveyListExample",
                    description="Example of a user having multiple surveys.",
                    value=[
                        {
                            "id": 1,
                            "profile": 1,
                            "attributes": [
                                {
                                    "name": "asfasf",
                                    "levels": [
                                        {"name": "1", "weight": 0.5},
                                        {"name": "2", "weight": 0.5},
                                    ],
                                },
                                {
                                    "name": "asf",
                                    "levels": [
                                        {"name": "3", "weight": 0.5},
                                        {"name": "4", "weight": 0.5},
                                    ],
                                },
                            ],
                            "constraints": [],
                        },
                    ],
                    response_only=True,
                    status_codes=[str(status.HTTP_200_OK)],
                )
            ],
        ),
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            description="No surveys found for the user",
            response=None,
            examples=[
                OpenApiExample(
                    name="NoSurveyExample",
                    description="Example of a user having no surveys.",
                    value={"message": "User has no surveys"},
                    response_only=True,
                    status_codes=[str(status.HTTP_204_NO_CONTENT)],
                )
            ],
        ),
    },
    description="Retrieves the list of surveys belonging to the user",
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_user_surveys(request):
    surveys = Survey.objects.filter(profile=request.user)
    if surveys.exists():
        serializer = ShortSurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "User has no surveys"}, status=status.HTTP_204_NO_CONTENT
        )


@extend_schema(
    request=ShortSurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="Preview of survey generated",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveyPreviewSuccess",
                    description="A successful preview of survey answers.",
                    value={
                        "attributes": ["attribute1", "attribute2"],
                        "previews": [
                            ["a1n1", "a2n1"],
                            ["a1n1", "a2n2"],
                        ],
                    },
                    response_only=True,
                    status_codes=[str(status.HTTP_201_CREATED)],
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Bad Request, no survey data or invalid data provided",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveyPreviewFailEmpty",
                    description="The survey data provided is empty.",
                    value={"message": "Survey is empty."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                ),
                OpenApiExample(
                    name="SurveyPreviewFailInvalid",
                    description="The survey data provided is invalid.",
                    value={"message": "Invalid survey data."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                ),
            ],
        ),
    },
    description="Generates a preview of survey answers based on provided attributes",
)
@api_view(["POST"])
def preview_survey(request):
    try:
        answer = {"attributes": [], "previews": []}
        attributes = request.data.get("attributes")

        if all(not attribute["levels"] for attribute in attributes):
            return Response(
                {"message": "Survey is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for _ in range(2):  # Generate two sets of answers
            answer_set = []
            for attribute in attributes:
                if attribute:
                    answer["attributes"].append(attribute["name"])
                    answer_set.append(random.choice(attribute["levels"])["name"])
            answer["previews"].append(answer_set)
        return Response(answer, status=status.HTTP_201_CREATED)
    except:
        return Response(
            {"message": "Invalid survey data."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(
    request=SurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response="text/csv",
            description="A CSV file containing the preview of survey data.",
            examples=[
                OpenApiExample(
                    name="PreviewCSVFileExample",
                    summary="Exported Preview CSV File",
                    description="A CSV file stream containing the preview of survey data.",
                    value={
                        "content_type": "text/csv",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="preview.csv"'
                        },
                    },
                    response_only=True,
                    status_codes=[str(status.HTTP_201_CREATED)],
                ),
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Bad Request, no survey data or invalid data provided",
            response="application/json",
            examples=[
                OpenApiExample(
                    name="SurveyPreviewFailEmpty",
                    description="The survey data provided is empty.",
                    value={"message": "Survey is empty."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                ),
                OpenApiExample(
                    name="SurveyPreviewFailInvalid",
                    description="The survey data provided is invalid.",
                    value={"message": "Invalid survey data."},
                    response_only=True,
                    status_codes=[str(status.HTTP_400_BAD_REQUEST)],
                ),
            ],
        ),
    },
    description="Generates and sends a CSV file based on provided attributes.",
)
@api_view(["POST"])
def preview_csv(request):
    try:
        previews = []
        attributes = request.data.get("attributes")
        CSV_FILES_NUM = 500

        if all(not attribute["levels"] for attribute in attributes):
            return Response(
                {"message": "Survey is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for i in range(CSV_FILES_NUM):
            preview = [str(i + 1)]
            for _ in range(2):
                for attribute in attributes:
                    if attribute:
                        preview.append(random.choice(attribute["levels"])["name"])
            previews.append(preview)

        with open("profiles.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerows(previews)

        response = HttpResponse(content_type="text/csv", status=status.HTTP_201_CREATED)
        response["Content-Disposition"] = 'attachment; filename="survey.csv"'

        return response
    except:
        return Response(
            {"message": "Invalid survey data."},
            status=status.HTTP_400_BAD_REQUEST,
        )


def __CreateHTML(i, num_attr, profiles):
    top = (
        "<span>Question "
        + str(i + 1)
        + '</span>\n<br /><br />\n<span>Please carefully review the options detailed below, then please answer the questions.</span>\n<br/>\n<br/>\n<span>Which of these choices do you prefer?</span>\n<br />\n<div>\n<br />\n<table class="UserTable">\n<tbody>\n'
    )

    # Create a header row
    header = "<tr>\n<td>&nbsp;</td>\n"
    for k in range(profiles):
        header = (
            header
            + '<td style="text-align: center;">\n<strong>Choice '
            + str(k + 1)
            + "</strong></td>\n"
        )
    header = header + "</tr>\n"

    # Row Array
    rows = ["A"] * num_attr
    for m in range(num_attr):
        rows[m] = (
            "<tr>\n<td style='text-align: center;'><strong>${e://Field/F-"
            + str(i + 1)
            + "-"
            + str(m + 1)
            + "}</strong></td>\n"
        )
        for n in range(profiles):
            rows[m] = (
                rows[m]
                + "<td style='text-align: center;'>${e://Field/F-"
                + str(i + 1)
                + "-"
                + str(n + 1)
                + "-"
                + str(m + 1)
                + "}</td>\n"
            )
        rows[m] = rows[m] + "</tr>"

    # Ending
    footer = "</tbody>\n</table>\n</div>"

    text_out = top + header
    for j in rows:
        text_out = text_out + j

    text_out = text_out + footer
    return text_out


def __CreateBlock(surveyID, bl, user_token):
    url = "https://yul1.qualtrics.com/API/v3/survey-definitions/" + surveyID + "/blocks"
    payload = {"Type": "Standard", "Description": "Block"}
    headers = {"Content-Type": "application/json", "X-API-TOKEN": user_token}

    response = requests.request("POST", url, json=payload, headers=headers).json()
    return response["result"]["BlockID"]


def __CreateSurvey(name, user_token, task, num_attr, profiles, currText, js):
    url = "https://yul1.qualtrics.com/API/v3/survey-definitions"
    payload = {"SurveyName": name, "Language": "AR", "ProjectCategory": "CORE"}
    headers = {"Content-Type": "application/json", "X-API-TOKEN": user_token}
    response = requests.request("POST", url, json=payload, headers=headers).json()
    surveyID = response["result"]["SurveyID"]
    for i in range(task):
        bl = __GetFlow(surveyID, user_token)
        blockID = __CreateBlock(surveyID, bl, user_token)
        currText = __CreateHTML(i, num_attr, profiles)
        currQ = __CreateQuestion(
            surveyID, currText, blockID, user_token, profiles, js, i
        )
    return surveyID


def __CreateQuestion(surveyID, text, blockID, user_token, profiles, js, i):
    url = f"https://yul1.qualtrics.com/API/v3/survey-definitions/{surveyID}/questions"
    querystring = {"blockId": blockID}
    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": user_token,
    }

    # Define the question text and number of answer choices
    question_text = text
    num_choices = profiles  # Replace "n" with the actual number of answer choices

    # Create the answer choices based on the number specified
    answer_choices = {
        str(i): {"Display": f"Profile {i}"} for i in range(1, num_choices + 1)
    }

    # Define the payload to create a multiple-choice question within the specified block
    if i == 0:
        payload = {
            "QuestionText": question_text,
            "QuestionType": "MC",
            "Selector": "SAVR",
            "Choices": answer_choices,
            "QuestionJS": js,
        }
    else:
        payload = {
            "QuestionText": question_text,
            "QuestionType": "MC",
            "Selector": "SAVR",
            "Choices": answer_choices,
        }
    response = requests.post(url, json=payload, headers=headers, params=querystring)


def __GetFlow(surveyID, user_token):
    url = "https://yul1.qualtrics.com/API/v3/survey-definitions/" + surveyID + "/flow"

    headers = {"Content-Type": "application/json", "X-API-TOKEN": user_token}
    response = requests.request("GET", url, headers=headers).json()
    # print(response["result"]["Flow"][0]["ID"])
    return response["result"]["Flow"][0]["ID"]


def __DownloadSurvey(surveyID, user_token):
    url = f"https://yul1.qualtrics.com/API/v3/survey-definitions/{surveyID}"

    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": user_token,
    }

    querystring = {
        "format": "qsf",
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            response_json = response.json()
            qsf_json = response_json.get("result", {})
            qsf_data = json.dumps(qsf_json)  # QSF data in the response text

            # Save the QSF data to a file named "survey.qsf"
            with open("survey.qsf", "w") as qsf_file:
                qsf_file.write(qsf_data)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def __createJS(
    level_dict,
    attributes,
    restrictions,
    random,
    tasks,
    profiles,
    randomize,
    constraints,
    noDuplicates,
    probabilities,
):
    if probabilities == {}:
        probabilities = _clearProbabilities(level_dict)

    """ Write into file """
    js = "Qualtrics.SurveyEngine.addOnload(function() {\n"
    js += "\t" + temp_1 + "\n\n"

    js += "\t" + _createArrayString(attributes, level_dict) + "\n"
    js += "\t" + _createRestrictionString(restrictions) + "\n"

    if random == 1:
        js += "\t" + _createProbString(attributes, probabilities) + "\n"
    else:
        js += "\tvar probabilityarray = {};\n\n"

    js += "\t// Indicator for whether weighted randomization should be enabled or not\n"
    js += "\tvar weighted = " + str(random) + ";\n\n"
    js += "\t// K = Number of tasks displayed to the respondent\n"
    js += "\tvar K = " + str(tasks) + ";\n\n"
    js += "\t// N = Number of profiles displayed in each task\n"
    js += "\tvar N = " + str(profiles) + ";\n\n"
    js += "\t// num_attributes = Number of Attributes in the Array\n"
    js += "\tvar num_attributes = featurearray.length;\n\n"
    js += "\t// Should duplicate profiles be rejected?\n"

    js += "\tvar noDuplicateProfiles = " + str(noDuplicates).lower() + ";\n"

    if randomize == 1:
        js += "\n"

        if len(constraints) > 0:
            constString = "\tvar attrconstraintarray = ["
            for m in range(len(constraints)):
                const = constraints[m]
                constString += "["
                for i in range(len(const)):
                    entry = const[i]
                    constString += '"' + entry + '"'
                    if i != len(const) - 1:
                        constString += ","
                if m != len(constraints) - 1:
                    constString += "],"
                else:
                    constString += "]"
            constString += "];\n\n"
        else:
            constString = "\tvar attrconstraintarray = [];\n"

        js += constString
        js += temp_2
    else:
        js += "\n"
        js += temp_2_star
        js += "\n"
        js += "\tvar featureArrayNew = featurearray;\n\n"
    js += temp_3
    js = js.rstrip("\n")
    js += "\n"
    js += "});\n"
    js += "Qualtrics.SurveyEngine.addOnReady(function() {\n"
    js += "\t/* Place your JavaScript here to run when the page is fully displayed */\n"
    js += "});\n"
    js += "Qualtrics.SurveyEngine.addOnUnload(function() {\n"
    js += "\t/* Place your JavaScript here to run when the page is unloaded */\n"
    js += "});"
    return js


@extend_schema(
    request=SurveySerializer,
    responses={
        201: OpenApiResponse(
            response="application/octet-stream",
            description="Creating Qualtrics survey and exporting QSF file",
            examples=[
                OpenApiExample(
                    name="CreateQualtricsExample",
                    description="Successful creation of Qualtrics survey and export of survey QSF",
                    value={
                        "content_type": "application/octet-stream",
                        "headers": {
                            "Content-Disposition": 'attachment; filename="{filename}"'
                        }             
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            response="application/octet-stream",
            description="Error in creating Qualtrics survey and exporting QSF file",
            examples=[
                OpenApiExample(
                    name="CreateQualtricsErrorExample",
                    summary="Bad Request Response",
                    description="This response is returned when request to create Qualtrics survey and export QSF file is invalid",
                    value={
                        "error": "Invalid data provided.",
                        "details": "Incomplete survey data"
                    },
                )
            ]
        )
}, 
    description="Creating Qualtrics survey and exporting QSF file",
)
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def create_qualtrics(request):
    if request.method == "POST":
        attributes_list_dict = request.data.get("attributes", [])
        filename = request.data.get("filename", "export survey")
        profiles = request.data.get("profiles", 2)
        tasks = request.data.get("tasks", 5)
        jsname = _createFile(request)

        attributes, level_dict, probabilities = _refactorAttributes(
            attributes_list_dict
        )

        with open(jsname, "r", encoding="utf-8") as file_js:
            js_text = file_js.read()

        num_attr = len(attributes)
        user_token = "ZOxp1TYLxPH8dlBs1FogWM3UNdKsLTHVmUAB1Rfm"  # FIGURE OUT BETTER WAY TO STORE THIS
        currText = ""
        created = __CreateSurvey(
            filename, user_token, tasks, num_attr, profiles, currText, js_text
        )
       
        __DownloadSurvey(created, user_token)
        return _sendFileResponse("survey.qsf")
