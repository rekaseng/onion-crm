from pydantic import BaseModel
from infrastructure.db.base_class import Base


#syd: a generic update function that remove or the meta_attributes
def update_orm_model_from_domain(orm_model: Base, domain_model: BaseModel, exclude_fields=None):
    """Update an ORM model instance from a Pydantic domain model, excluding specified fields."""
    if exclude_fields is None:
        exclude_fields = {'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by', 'id'}

    for key, value in domain_model.dict().items():
        if key in exclude_fields:
            continue
        setattr(orm_model, key, value)

    return orm_model
