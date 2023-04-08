import giteapy
import os
from dotenv import load_dotenv
from fastapi import FastAPI

from pydantic import BaseModel


class Item(BaseModel):
    title: str
    description: str


load_dotenv()

app = FastAPI()

gitea_config = giteapy.Configuration()
gitea_config.host = os.getenv("GITEA_HOST")
gitea_config.api_key["access_token"] = os.getenv("GITEA_TOKEN")
issue_api = giteapy.IssueApi(giteapy.ApiClient(gitea_config))


@app.post("/hooks", status_code=204)
async def hooks(item: Item):
    body = f"""{item.description}
    
    {os.getenv('DSM_HOST')}
    """
    issue = {
        "assignee": os.getenv("GITEA_ASSIGNEE"),
        "body": body,
        "title": item.title
    }
    issue_api.issue_create_issue(
        owner=os.getenv("GITEA_ISSUE_OWNER"),
        repo=os.getenv("GITEA_ISSUE_REPO"),
        body=issue
    )

