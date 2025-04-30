from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    applicationDetails = {
        "reference": "RB/2025/0742/HH",
        "address": "10 Seaforth Gardens, Woodford Green",
        "proposal": "Loft conversion with rear dormers incorporating a Juliet balcony, removal of chimney breast, and insertion of four front roof lights",
        "applicant": "Mr. & Mrs. Rodriguez",
        "agentName": "Woodford Architectural Services",
        "received": "12 April 2025",
        "validated": "19 April 2025",
        "type": "Householder Planning Permission",
        "status": "Under Assessment",
        "description": "Loft conversion to create additional bedroom space. Works include installation of rear dormer windows with a Juliet balcony, removal of chimney breast, and insertion of four front roof lights. Materials to include tiles for the dormer cheeks to match existing as closely as possible, and uPVC window frames.",
        "materials": "Roof: Tiles \n Windows/Doors: uPVC frames \n Dormer cheeks: Tile hung to match existing",
        "constraints": "Flood Zone 1 (low risk) \n Not in a Conservation Area \n Not a Listed Building",
        "documents": [
            "Completed application form with ownership certificate",
            "Site location plan and block plan",
            "Existing and proposed floor plans",
            "Existing and proposed elevations",
            "Existing and proposed roof plans",
            "Flood Risk Assessment"
        ]
    }
    feedbackPoints = [
        {
            "point": "The proposal appears to include the necessary information for validation according to local requirements",
            "policyRef": None,
            "type": "General"
        },
        {
            "point": "The proposal involves changes to the roof design, scale and appearance of the property",
            "policyRef": "LP26",
            "type": "Design"
        },
        {
            "point": "As a household extension, the proposal must complement the character of the existing building and be subordinate in scale",
            "policyRef": "LP30",
            "type": "Key Consideration"
        },
        {
            "point": "Materials (tiles for dormer cheeks to match existing) appear appropriate but detail is somewhat limited",
            "policyRef": "LP26",
            "type": "Materials"
        },
        {
            "point": "The dormer windows and Juliet balcony may affect neighbour privacy and outlook",
            "policyRef": "LP30",
            "type": "Amenity Impact"
        },
        {
            "point": "The Flood Risk Assessment confirms the site is in Flood Zone 1 (low risk)",
            "policyRef": "LP21",
            "type": "Environmental"
        }
    ]
    relevantPolicies = [
        {
            "id": "LP30",
            "name": "Household Extensions",
            "relevance": "Highly Relevant",
            "description": "Directly relevant for household extensions including loft conversions and dormers. The extension must complement the character of the building, be subordinate in scale, maintain adequate spacing, retain sufficient amenity space, avoid adverse impacts on sunlight/daylight to neighbouring properties, and respect local character."
        },
        {
            "id": "LP26",
            "name": "Promoting High Quality Design",
            "relevance": "Highly Relevant",
            "description": "Requires all development to demonstrate high quality design. The extension must complement the character of the existing building, be well integrated, and respect the surrounding area in terms of layout, form, style, and materials."
        },
    ]   
    return render_template('index.html', applicationDetails=applicationDetails, relevantPolicies=relevantPolicies )

if __name__ == "__main__":
    app.run()
    