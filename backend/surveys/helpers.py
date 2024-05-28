'''
THIS IS A HELPER FUNCTION TO CLEAR UP THE VIEWS FILE
'''

import os
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response

from .serializers import  SurveySerializer

import requests, random, json


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


'''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''' MAIN LOGIC  ''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''


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
    serializer = SurveySerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data

        # Convert parameters to types
        attributes = validated_data['attributes']

        # Optional
        constraints = validated_data['constraints']
        restrictions = validated_data['restrictions']
        filename = validated_data['filename']
        profiles = validated_data['profiles']
        tasks = validated_data['tasks']
        randomize = validated_data['randomize']
        repeat_task = validated_data['repeat_task']
        random = validated_data['random']
        advanced = validated_data['advanced']
        duplicate_first = validated_data['duplicate_first']
        duplicate_second = validated_data['duplicate_second']
        
        noFlip = validated_data['noFlip']

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
            file_js.write("let dupprofiles = [" + str(duplicate_first) + "," + str(duplicate_second) + "]" + "\n")
            file_js.write(f"var noDuplicateProfiles = {'false' if repeat_task else 'true'};\n\n")

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
                    for (const key in returnarray) {{
                    if (returnarray.hasOwnProperty(key)) {{
                        if (key.startsWith('F-{}')) {{
                        let correspondingKey = 'F-{}' + key.substring(3); // Get corresponding key starting with 'F-1'
                        if (returnarray[correspondingKey]) {{
                            returnarray[key] = returnarray[correspondingKey]; // Set value of 'F-2' key to be the same as 'F-1' counterpart
                        }}
                        }}
                    }}
                    }}
                    """.format(str(duplicate_first), str(duplicate_second)))
            else:
                file_js.write("""
                let curr = N;
                for (let i = 1; i <= N; i++) {{ // Loop through tasks starting from Task 2
                    let startKey = 'F-{}-' + curr;
                    let trailKey = 'F-{}-' + i;
                    for (let j = 1 ; j <= num_attributes; j++){{
                        let correspondingKey = startKey + '-' + j;
                        let trailCorKey = trailKey + '-' + j;
                        if (returnarray[correspondingKey]){{
                            returnarray[correspondingKey] = returnarray[trailCorKey];
                        }}
                    }};
                    curr -=1;
                }}

                for(let i=1 ; i<=num_attributes; i++){{
                    let startKey = 'F-1-' + i;
                    let trailKey = 'F-2-' + i;
                    if (returnarray[startKey]){{
                        returnarray[startKey] = returnarray[trailKey];
                    }}
                }}""".format(str(duplicate_first), str(duplicate_second)))
            file_js.write("\n")
            file_js.write(temp_4)
            file_js.close()
        return filename
    else:
        return Response(serializer.errors, status=400)


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

def _evaluate_condition(profile, conditions):
    current_result = None
    for cond in conditions:
        attr, op, value = cond['attribute'], cond['operation'], cond['value']
        # Convert operation string to actual operation
        if op == '==': result = profile[attr] == value
        elif op == '!=': result = profile[attr] != value

        if 'logical' in cond:
            if cond['logical'] == '&&':
                current_result = current_result and result if current_result is not None else result
            elif cond['logical'] == '||':
                current_result = current_result or result if current_result is not None else result
        else:
            current_result = result
    return current_result

def _evaluate_result(profile, results):
    # Check the 'Then' part
    for res in results:
        attr, op, value = res['attribute'], res['operation'], res['value']
        if op == '==': 
            if not (profile[attr] == value): return False
        elif op == '!=': 
            if not (profile[attr] != value): return False
    return True

def _evaluate_restriction(profile, restriction):
    if _evaluate_condition(profile, restriction['condition']):
        # If the condition is true, check the result part
        return _evaluate_result(profile, restriction['result'])
    return True

def _check_restrictions(profile, restrictions):
    for restriction in restrictions:
        if not _evaluate_restriction(profile, restriction):
            return False
    return True

def _createProfiles(profiles_num, attributes, restrictions, cross_restrictions, csv_mode):
    cross_profile_restriction_broken = True
    while cross_profile_restriction_broken:
        profiles_list = []
        csv_export = []
        while len(profiles_list) < profiles_num:
            profile = {}
            for attribute in attributes:
                attr_name = attribute['name']
                levels = [level['name'] for level in attribute['levels']]
                profile[attr_name] = random.choice(levels)
            if _check_restrictions(profile, restrictions):
                level = [profile[attr] for attr in profile]
                profiles_list.append(level[:])
                for index, name in enumerate(list(profile.keys())):
                    level.insert(2 * index, name)
                csv_export.append(level)
        cross_profile_restriction_broken = _checkCrossProfileRestrictions(profiles_list, cross_restrictions)
    return profiles_list if not csv_mode else csv_export



'''''''''''''''''''''''''''''''''''''''''''''
''''''''''''QUALTRICS LOGIC''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''



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


def __CreateSurvey(name, user_token, task, num_attr, profiles, currText, js, duplicates, repeatFlip, doubleQ, qText):
    url = "https://yul1.qualtrics.com/API/v3/survey-definitions"
    payload = {"SurveyName": name, "Language": "AR", "ProjectCategory": "CORE"}
    headers = {"Content-Type": "application/json", "X-API-TOKEN": user_token}
    response = requests.request("POST", url, json=payload, headers=headers).json()
    surveyID = response["result"]["SurveyID"]
    d1, d2 = duplicates
    for i in range(task+1): 
        bl = __GetFlow(surveyID, user_token)
        blockID = __CreateBlock(surveyID, bl, user_token)
        currText += qText
        currText += "\n"
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


def __DownloadSurvey(surveyID, user_token, doubleQ, qType):
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
        if qType == "MC":
            questionType = ['MC', 'SAVR']
        elif qType == "Rank":
            questionType = ["RO", "DND"]
        else:
            questionType = ["Slider", "HSLIDER"]
        questionType2 = ['TE', 'SL'] 

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
