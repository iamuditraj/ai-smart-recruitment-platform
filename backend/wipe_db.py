import os
import sys

# Ensure backend is in path so we can import services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.firebase_service import get_db

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc: {doc.reference.path}')
        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

if __name__ == "__main__":
    from services.firebase_service import init_firebase
    init_firebase()
    db = get_db()
    if not db:
        print("Could not connect to Firestore.")
        sys.exit(1)
        
    collections_to_wipe = [
        'users',
        'candidates',
        'recruiters',
        'user_index',
        'job_applications',
        'jobs',
        'resumes',
        'candidate_profiles'
    ]
    
    for coll_name in collections_to_wipe:
        print(f"\n--- Wiping collection: {coll_name} ---")
        delete_collection(db.collection(coll_name), 50)
        
    print("\nDatabase wiped successfully! You can now start completely fresh.")
