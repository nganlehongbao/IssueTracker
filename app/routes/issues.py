import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueStatus, IssueUpdate, IssueOut
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["Issues"])

@router.get("/", response_model=list[IssueOut])
async def get_issues():
    """Retrive all issues."""
    issues = load_data()
    return issues

@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate):
    """Create a new issue"""
    issues = load_data()
    new_issue = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority,
        "status": IssueStatus.open,
    }
    issues.append(new_issue)
    save_data(issues)
    return new_issue

@router.get(f"/{id}", response_model=IssueOut)
def get_issue(id: str):
    """Get an issue detail"""
    issues = load_data()
    for issue in issues:
        if issue["id"] == id:
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found!")

@router.put(f"/{id}", response_model=IssueOut, status_code=status.HTTP_200_OK)
def update_issue(id, payload: IssueUpdate):
    """Update an existing issue"""
    issues = load_data()
    existing_id = None
    for index, issue in enumerate(issues):
        if issue["id"] == id:
            existing_id = index
        
    if existing_id is not None:
        existing_issue = issues[existing_id]
        if payload.title is not None:
            existing_issue["title"] = payload.title
        if payload.description is not None:
            existing_issue["description"] = payload.description
        if payload.priority is not None:
            existing_issue["priority"] = payload.priority
        if payload.status is not None:
            existing_issue["status"] = payload.status
        issues[existing_id] = existing_issue
        save_data(issues)
        return existing_issue
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found!")
    
@router.delete(f"/{id}", status_code=status.HTTP_200_OK)
def delete_issue(id: str):
    """Delete an existing issue"""
    issues = load_data();
    for index, issue in enumerate(issues):
        if issue["id"] == id:
            issues.pop(index)
            save_data(issues)
            return {"message": "Delete issue successfully!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")