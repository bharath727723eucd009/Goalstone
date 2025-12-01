// MongoDB initialization script for AI Life Goals system

// Switch to the application database
db = db.getSiblingDB('ai_life_goals');

// Create collections with validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'created_at'],
      properties: {
        user_id: { bsonType: 'string' },
        name: { bsonType: 'string' },
        email: { bsonType: 'string' },
        skills: { bsonType: 'array' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('milestones', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'title', 'category', 'created_at'],
      properties: {
        user_id: { bsonType: 'string' },
        title: { bsonType: 'string' },
        description: { bsonType: 'string' },
        category: { bsonType: 'string' },
        status: { bsonType: 'string' },
        progress: { bsonType: 'double' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('agent_outputs');
db.createCollection('user_progress');

// Create indexes for performance
db.users.createIndex({ 'user_id': 1 }, { unique: true });
db.milestones.createIndex({ 'user_id': 1, 'created_at': -1 });
db.milestones.createIndex({ 'user_id': 1, 'category': 1 });
db.agent_outputs.createIndex({ 'user_id': 1, 'created_at': -1 });
db.agent_outputs.createIndex({ 'user_id': 1, 'agent_type': 1 });
db.user_progress.createIndex({ 'user_id': 1, 'category': 1 }, { unique: true });

print('AI Life Goals database initialized successfully');