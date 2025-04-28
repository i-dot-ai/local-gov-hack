import requests

data_url = 'https://www.planning.data.gov.uk/entity'
dataset_url = 'https://www.planning.data.gov.uk/dataset'


def list_datasets():
    """
    List all available datasets.
    
    Returns:
        dict: JSON response containing all datasets
    """
    response = requests.get(dataset_url + '.json')
    if response.status_code != 200:
        raise Exception('Failed to retrieve datasets')
    return response.json()

def get_all_entities_from_dataset(dataset_id, limit=100):
    """
    Get all entities from a specified dataset.
    
    Args:
        dataset_id (str): ID of the dataset
        limit (int, optional): Maximum number of results to return. Defaults to 100.
        
    Returns:
        list: List of entities in the dataset
    """
    params = {
        'dataset': dataset_id,
        'limit': limit
    }
    return search_entities(params)

# Example usage
if __name__ == "__main__":
    # Example of listing all available datasets
    print("\nListing all datasets...")
    datasets = list_datasets()
    dataset_names=[dataset['name'] for dataset in datasets['datasets']]
    print(f"Found {len(datasets.get('datasets', []))} datasets")
    # Example of getting all entities from a dataset
    # Replace 'example-dataset' with an actual dataset ID
    print("Getting entities from dataset...")
    dataset_entities = get_all_entities_from_dataset('article-4-direction')
    print(f"Found {len(dataset_entities.get('entities', []))} entities")
    
    