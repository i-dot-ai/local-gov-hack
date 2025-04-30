import requests

BASE_URL = "https://www.planit.org.uk"


def search_planning_applications_by_postcode(postcode, radius=1, recent_days=90):
    """
    Search for planning applications near a postcode.
    
    Args:
        postcode (str): UK postcode to search near
        radius (float): Search radius in kilometers
        recent_days (int): Only return applications from this many recent days
        
    Returns:
        dict: JSON response from the API
    """
    endpoint = f"{BASE_URL}/api/applics/json"
    
    params = {
        "pcode": postcode,
        "krad": radius,
        "recent": recent_days,
        "pg_sz": 10  # Limit to 10 results for simplicity
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error searching for planning applications: {e}")
        return None


def get_planning_application_details(application_name):
    """
    Get detailed information for a specific planning application.
    
    Args:
        application_name (str): The unique name of the planning application
        
    Returns:
        dict: JSON response from the API
    """
    endpoint = f"{BASE_URL}/planapplic/{application_name}/json"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving application details: {e}")
        return None


def display_application_summary(applications):
    """Display a simple summary of planning applications."""
    if not applications or "records" not in applications or not applications["records"]:
        print("No planning applications found.")
        return None
    
    print(f"Found {applications['total']} planning applications. Showing top results:")
    print("-" * 50)
    
    for i, app in enumerate(applications["records"][:3]):  # Show only first 3 for brevity
        start_date = app.get("start_date", "Unknown date")
        description = app.get("description", "No description available")
        # Truncate long descriptions
        if len(description) > 70:
            description = description[:67] + "..."
            
        print(f"{i+1}. [{start_date}] {description}")
    
    # Return the first application for the demo
    if applications["records"]:
        return applications["records"][0]["name"]
    return None


def display_application_details(details):
    """Display simplified information about a planning application."""
    if not details or not isinstance(details, dict):
        print("No details available.")
        return
    
    print("\nPLANNING APPLICATION DETAILS")
    print("-" * 50)
    print(f"Reference: {details.get('reference', 'N/A')}")
    print(f"Status: {details.get('status', 'N/A')}")
    print(f"Address: {details.get('address', 'N/A')}")
    print(f"Description: {details.get('description', 'No description available')[:100]}...")
    
    # Display a link to view the application on PlanIt website
    if "link" in details:
        print(f"View online: {details['link']}")


def main():
    """Main function demonstrating the API with a dummy example."""

    postcode = "SW1A 1AA"  # Westminster, London
    radius = 1
    days = 90
    
    print("UK Planning Applications - Dummy Example")
    print("=" * 50)
    print(f"Searching for planning applications within {radius}km of {postcode}...")
    
    # Search for applications
    applications = search_planning_applications_by_postcode(postcode, radius, days)
    
    if not applications:
        print("Failed to retrieve applications.")
        return
    
    # Display application list and get the first application name
    app_name = display_application_summary(applications)
    
    if not app_name:
        return
    
    print("\nAutomatically selecting the first application for details...")
    
    # Get and display details for the selected application
    details = get_planning_application_details(app_name)
    
    if details:
        display_application_details(details)
    else:
        print("Failed to retrieve application details.")


if __name__ == "__main__":
    main() 
