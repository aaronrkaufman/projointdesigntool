import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from tkinter import messagebox

app = Flask(__name__)
CORS(app)

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


def _cleanConstraints(constraints):
    # Drop any Null constraints
    constrai = []
    for c in constraints:
        if c != []:
            constrai.append(c)
    return constrai


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


"""
{
    [
        {
            name: attribute_name, 
            levels: [
                        {
                            name: level_name, 
                            weight: float
                        },
                        {
                            name: level_name, 
                            weight: float
                        }
                    ]
        }
        
    ]
}
"""


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


@app.route("/api/v1/exportJS", methods=["POST"])
def exportToJS():
    """
    POST Method to export survey to JS
    Creates a file on the server and then (TODO)returns it to the user

    :attr:`attributes` -> List[Dict] Required
    """

    # Convert parameters to types
    data = request.json
    attributes_list_dict = data.get("attributes", [])

    # Optional
    constraints = data.get("constraints", [])
    restrictions = data.get("restrictions", [])
    filename = data.get("filename", "survey.js")
    profiles = data.get("profiles", 2)
    tasks = data.get("tasks", 5)
    randomize = data.get("randomize", 1)
    noDuplicates = data.get("noDuplicates", 0)
    random = data.get("random", 0)

    # Split attributes(NEW DESIGN) to attributes and level_dict(OLD DESIGN)
    attributes, level_dict, probabilities = _refactorAttributes(attributes_list_dict)

    attributes = _cleanAttributes(attributes, level_dict)
    constraints = _cleanConstraints(constraints)
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

    return send_from_directory(os.getcwd(), filename, as_attachment=True), 201


if __name__ == "__main__":
    app.run(port=5000, debug=True)


exportToJS()
