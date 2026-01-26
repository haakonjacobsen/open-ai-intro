import json
from datetime import date
from pathlib import Path

from pydantic import BaseModel

DB_PATH = Path(__file__).parent / "database" / "celebrity.json"


class Celebrity(BaseModel):
    name: str
    profession: str
    birthdate: date


class CelebrityDatabase:
    def read(self, id: str) -> Celebrity | None:
        data = json.loads(DB_PATH.read_text())
        if id in data:
            return Celebrity(**data[id])
        return None

    def write(self, celebrity: Celebrity) -> str:
        """Write a celebrity to the database. Returns the assigned ID."""
        data = json.loads(DB_PATH.read_text())
        
        # Check if celebrity already exists by name
        for id, existing in data.items():
            if existing["name"].lower() == celebrity.name.lower():
                data[id] = celebrity.model_dump(mode='json')
                DB_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
                return id
        
        # Find next available numeric key
        numeric_keys = [int(k) for k in data.keys() if k.isdigit()]
        next_id = str(max(numeric_keys, default=-1) + 1)
        
        data[next_id] = celebrity.model_dump(mode='json')
        DB_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        return next_id

    def read_all(self) -> dict[str, Celebrity]:
        data = json.loads(DB_PATH.read_text())
        return {k: Celebrity(**v) for k, v in data.items()}

    def search(self, name: str) -> dict[str, Celebrity]:
        results = {}
        for id, celeb in self.read_all().items():
            if name.lower() in celeb.name.lower():
                results[id] = celeb
        return results
