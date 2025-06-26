from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import config

router = APIRouter(
  prefix='/demo',
  tags=['demo'],
  responses={404: {'description': 'Not found'}}
)

class DemoItem(BaseModel):
  id: int
  name: str
  description: Optional[str] = None
  created_at: datetime
  tags: List[str] = []

class CreateDemoItem(BaseModel):
  name: str
  description: Optional[str] = None
  tags: List[str] = []

# Mock data for demo
demo_items = [
  DemoItem(
    id=1,
    name="Sample Item 1",
    description="This is a sample item for demonstration",
    created_at=datetime.now(),
    tags=["sample", "demo"]
  ),
  DemoItem(
    id=2,
    name="Sample Item 2",
    description="Another sample item",
    created_at=datetime.now(),
    tags=["demo", "test"]
  )
]

@router.get("/", response_model=List[DemoItem])
async def list_demo_items(
  limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
  offset: int = Query(0, ge=0, description="Number of items to skip")
):
  """List demo items with pagination."""
  return demo_items[offset:offset + limit]

@router.get("/{item_id}", response_model=DemoItem)
async def get_demo_item(item_id: int):
  """Get a specific demo item by ID."""
  for item in demo_items:
    if item.id == item_id:
      return item
  raise HTTPException(status_code=404, detail="Item not found")

@router.post("/", response_model=DemoItem)
async def create_demo_item(item: CreateDemoItem):
  """Create a new demo item."""
  new_id = max([item.id for item in demo_items]) + 1 if demo_items else 1
  new_item = DemoItem(
    id=new_id,
    name=item.name,
    description=item.description,
    created_at=datetime.now(),
    tags=item.tags
  )
  demo_items.append(new_item)
  return new_item

@router.put("/{item_id}", response_model=DemoItem)
async def update_demo_item(item_id: int, item: CreateDemoItem):
  """Update an existing demo item."""
  for i, existing_item in enumerate(demo_items):
    if existing_item.id == item_id:
      updated_item = DemoItem(
        id=item_id,
        name=item.name,
        description=item.description,
        created_at=existing_item.created_at,
        tags=item.tags
      )
      demo_items[i] = updated_item
      return updated_item
  raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{item_id}")
async def delete_demo_item(item_id: int):
  """Delete a demo item."""
  for i, item in enumerate(demo_items):
    if item.id == item_id:
      deleted_item = demo_items.pop(i)
      return {"message": f"Item {item_id} deleted successfully", "deleted_item": deleted_item}
  raise HTTPException(status_code=404, detail="Item not found")

@router.get("/info/environment")
async def get_environment_info():
  """Get information about the current environment."""
  return {
    "environment": config.env,
    "api_version": config.API_VERSION,
    "debug_mode": config.env_config['debug'],
    "log_level": config.LOG_LEVEL
  } 