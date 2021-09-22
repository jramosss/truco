from pydantic import BaseModel, Field


class RoomCreationRequest(BaseModel):
    """
    Body of the request used to create a new room,
    Identifying owner by email isn't optimal(?)
    """

    name: str = Field(..., min_length=2, max_length=20, description="The room's name")
    max_players: int = Field(
        ..., ge=2, le=6, description="Max allowed players in the room"
    )


class ChatRequest(BaseModel):
    """
    Body of the request used for sending messages to the chat.
    """

    msg: str = Field(
        ..., max_length=256, min_length=1, description="The message you want to send"
    )
