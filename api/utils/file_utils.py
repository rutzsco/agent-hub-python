from typing import List, Optional
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole


async def download_and_process_file(blob_service_client, file_path: str):
    """Download and process file from blob storage"""
    # This is a placeholder implementation
    # You would implement the actual file download logic here
    return None, None


def create_chat_message_content(user_message: str, file_content: Optional[str] = None,
                                file_name: Optional[str] = None, ai_project_file=None) -> List[ChatMessageContent]:
    """Create chat message content from user message and optional file"""
    messages = []

    # Add the user message
    message_content = ChatMessageContent(
        role=AuthorRole.USER, content=user_message)

    # If there's file content, add it to the message
    if file_content and file_name:
        message_content.content += f"\n\nFile content from {file_name}:\n{file_content}"

    messages.append(message_content)
    return messages
