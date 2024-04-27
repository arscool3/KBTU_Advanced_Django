from pydantic import BaseModel
from typing import List, Optional

# Base Schemas
class BaseClassSchema(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True

# Clan Schema
class ClanSchemaBase(BaseClassSchema):
    total_profit: str

class ClanSchema(ClanSchemaBase):
    pass

# Forward declaration for recursive models
ClanSchema.update_forward_refs()

# Human Schema
class HumanSchema(BaseClassSchema):
    surname: str
    clan_id: Optional[int]

class ClanLeaderSchema(HumanSchema):
    abilities: str

# Territory Schema
class TerritorySchema(BaseClassSchema):
    address: str
    clan_id: Optional[int]

# Business Schema
class BusinessSchema(BaseClassSchema):
    profit: int
    clan_id: Optional[int]

# Relations Schema
class RelationsSchema(BaseModel):
    id: Optional[int]
    name: str
    clan_1_id: Optional[int]
    clan_2_id: Optional[int]
    relation_status: str

    class Config:
        orm_mode = True

# Update Schemas with Relationships
class ClanExtendedSchema(ClanSchemaBase):
    members: List[HumanSchema] = []
    clan_leader: Optional[ClanLeaderSchema]
    territory: Optional[TerritorySchema]

# Use this schema where you need detailed information about clans including relationships
