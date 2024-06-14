from pydantic import BaseModel


def to_dict(entity):
    if isinstance(entity, BaseModel):
        return entity.dict(by_alias=True)
    raise TypeError(f"Object of type {entity.__class__.__name__} is not JSON serializable")
