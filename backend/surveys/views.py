from rest_framework.decorators import api_view, permission_classes
from django.http import FileResponse, HttpResponse
from rest_framework import status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from .models import Survey
from .serializers import SurveySerializer, ShortSurveySerializer
from functools import reduce
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
var featureArrayKeys = Object.keys(featurearray);

"""

temp_2_randomize = """// Re-randomize the featurearray

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
"""

temp_2 =  """// Re-insert the non-free attributes constrained by attrconstraintarray
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
for (var p = 1; p <= K; p++) {
  // For each profile i
  for (var i = 1; i <= N; i++) {
    // Repeat until non-restricted profile generated
    var complete = false;

    while (complete == false) {
      complete = true;
      // Create a count for attributes to be incremented in the next loop
      var attr = 0;

      // Create a dictionary to hold profile's attributes
      var profile_dict = {};

      // For each attribute attribute and level array levels in task p
      for (var q = 0; q < featureArrayKeys.length; q++) {
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
        if (weighted == 1) {
          var level_index = weighted_randomize(probabilityarray, attr_name) - 1;
        } else {
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

      // Cycle through restrictions to confirm/reject profile
      for (var k = 0; k < restrictionarray.length; k++) {
        var reDo = 1;
        for (var l = 0; l < 2; l++) {
          if (restrictionarray[k][l * 3 + 1] == "=") {
            if (
              profile_dict[restrictionarray[k][l * 3 + 0]] ==
              restrictionarray[k][l * 3 + 2]
            ) {
              reDo *= 1;
            } else {
              reDo = 0;
            }
          } else if (restrictionarray[k][l * 3 + 1] == "!") {
            if (
              profile_dict[restrictionarray[k][l * 3 + 0]] ==
              restrictionarray[k][l * 3 + 2]
            ) {
              reDo *= 1;
            } else {
              reDo = 0;
            }
          }
        }
        if (reDo == 1) {
          complete = false;
          break;
        }
      }

      // If we're throwing out duplicates
      if (noDuplicateProfiles == true) {
        // For each previous profile
        for (var z = 1; z < i; z++) {
          // Start by assuming it's the same
          var identical = true;

          // Create a count for attributes to be incremented in the next loop
          var attrTemp = 0;

          // For each attribute attribute and level array levels in task p
          for (var qz = 0; qz < featureArrayKeys.length; qz++) {
            // Increment attribute count
            attrTemp = attrTemp + 1;

            // Create keys
            var level_key_profile = "F-" + p + "-" + i + "-" + attrTemp;
            var level_key_check = "F-" + p + "-" + z + "-" + attrTemp;

            // If attributes are different, declare not identical
            if (
              returnarray[level_key_profile] != returnarray[level_key_check]
            ) {
              identical = false;
              break;
            }
          }
          // If we detect an identical profile, reject
          if (identical == true) {
            complete = false;
            break;
          }
        }
      }
    }
  }
}


// Write returnarray to Qualtrics

var returnarrayKeys = Object.keys(returnarray);
"""
temp_dup = """
// Duplicate profiles
for (const key in returnarray) {
  if (returnarray.hasOwnProperty(key)) {
    if (key.startsWith('F-2')) {
      let correspondingKey = 'F-1' + key.substring(3); // Get corresponding key starting with 'F-1'
      if (returnarray[correspondingKey]) {
        returnarray[key] = returnarray[correspondingKey]; // Set value of 'F-2' key to be the same as 'F-1' counterpart
      }
    }
  }
}
"""
temp_4 = """
for (var pr = 0; pr < returnarrayKeys.length; pr++) {
  Qualtrics.SurveyEngine.setEmbeddedData(
    returnarrayKeys[pr],
    returnarray[returnarrayKeys[pr]]
  );
}

"""

def _checkAttributes(attributes):
    # Raise error if level is missing
    for attribute in attributes:
        if len(attribute["levels"]) == 0:
            return Response({"Error": "Cannot export to JavaScript. Some attributes have no levels."}, status=status.HTTP_400_BAD_REQUEST)
    return None


def _cleanConstraints(constraints):
    # Drop any Null constraints
    return [constraint for constraint in constraints if constraint != []]


def _createArrayOrProbString(attributes, isArray):
    arrayString = {}
    for attribute in attributes:
        arrayString[attribute["name"]] = [level["name"] if isArray else level["weight"] for level in attribute["levels"]]

    return f"var {'featurearray' if isArray else 'probabilityarray'} = " + str(arrayString) + ";\n\n"


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
    attributes = request.data.get("attributes", [])

    # Optional
    constraints = request.data.get("constraints", [])
    restrictions = request.data.get("restrictions", [])
    filename = request.data.get("filename", "survey.js")
    profiles = request.data.get("profiles", 2) #PROFILE NUM #FIX
    tasks = request.data.get("tasks", 5)
    randomize = request.data.get("randomize", 1)
    noDuplicates = request.data.get("noDuplicates", 0)
    random = request.data.get("random", 0)
    advanced = request.data.get("advanced", {})
    duplicates = request.data.get("duplicates", [2, 4])
    noFlip = request.data.get("noFlip", 0)

    resp = _checkAttributes(attributes)
    if resp:
        return resp
    constraints = _cleanConstraints(constraints)

    """ Write into file """
    with open(filename, "w", encoding="utf-8") as file_js:
        file_js.write(temp_1)

        file_js.write(_createArrayOrProbString(attributes, True))
        file_js.write("var restrictionarray = "  + str(restrictions) + ";\n\n")
        file_js.write(_createArrayOrProbString(attributes, False) if random == 1 else "var probabilityarray = {};\n\n")

        file_js.write("// Indicator for whether weighted randomization should be enabled or not\n")
        file_js.write("var weighted = " + str(random) + ";\n\n")
        file_js.write("// K = Number of tasks displayed to the respondent\n")
        file_js.write("var K = " + str(tasks) + ";\n\n")
        file_js.write("// N = Number of profiles displayed in each task\n")
        file_js.write("var N = " + str(profiles) + ";\n\n")
        file_js.write("// num_attributes = Number of Attributes in the Array\n")
        file_js.write("var num_attributes = featurearray.length;\n\n")
        file_js.write("// Should duplicate profiles be rejected?\n")
        file_js.write("let dupprofiles = [" + str(duplicates[0]) + "," + str(duplicates[1]) + "]" + "\n")
        file_js.write(f"var noDuplicateProfiles = {'true' if noDuplicates else 'false'};\n\n")

        if randomize == 1:
            file_js.write("var attrconstraintarray = "  + str(constraints) + ";\n\n")
            file_js.write(temp_2_randomize)
            if len(advanced) != 0: # Advanced randomization option (i.e. political party always first)
                attributes_order = [key for key, value in advanced.items() if value != 0]
                attributes_random = [key for key, value in advanced.items() if value == 0]
                #random.shuffle(attributes_random)
                
                attributes_order.sort(key=lambda x: x[1])
                final_order = []

                for i in range(1, len(advanced)+1):
                    if i in advanced.values():
                        final_order.append(attributes_order[0])
                        attributes_order.pop(0)
                    else:
                        final_order.append(attributes_random[-1])
                        attributes_random.pop()

                file_js.write("featureArrayKeys = " + str(final_order)) 
            file_js.write(temp_2)
        else:
            file_js.write(temp_2_star)
            file_js.write("var featureArrayNew = featurearray;\n\n")

        file_js.write(temp_3)
        
        if noFlip:
            file_js.write("""
                // Duplicate profiles
                for (const key in returnarray) {
                if (returnarray.hasOwnProperty(key)) {
                    if (key.startsWith('F-{}')) {
                    let correspondingKey = 'F-{}' + key.substring(3); // Get corresponding key starting with 'F-1'
                    if (returnarray[correspondingKey]) {
                        returnarray[key] = returnarray[correspondingKey]; // Set value of 'F-2' key to be the same as 'F-1' counterpart
                    }
                    }
                }
                }
                """).format(duplicates[0], duplicates[1])
        else:
            file_js.write("""
            for (let i = 1; i <= N; i++) { // Loop through tasks starting from Task 2
                let startKey = 'F-{}-' + curr;
                let trailKey = 'F-{}-' + i;
                for (let j = 1 ; j <= num_attributes; j++){
                    let correspondingKey = startKey + '-' + j;
                    let trailCorKey = trailKey + '-' + j;
                    if (returnarray[correspondingKey]){
                        returnarray[correspondingKey] = returnarray[trailCorKey];
                    }
                };
                curr -=1;
            }

            for(let i=1 ; i<=num_attributes; i++){
                let startKey = 'F-1-' + i;
                let trailKey = 'F-2-' + i;
                if (returnarray[startKey]){
                    returnarray[startKey] = returnarray[trailKey];
                }
            """).format(duplicates[0], duplicates[1])
        file_js.write(temp_4)
        file_js.close()
    return filename


def _checkCrossProfileRestrictions(profiles_list, cross_restrictions):
    # FORMAT -> prof1;att1;==;b;then;prof2;att2;==;d"
    for restriction in cross_restrictions:
        # split if then statement
        res = restriction.split("then")
        if_prof, if_attr, if_op, if_lvl, _ = res[0].strip().split(";")
        _, then_prof, then_attr, then_op, then_lvl = res[1].strip().split(";")
        
        # Check if both ==/==, then as long as there is an isntance of this case, restriction is not broken
        restriction_broken = True
        if if_op == "==" and then_op == "==":
            if if_lvl in profiles_list[0] and then_lvl in profiles_list[1]:
                restriction_broken = False
            if if_lvl in profiles_list[1] and then_lvl in profiles_list[0]:
                restriction_broken = False
            return True if restriction_broken else False
    
        # Check other cases, such as ==/!=, !=/==
        for i in range(2):
            broken_profiles_matched = 0
            if if_lvl in profiles_list[i] and if_op == "==" or if_lvl not in profiles_list[i] and if_op == "!=": 
                broken_profiles_matched += 1
            if then_lvl in profiles_list[1 - i] and then_op == "!=" or then_lvl not in profiles_list[1 - i] and then_op == "==": 
                broken_profiles_matched += 1
            if broken_profiles_matched == 2:
                return True
    return False

def _createProfiles(profiles, attributes, restrictions, cross_restrictions):
    cross_profile_restriction_broken = True
    while cross_profile_restriction_broken:
        profiles_list = []
        for _ in range(profiles): 
            restriction_broken = True
            while restriction_broken:
                levels = []
                level_dict = {}
                for attribute in attributes:
                    lvl = random.choice(attribute["levels"])["name"]
                    level_dict[attribute["name"]] = lvl
                    levels.append(lvl)
                # FORMAT: if att = lvl &&/|| ... then att =/!= lvl
                # "att1;==;b;||;att1;==;a;then;att2;==;d"
                restriction_broken = False
                # Check for restriction break
                for restriction in restrictions:
                    # split if then statement
                    res = restriction.split("then")
                    if_strings = res[0].strip().split(";")
                    if_strings.pop() # remove empty string
                    then_statement = res[1].strip().split(";")
                    then_statement.pop(0) # remove empty string
                    # and_statement: True - for only one statement || for multiple "AND" statements
                    # False: - for multiple "OR" statements
                    and_statement = True
                    if len(if_strings) > 3 and if_strings[3] == "||":
                        and_statement = False
                    
                    if_statements = []
                    for i in range((len(if_strings) + 1) // 4):
                        if_statements.append(if_strings[4 * i : 4 * i + 3])
                    # if the "if statements" are true, then make check_then_statement True
                    check_then_statement = False
                    if and_statement:
                        if all(lvl == level_dict[attr] for attr, _, lvl in if_statements):
                            check_then_statement = True
                    else:
                        if any(lvl == level_dict[attr] for attr, _, lvl in if_statements):
                            check_then_statement = True
                    
                    # if "then statement" is true, then restriction is broken
                    if check_then_statement:
                        attr, op, lvl = then_statement
                        if op == "==":
                            if lvl != level_dict[attr]:
                                restriction_broken = True
                        else:
                            if lvl == level_dict[attr]:
                                restriction_broken = True
                if not restriction_broken:
                    profiles_list.append(levels)
        cross_profile_restriction_broken = _checkCrossProfileRestrictions(profiles_list, cross_restrictions)
    return profiles_list


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
        restrictions = request.data.get("restrictions", [])
        cross_restrictions = request.data.get("cross_restrictions", [])
        profiles = request.data.get("profiles", 2)
        
        if any(not attribute["levels"] for attribute in attributes):
            return Response({"Error": "Cannot export to JavaScript. Some attributes have no levels."}, status=status.HTTP_400_BAD_REQUEST)
        answer["previews"] = _createProfiles(profiles, attributes, restrictions, cross_restrictions)
        answer["attributes"] = [attribute["name"] for attribute in attributes]
        return Response(answer, status=status.HTTP_201_CREATED)
    except:
        return Response(
            {"Error": "Invalid survey data."},
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
        CSV_FILES_NUM = 500
        attributes = request.data.get("attributes")
        restrictions = request.data.get("restrictions", [])
        cross_restrictions = request.data.get("cross_restrictions", [])
        profiles = request.data.get("profiles", 2)

        #To calculate the total number of combinations
        levels_per_attribute = [len(attribute['levels']) for attribute in attributes]
        profiles_per_attribute = [profiles for _ in attributes]
        
        
        header = []
        for i in range(1, len(attributes) + 1):
            for j in range(1, profiles + 2):
                if j == 1:
                    header.append(f'ATT{i}')
                else:
                    header.append(f'ATT{i}P{j-1}')
        previews = []
        previews.append(header)

        rows = []
        while len(rows) < CSV_FILES_NUM:
            row = []
            # Shuffle the attributes for each row
            shuffled_attributes = random.sample(attributes, len(attributes))
            for attribute in shuffled_attributes:
                att_name = attribute['name']
                row.append(att_name)
                for j in range(1, profiles + 1):
                    random_level = random.choice(attribute['levels'])['name']
                    row.append(random_level)
            rows.append(row)

        previews.extend(rows)

        with open("profiles.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerows(previews)
        return _sendFileResponse("profiles.csv")
        #response = HttpResponse(content_type="text/csv", status=status.HTTP_201_CREATED)
        #response["Content-Disposition"] = 'attachment; filename="survey.csv"'

    except:
        return Response(
            {"message": "Invalid survey data."},
            status=status.HTTP_400_BAD_REQUEST,
        )


def __CreateHTML(i, num_attr, profiles, qNum, noFlip):
    if i==0:
        text_out = "<span>Blank page</span>"
        return text_out
    i-=1
    top = (
        "<span>Question "
        + str(qNum + 1)
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
        for n in range(profiles) if noFlip==0 else range(profiles-1,-1,-1):
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


def __CreateSurvey(name, user_token, task, num_attr, profiles, currText, js, duplicates, repeatFlip, doubleQ):
    url = "https://yul1.qualtrics.com/API/v3/survey-definitions"
    payload = {"SurveyName": name, "Language": "AR", "ProjectCategory": "CORE"}
    headers = {"Content-Type": "application/json", "X-API-TOKEN": user_token}
    response = requests.request("POST", url, json=payload, headers=headers).json()
    surveyID = response["result"]["SurveyID"]
    d1, d2 = duplicates
    for i in range(task+1): 
        bl = __GetFlow(surveyID, user_token)
        blockID = __CreateBlock(surveyID, bl, user_token)
        currText = __CreateHTML(i, num_attr, profiles, i-1, 0)
        #if i==d2:
            #currText = __CreateHTML(d1, num_attr, profiles, i-1, repeatFlip)
        currQ = __CreateQuestion(
            surveyID, currText, blockID, user_token, profiles, js, i
        )
        if doubleQ: 
            currQ = __CreateQuestion(
                surveyID, " ", blockID, user_token, profiles, js, i
            )
    __EmbFields(surveyID, user_token, num_attr, profiles, task)
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

def __EmbFields(surveyID, user_token, num_attr ,profiles,tasks):
    url = "https://yul1.qualtrics.com/API/v3/surveys/" + surveyID + "/embeddeddatafields"
    headers = {
        'X-API-TOKEN': user_token,
        'Content-Type': 'application/json'
    }

    fields = []
    for i in range(1, tasks+1):
        for j in range(1, profiles + 1):
            key = F'F-{i}-{j}'
            fields.append({
                "key": key,
                "type": "text"
            })
            for k in range(1, num_attr + 1):
                sub_key = F'{key}-{k}'
                fields.append({
                    "key": sub_key,
                    "type": "text"
                })
 
    payload = { "embeddedDataFields": fields }

    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, application/xml",
    "X-API-TOKEN": user_token
    }

    # Make the API request to set embedded fields without values
    response = requests.post(url, json=payload, headers=headers)


def __DownloadSurvey(surveyID, user_token, doubleQ):
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
        questionType = ['MC', 'SAVR']
        questionType2 = ['TE', 'SL']
        #questionType = ["Slider", "HSLIDER"] 
        #questionType = ["RO", "DND"]

        if response.status_code == 200:
            response_json = response.json()
            qsf_data = response_json.get("result", {})
            
            if doubleQ: 
                counter = 0
                for i in qsf_data['SurveyElements']:
                    if 'Payload' in i:
                        counter +=1
                        curr = i['Payload']
                        if curr and 'QuestionType' in curr:
                            if counter%2==1:
                                curr['QuestionType'] = questionType[0]
                            else:
                                curr['QuestionType'] = questionType2[0]
                        if curr and 'Selector' in curr:
                            if counter%2==1:
                                curr['Selector'] = questionType[1]
                            else:
                                curr['Selector'] = questionType2[1]
            else:
                for i in qsf_data['SurveyElements']:
                    if 'Payload' in i:
                        curr = i['Payload']
                        if curr and 'QuestionType' in curr:
                            curr['QuestionType'] = questionType[0]
                        if curr and 'Selector' in curr:
                            curr['Selector'] = questionType[1]

            # Save the QSF data to a file named "survey.qsf"
            with open("survey.qsf", "w") as qsf_file:
                json.dump(qsf_data, qsf_file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


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
    attributes = request.data.get("attributes", [])
    filename = request.data.get("filename", "export survey")
    profiles = request.data.get("profiles", 2)
    tasks = request.data.get("tasks", 5)
    duplicates = request.data.get("duplicates", [2,4])
    repeatFlip = request.data.get("repeatFlip", 1)
    doubleQ = request.data.get("doubleQ", False)

    resp = _checkAttributes(attributes)
    if resp:
        return resp
    jsname = _createFile(request)
    js_py = json.dumps(request.data)
    with open(jsname, "r", encoding="utf-8") as file_js:
        js_text = file_js.read()
    js_text = "Qualtrics.SurveyEngine.addOnload(function(){" + js_text
    js_text += "\n"
    js_text += "});\nQualtrics.SurveyEngine.addOnReady(function(){\
               \n/*Place your JavaScript here to run when the page is fully displayed*/\
                });\nQualtrics.SurveyEngine.addOnUnload(function()\
                {\n/*Place your JavaScript here to run when the page is unloaded*/});"
    js_text = "//" + js_py + "\n"+ js_text
    user_token = "mz1rvjsRNwqqvl5laoESTZYdUP3nsYPO4fplYncM"  # FIGURE OUT BETTER WAY TO STORE THIS
    created = __CreateSurvey(
        filename, user_token, tasks, len(attributes), profiles, "", js_text, duplicates, repeatFlip, doubleQ
    )
    
    __DownloadSurvey(created, user_token, doubleQ)
    return _sendFileResponse("survey.qsf")


@extend_schema(
    request=None,
    responses={
        201: OpenApiResponse(
            response="application/octet-stream",
            description="Reversing QSF File into Attribute JSON",
            examples=[
                OpenApiExample(
                    name="ReverseQualtricsExample",
                    description="Successful Reversing QSF File into Attribute JSON",
                    value={
                        "attributes": [
                            {
                                "name": "att1",
                                "levels": [
                                    {"name": "b", "weight": 0.5},
                                    {"name": "a", "weight": 0.5},
                                ],
                            },
                            {
                                "name": "att2",
                                "levels": [
                                    {"name": "d", "weight": 0.5},
                                    {"name": "e", "weight": 0.5},
                                ],
                            },
                            {
                                "name": "att3",
                                "levels": [
                                    {"name": "f", "weight": 0.5},
                                    {"name": "g", "weight": 0.5},
                                ],
                            },
                        ],
                        "restrictions" : ["att1 == b || att1 == a then att2 == d"]   

                    }
                )
            ]
        ),
        400: OpenApiResponse(
            response="application/octet-stream",
            description="Error in Reversing QSF File into Attribute JSON",
            examples=[
                OpenApiExample(
                    name="ReverseQualtricsErrorExample",
                    summary="Bad Request Response",
                    description="This response is returned when request to reverse QSF File is unsuccessful",
                    value={
                        "error": "Invalid QSF provided.",
                        "details": "QSF is invalid. Make sure QSF from survey created from projoint is used."
                    },
                )
            ]
        )
}, 
    description="Reversing QSF File into Attribute JSON",
)
@api_view(["POST"])
def qsf_to_attributes(request):
    qsf_data = json.loads(request)
    questions = qsf_data.get("SurveyElements")
    flag = 1
    for i in questions:
        if i.get("PrimaryAttribute") == "QID1":
            payload = i.get("Payload", {})
            js = payload.get("QuestionJS")
            attribute_comment = js.split("\n")[0]
            if "\\" in attribute_comment:
                attribute_comment.replace("\\","")
                attribute_data = json.loads(attribute_comment)
                flag = 0
            break
    if flag: # If QSF invalid, will return empty json
        attribute_data = {}
    return attribute_data

@extend_schema(
    request=SurveySerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            response="text/csv",
            description="A CSV file containing the preview of survey data.",
            examples=[
                OpenApiExample(
                    name="PreviewCSVFileExample",
                    summary="Exported Preview CSV File (No duplicates)",
                    description="A CSV file stream containing the preview of survey data of all possible combinations.",
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
    description="Generates and sends a CSV file of profile combinations based on provided attributes.",
)
@api_view(["POST"])
def noDuplicate_csv(request):
    try:
        CSV_FILES_NUM = 500
        attributes = request.data.get("attributes")
        restrictions = request.data.get("restrictions", [])
        profiles = request.data.get("profiles", 2)

        #To calculate the total number of combinations
        levels_per_attribute = [len(attribute['levels']) for attribute in attributes]
        profiles_per_attribute = [profiles for _ in attributes]
        
        
        header = []
        for i in range(1, len(attributes) + 1):
            for j in range(1, profiles + 2):
                if j == 1:
                    header.append(f'ATT{i}')
                else:
                    header.append(f'ATT{i}P{j-1}')
        previews = []
        previews.append(header)

        rows = []
        while len(rows) < CSV_FILES_NUM:
            row = []
            for attribute in attributes:
                att_name = attribute['name']
                row.append(att_name)
                
                randomized_levels = [random.choice(attribute['levels'])['name'] for _ in range(profiles + 1)]
                row.extend(randomized_levels)
            rows.append(row)

        previews.extend(rows)

        with open("unique_profiles.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerows(previews)
        return _sendFileResponse("profiles.csv")
        #response = HttpResponse(content_type="text/csv", status=status.HTTP_201_CREATED)
        #response["Content-Disposition"] = 'attachment; filename="survey.csv"'

    except:
        return Response(
            {"message": "Invalid survey data."},
            status=status.HTTP_400_BAD_REQUEST,
        )