"""User database with persistent storage."""
import json
import os
from pathlib import Path
import hashlib

class UserDatabase:
    def __init__(self, db_file="users_db.json"):
        self.db_file = Path(db_file)
        self.users = self._load_users()
    
    def _load_users(self):
        """Load users from JSON file."""
        if self.db_file.exists():
            try:
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    # Convert new format to old format for compatibility
                    users = {}
                    for email, user_data in data.items():
                        if 'password_hash' in user_data:
                            # New format
                            users[email] = {
                                "password": user_data["password_hash"],
                                "name": user_data["name"],
                                "id": user_data["id"]
                            }
                        else:
                            # Old format
                            users[email] = user_data
                    return users
            except:
                pass
        return {
            "demo@gmail.com": {
                "password": self._hash_password("demo123"),
                "name": "Demo User",
                "id": "demo_user"
            },
            "test@gmail.com": {
                "password": self._hash_password("password123"),
                "name": "Test User",
                "id": "test_user"
            }
        }
    
    def _save_users(self):
        """Save users to JSON file."""
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def _hash_password(self, password):
        """Hash password for security."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, email, password, name):
        """Create new user."""
        if email in self.users:
            raise ValueError("Email already registered")
        
        user_id = f"user_{len(self.users) + 1}"
        self.users[email] = {
            "password": self._hash_password(password),
            "name": name,
            "id": user_id
        }
        self._save_users()
        return user_id
    
    def verify_user(self, email, password):
        """Verify user credentials."""
        if email not in self.users:
            return None
        
        if self.users[email]["password"] == self._hash_password(password):
            return self.users[email]
        return None
    
    def get_user(self, email):
        """Get user by email."""
        return self.users.get(email)

# Global database instance
user_db = UserDatabase()