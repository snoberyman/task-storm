# app/graphql/tasks_graphql.py
from flask import Blueprint, request, jsonify
from ariadne import gql, make_executable_schema, graphql_sync, ObjectType, MutationType
from ariadne.explorer import ExplorerGraphiQL
from bson import ObjectId
from app.extensions import mongo  # adjust this import based on your project

# -----------------------
# 1️⃣ GraphQL type definitions
# -----------------------
type_defs = gql("""     
    enum Priority {
        LOW
        MEDIUM
        HIGH
    }
    
    type Task {
        id: ID!
        title: String!
        description: String
        completed: Boolean!
        tags: [String!]
        priority: Priority
    }

    type Query {
        tasks: [Task!]!
        task(id: ID!): Task
    }

    type Mutation {
        createTask(
            title: String!
            description: String
            tags: [String!]
            priority: Priority
        ): Task!

        updateTask(
            id: ID!
            title: String
            description: String
            completed: Boolean
            tags: [String!]
            priority: Priority
        ): Task

        deleteTask(id: ID!): String
        
        autoPrioritizeTasks: [Task!]!
    }
""")

# -----------------------
# 2️⃣ Resolvers
# -----------------------
query = ObjectType("Query")
mutation = MutationType()

# --- Query Resolvers ---
@query.field("tasks")
def resolve_tasks(_, info):
    if mongo.db is None:
        raise Exception("MongoDB connection not initialized. Please check DATABASE_URL environment variable.")
    tasks = list(mongo.db.tasks.find())
    for t in tasks:
        t["id"] = str(t["_id"])
    return tasks

@query.field("task")
def resolve_task(_, info, id):
    if mongo.db is None:
        raise Exception("MongoDB connection not initialized. Please check DATABASE_URL environment variable.")
    task = mongo.db.tasks.find_one({"_id": ObjectId(id)})
    if not task:
        return None
    task["id"] = str(task["_id"])
    return task

# --- Mutation Resolvers ---
@mutation.field("createTask")
def resolve_create_task(_, info, title, description="", tags=None, priority="LOW"):
    if mongo.db is None:
        raise Exception("MongoDB connection not initialized. Please check DATABASE_URL environment variable.")
    task = {
        "title": title,
        "description": description,
        "completed": False,
        "tags": tags or [],
        "priority": priority  # stored as string: "LOW", "MEDIUM", "HIGH"
    }

    result = mongo.db.tasks.insert_one(task)
    task["id"] = str(result.inserted_id)
    return task

@mutation.field("updateTask")
def resolve_update_task(_, info, id, title=None, description=None, completed=None, tags=None, priority=None):
    if mongo.db is None:
        raise Exception("MongoDB connection not initialized. Please check DATABASE_URL environment variable.")
    updates = {}

    if title is not None:
        updates["title"] = title
    if description is not None:
        updates["description"] = description
    if completed is not None:
        updates["completed"] = completed
    if tags is not None:
        updates["tags"] = tags
    if priority is not None:
        updates["priority"] = priority

    mongo.db.tasks.update_one(
        {"_id": ObjectId(id)},
        {"$set": updates}
    )

    task = mongo.db.tasks.find_one({"_id": ObjectId(id)})
    task["id"] = str(task["_id"])
    return task

@mutation.field("deleteTask")
def resolve_delete_task(_, info, id):
    if mongo.db is None:
        raise Exception("MongoDB connection not initialized. Please check DATABASE_URL environment variable.")
    mongo.db.tasks.delete_one({"_id": ObjectId(id)})
    return "Task deleted"

@mutation.field("autoPrioritizeTasks")
def resolve_auto_prioritize(_, info):
    """
    Fetch all tasks, send to local Mistral model, update priorities in DB,
    and return updated tasks.
    """
    if mongo.db is None:
        raise Exception("MongoDB connection not initialized. Please check DATABASE_URL environment variable.")
    # 1️⃣ Fetch tasks from DB
    tasks = list(mongo.db.tasks.find())
    for t in tasks:
        t["id"] = str(t["_id"])

    # 2️⃣ Prepare task list for the helper
    task_list = [{"id": t["id"], "title": t["title"], "description": t.get("description", "")} for t in tasks]

    # 3️⃣ Call the helper function (you created)
    from utils.prioritize import prioritize_tasks  # adjust the import if needed
    try:
        prioritized = prioritize_tasks(task_list)
    except Exception as e:
        raise Exception(f"Error calling Mistral: {e}")

    # 4️⃣ Update tasks in DB with new priorities
    for p in prioritized:
        mongo.db.tasks.update_one(
            {"_id": ObjectId(p["id"])},
            {"$set": {"priority": p["priority"]}}
        )

    # 5️⃣ Return updated tasks
    updated_tasks = list(mongo.db.tasks.find())
    for t in updated_tasks:
        t["id"] = str(t["_id"])
    return updated_tasks


# -----------------------
# 3️⃣ Create executable schema
# -----------------------
schema = make_executable_schema(type_defs, query, mutation)

# -----------------------
# 4️⃣ Blueprint & GraphiQL
# -----------------------
tasks_bp = Blueprint("tasks_graphql", __name__, url_prefix="/graphql")
explorer_html = ExplorerGraphiQL().html(None)

@tasks_bp.route("", methods=["GET"])
def graphql_playground():
    return explorer_html, 200

@tasks_bp.route("", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    status_code = 200 if success else 400
    return jsonify(result), status_code
