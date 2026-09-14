from pydantic import BaseModel, Field


class AuthenticatedUser(BaseModel):
    oid: str = Field(
        description="Stable Azure Object ID from the NTU Microsoft tenant.",
        examples=["00000000-0000-0000-0000-000000000000"],
    )
    email: str = Field(
        description="NTU email from the Microsoft identity token.",
        examples=["student@e.ntu.edu.sg"],
    )
    name: str = Field(
        description="Display name from the Microsoft identity token.",
        examples=["NTU Student"],
    )
