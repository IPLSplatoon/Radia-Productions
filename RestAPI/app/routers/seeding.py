from fastapi import APIRouter, Request, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
import aiohttp
import csv
import io

router = APIRouter()


@router.get("/battlefy/{tournament_id}")
async def battlefy_seed_csv(request: Request, tournament_id: str):
    """Returns a CSV of teams and players for seeding use"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://dtmwra1jsgyb0.cloudfront.net/tournaments/{tournament_id}/teams") as resp:
            data = await resp.json()
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail=f"{data['error']}")
            # If status is 200
            # Create in-memory store for csv writer
            csv_file = io.StringIO()
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(
                ["team", "player1", "player2", "player3", "player4", "player5", "player6", "player7", "player8"])
            for team in data:
                team_row = [team['name']]
                for p in team.get('players'):
                    name = p['inGameName']
                    if name[0] is "=":
                        name = f".{name}"
                    team_row.append(name)
                csv_writer.writerow(team_row)
            # Return CSV
            response = StreamingResponse(iter([csv_file.getvalue()]), media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=teams.csv"
            return response
